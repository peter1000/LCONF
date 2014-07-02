""" Main LCONF module

   **Module CONSTANTS:**
      LCONF_BASE_INDENT `int` - the lconf base indentation (number of spaces for one indentation level)

      NO_INDENT `int` - no indentation

      ONE_INDENT `int` - used by main lists and Repeated l_blocks Names

      TWO_INDENT `int` - used by l_blocks key/value pairs

      THREE_INDENT `int` - used by BLK lists
"""
import copy
from os import path
from pickle import (
   dumps as pdumps,
   loads as ploads,
   HIGHEST_PROTOCOL as P_HIGHEST_PROTOCOL
)

from RDICT.MainCode import (
   Rdict,
   RdictFO,
   RdictFO2,
   RdictIO
)

from LCONF.ProjectErr import Err


LCONF_BASE_INDENT = 3
NO_INDENT = 0
ONE_INDENT = LCONF_BASE_INDENT
TWO_INDENT = LCONF_BASE_INDENT * 2
THREE_INDENT = LCONF_BASE_INDENT * 3
SECTION_START_TAG = '___SECTION'
SECTION_END_TAG = '___END'


def lconf_extract_all_sections(source):
   """ Extracts all LCONF-Sections from the raw string.

   Args:
      source (raw str): which contains one or more LCONF-Sections

   Returns:
      list: of LCONF-Sections text each inclusive the ___SECTION, ___END TAG
         these are not split by line but all in one txt
   """
   len_section_start_tag = len(SECTION_START_TAG)
   len_section_end_tag = len(SECTION_END_TAG)

   lconf_sections = []
   # Assumption is that most of the time LCONF: is parsed from not extremely large files
   # Fastest: read the whole file at once and split it: instead of iter over the file object for line in file
   # cut all between first : ___SECTION and last ___END: raise already error if one of them is not found(using str.index)
   first_start_idx = source.index(SECTION_START_TAG)
   last_end_idx = source.rindex(SECTION_END_TAG)
   main_text_source = source[first_start_idx:last_end_idx + len_section_end_tag]
   # Check multiple sections in source:
   if SECTION_START_TAG in main_text_source[len_section_start_tag:]:
      start_idx = 0  # keep first ___SECTION TAG but search for ___END TAG
      search_for_start = False
      from_here_idx = start_idx
      while True:
         if search_for_start:
            start_idx = main_text_source[from_here_idx:].find(SECTION_START_TAG)
            if start_idx == -1:
               break  # no more docs
            search_for_start = False
            from_here_idx = from_here_idx + start_idx
         else:
            end_idx = main_text_source[from_here_idx:].find(SECTION_END_TAG)
            if end_idx == -1:
               raise Err('lconf_extract_all_sections', 'END_TAG_NOT_FOUND: expected <{}> Search text was: main_text_source[from_here_idx:] \n\n{}'.format(SECTION_END_TAG, main_text_source[from_here_idx:]))
            # add doc
            end_idx_with_tag = from_here_idx + end_idx + len_section_end_tag
            tmp_section_txt = main_text_source[from_here_idx:end_idx_with_tag]
            if SECTION_START_TAG in tmp_section_txt[len_section_start_tag:]:
               raise Err('lconf_extract_all_sections', 'START-TAG FOUND within LCONF-Section. Section text:\n\n==================\n{}\n==================\n'.format(tmp_section_txt))
            lconf_sections.append(main_text_source[from_here_idx:end_idx_with_tag])
            search_for_start = True
            from_here_idx = end_idx_with_tag
   else:
      if SECTION_END_TAG in main_text_source[:-len_section_end_tag]:
         raise Err('lconf_extract_all_sections', 'END-TAG FOUND within LCONF-Section. Section text:\n\n==================\n{}\n==================\n'.format(main_text_source))
      lconf_sections.append(main_text_source)
   return lconf_sections


def lconf_extract_one_section_by_name(source, section_name):
   """ Extracts one LCONF-Sections from the raw string.

   This will immediately return if the given section is found and not scan the whole source

   Args:
      source (raw str): which contains one or more LCONF-Sections
      section_name (str): section name: which one wants to extract from the `source`

   Returns:
      str: Extracted LCONF-Sections text inclusive the ___SECTION, ___END TAG
         these are not split by line but all in one txt

   Raises:
      LCONF.Err: if a section with `section_name` is not found
   """
   len_section_start_tag = len(SECTION_START_TAG)
   len_section_end_tag = len(SECTION_END_TAG)

   full_start_line = '{} :: {}'.format(SECTION_START_TAG, section_name)
   # cut all between first : ___SECTION and last ___END: raise already error if one of them is not found(using str.index)
   try:
      first_start_idx = source.index(full_start_line)
      last_end_idx = source.index(SECTION_END_TAG, first_start_idx + len_section_start_tag)
      main_text_source = source[first_start_idx:last_end_idx + len_section_end_tag]
   except ValueError:
      raise Err('lconf_extract_one_section_by_name', 'No Section with section_name: <{}> was found in the source:\n\n<{}>'.format(section_name, source))
   return main_text_source


def lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False):
   """ Split a section raw string into lines and validate the first line

   Args:
      lconf_section_raw_str (raw str): which contains one LCONF-Section
      validate_first_line (bool):  if true the first line is validated

   Returns:
      tuple: section_lines, section_name

   Raises:
      LCONF.Err: if validate_first_line=True: if the validation fails
   """
   section_lines = lconf_section_raw_str.splitlines()
   first_line = section_lines[0]

   if validate_first_line:
      # FIRST LINE: special
      if not first_line.startswith('{} :: '.format(SECTION_START_TAG)):
         raise Err('lconf_section_splitlines', 'FIRST LINE ERROR: Must start with <{} :: > LineNumber: <1>\n    <{}>'.format(SECTION_START_TAG, first_line))
      first_line_length = len(first_line)
      if first_line_length < 15:
         raise Err('lconf_section_splitlines', 'l_section_name: Minimum length 1 characters: LineNumber: <1>\n    <{}>'.format(first_line))
      elif first_line[first_line_length - 1] == ' ':
         raise Err('lconf_section_splitlines', 'TRAILING SPACE ERROR: LineNumber: <1>\n    <{}>'.format(first_line))
      elif first_line[14] == ' ':
         raise Err('lconf_section_splitlines', 'TOO MANY SPACES around < :: > ERROR: LineNumber: <1>\n    <{}>'.format(first_line))

      not_needed_start_tag, section_name = first_line.split(' :: ', 1)
   else:
      not_needed_start_tag, section_name = first_line.split(' :: ', 1)
   return section_lines, section_name


def _helper_check_list_or_key_value_mapping(section_lines_, num_section_lines_, next_idx_):
   """ Helper to find out if we have a `Key-Value-Mapping` or `Key-Value-List` based on the next none comment line

   Args:
      section_lines_ (list):
      num_section_lines_ (int):
      next_idx_ (int):

   Returns:
      bool: True  if situation: is_key_value_mapping else False (is_list situation)
   """
   # to know if we have a `Key-Value-Mapping` or `Key-Value-List` we need to check the next `none comment` line
   next_section_line = section_lines_[next_idx_]
   situation_is_key_value_mapping = True
   if '#' in next_section_line:
      tmp_next_idx = next_idx_
      while (tmp_next_idx < num_section_lines_):
         next_section_line = section_lines_[tmp_next_idx]
         if '#' in next_section_line:
            temp_check_line_indent = len(next_section_line) - len(next_section_line.lstrip())
            if next_section_line[temp_check_line_indent] == '#':
               # Comment line: check next
               tmp_next_idx += 1
               continue

         # No Comment Line check and break
         if '::' in next_section_line:
            situation_is_key_value_mapping = True
         else:
            situation_is_key_value_mapping = False
         break
   elif '::' in next_section_line:
      situation_is_key_value_mapping = True
   else:
      situation_is_key_value_mapping = False

   return situation_is_key_value_mapping


def _validate_key_value_separator(section_name, temp_line_num, temp_line, temp_line_length):
   """ Helper: Validates that there are:
      - only one space before and one space after the double colon
         - for empty string values no space after the double colon
      - MISSING characters after <::>
      - WRONG CHAR/SPACES after <::>
      - WRONG CHAR/SPACES before <::>

   Args:
      section_name (str): already extracted section name
      temp_line_num (int): line number of the section
      temp_line (raw str): which contains at least <::>  a double colon
      temp_line_length (int): length of the temp_line

   Returns:
      bool: is_empty_string_value: True if the line has an empty string value

   Raises:
      LCONF.Err: if the validation fails
   """
   is_empty_string_value = False
   colon_idx = temp_line.index('::')
   if temp_line[colon_idx - 1] != ' ':
      raise Err('_validate_key_value_separator', 'l_section_name: {}\nMISSING SPACES before <::> ERROR: LineNumber: <{}>\n    <{}>'.format(section_name, temp_line_num, temp_line))
   elif temp_line[colon_idx - 2] == ' ':
      raise Err('_validate_key_value_separator', 'l_section_name: {}\nWRONG CHAR/SPACES before <::> ERROR: LineNumber: <{}>\n    <{}>'.format(section_name, temp_line_num, temp_line))

   if ':: ' in temp_line:
      if (colon_idx + 2) > temp_line_length:
         raise Err('_validate_key_value_separator', 'l_section_name: {}\nMISSING characters after <::> ERROR: LineNumber: <{}>\n    <{}>'.format(section_name, temp_line_num, temp_line))
      elif temp_line[colon_idx + 3] == ' ':
         raise Err('_validate_key_value_separator', 'l_section_name: {}\nWRONG SPACES after <::> ERROR: LineNumber: <{}>\n    <{}>'.format(section_name, temp_line_num, temp_line))
   else:
      if (colon_idx + 2) != temp_line_length:
         raise Err('_validate_key_value_separator', 'l_section_name: {}\nEXPECTED: EMPTY STRING or a space after :: ! WRONG CHAR/SPACES after <::> ERROR: LineNumber: <{}>\n    <{}>'.format(section_name, temp_line_num, temp_line))
      is_empty_string_value = True
   return is_empty_string_value


def lconf_validate_one_section_str(lconf_section_raw_str):
   """ Validates one LCONF-Section raw string: the section must be already correctly extracted
   This does not validate with the corresponding Section-Template classes: like correct names for: Keys, Repeated Block Identifiers ect..

   Validates/Checks for:
      - No Trailing Spaces
      - Most Indentation Errors: inclusive indent of Comment lines
      - if a line is a Key/Value separator line: :
         - only one space before and one space after the double colon
            - for empty string values no space after the double colon
         - MISSING characters after <::>
         - WRONG CHAR/SPACES after <::>
         - WRONG CHAR/SPACES before <::>

   Args:
      lconf_section_raw_str (raw str): which contains one extracted LCONF-Sections inclusive the Start/End Tags

   Returns:
      bool: True  if success else raises an error

   Raises:
      LCONF.Err: if the validation fails
   """
   is_key_value_mapping = 2
   is_list = 3
   is_blk = 4

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   num_section_lines = len(section_lines)

   main_situation = None
   block_situation = None
   prev_indent = 0

   next_idx = 1
   # Validate END-TAG (last line) has no indent
   if section_lines[num_section_lines - 1] != SECTION_END_TAG:
      raise Err('lconf_validate_source', 'l_section_name: {}\nEND-TAG LINE ERROR: EXPECTED: <{}>\n    LineNumber: <{}>\n      <{}>'.format(section_name, SECTION_END_TAG, num_section_lines, section_lines[num_section_lines - 1]))

   for orig_line in section_lines[1:-1]:
      next_idx += 1
      count_lines = next_idx
      if orig_line:
         # Main list
         orig_line_length = len(orig_line)
         # Validate: No Trailing Spaces
         if orig_line[orig_line_length - 1] == ' ':
            raise Err('lconf_validate_source', 'l_section_name: {}\nTRAILING SPACE ERROR: LineNumber: <{}>\n  <{}>'.format(section_name, count_lines, orig_line))
         if orig_line[NO_INDENT] != ' ':
            if orig_line[0] == '#':
               # check next line indent
               temp_next_line_indent = len(section_lines[next_idx]) - len(section_lines[next_idx].lstrip())
               if temp_next_line_indent != NO_INDENT:
                  raise Err('lconf_validate_source', 'l_section_name: {}\nINDENTATION COMMENT LINE ERROR: LineNumber: <{}>\n  <{}>\n    Current Comment Line indent: <{}> spaces\n      must be the same as the `next line indent: <{}> spaces'.format(section_name, count_lines, orig_line, NO_INDENT, temp_next_line_indent))
               continue
            main_situation = None
            block_situation = None
            if '::' in orig_line:
               # Validate: Key Value separator
               _validate_key_value_separator(section_name, count_lines, orig_line, orig_line_length)
            elif orig_line[0] == '*':
               main_situation = is_blk
               # check proper Block Identifier: no leading white space
               if orig_line[2] == ' ':
                  raise Err('lconf_validate_source', 'SectionName: {}\nBLOCK IDENTIFIER NAME ERROR: LineNumber: <{}>\n  <{}>\n    Got TOO MANY SPACES after the `asterisk`. Expected `one space`.'.format(section_name, count_lines, orig_line))
            else:
               # to know if we have a `Key-Value-Mapping` or `Key-Value-List` we need to check the next `none comment` line
               situation_is_key_value_mapping = _helper_check_list_or_key_value_mapping(section_lines, num_section_lines, next_idx)
               if situation_is_key_value_mapping:
                  main_situation = is_key_value_mapping
               else:
                  main_situation = is_list
            prev_indent = NO_INDENT
         # # # #
         else:
            cur_indent = orig_line_length - len(orig_line.lstrip())
            if orig_line[cur_indent] == '#':
               # check next line indent
               temp_next_line_indent = len(section_lines[next_idx]) - len(section_lines[next_idx].lstrip())
               if temp_next_line_indent != cur_indent:
                  raise Err('lconf_validate_source', 'l_section_name: {}\nINDENTATION COMMENT LINE ERROR: LineNumber: <{}>\n  <{}>\n    Current Comment Line indent: <{}> spaces\n      must be the same as the `next line indent: <{}> spaces'.format(section_name, count_lines, orig_line, cur_indent, temp_next_line_indent))
               continue
            if main_situation == is_blk:
               # check jump indentation
               if cur_indent > (prev_indent + LCONF_BASE_INDENT):
                  raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION LEVEL JUMP ERROR: LineNumber: <{}>\n  <{}>\n    previous indent: <{}> - current indent: <{}>'.format(section_name, count_lines, orig_line, prev_indent, cur_indent))
               # BLK-Name
               if cur_indent == ONE_INDENT:
                 # Check NO: Key Value separator
                  if '::' in orig_line:
                     raise Err('lconf_validate_source', 'SectionName: {}\nLCONF ERROR: LineNumber: <{}>\n  BLOCK `Block-Name`: Expected no `Key-Value-Separator in the line.\n    <{}>'.format(section_name, count_lines, orig_line))
               elif cur_indent == TWO_INDENT:
                  block_situation = None
                  # Validate: Key Value separator
                  if '::' in orig_line:
                     _validate_key_value_separator(section_name, count_lines, orig_line, orig_line_length)
                  else:
                     # to know if we have a `Key-Value-Mapping` or `Key-Value-List` we need to check the next `none comment` line
                     situation_is_key_value_mapping = _helper_check_list_or_key_value_mapping(section_lines, num_section_lines, next_idx)
                     if situation_is_key_value_mapping:
                        block_situation = is_key_value_mapping
                     else:
                        block_situation = is_list
               elif cur_indent == THREE_INDENT:
                  if block_situation == is_key_value_mapping:
                     # Validate: Key Value separator
                     if '::' in orig_line:
                        _validate_key_value_separator(section_name, count_lines, orig_line, orig_line_length)
                     else:
                        raise Err('lconf_validate_source', 'SectionName: {}\nLCONF ERROR: LineNumber: <{}>\n  BLOCK `Key-Value-Mapping`: Expected a `Key-Value-Separator in the line.\n    <{}>'.format(section_name, count_lines, orig_line))
                  elif block_situation == is_list:
                     # Check NO: Key Value separator
                     if '::' in orig_line:
                        raise Err('lconf_validate_source', 'SectionName: {}\nLCONF ERROR: LineNumber: <{}>\n  BLOCK `Key-Value-List`: Expected no `Key-Value-Separator in the line.\n    <{}>'.format(section_name, count_lines, orig_line))
                  else:
                     raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION ERROR: LineNumber: <{}>\n  <{}>\n    No previous: `BLOCK Key-Value-List` or `BLOCK Key-Value-Mapping`'.format(section_name, count_lines, orig_line))
               else:
                  raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION ERROR: LineNumber: <{}>\n  <{}>\n    MAIN `BLOCK`: Expected: <{}>, <{}> or <{}> spaces: but we got: indent of: <{}>'.format(section_name, count_lines, orig_line, ONE_INDENT, TWO_INDENT, THREE_INDENT, cur_indent))
            elif main_situation == is_list:
               if cur_indent != ONE_INDENT:
                  raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION ERROR: LineNumber: <{}>\n  <{}>\n    MAIN `Key-Value-List`: Expected: <{}> spaces: but we got: indent of: <{}>'.format(section_name, count_lines, orig_line, ONE_INDENT, cur_indent))
               # Check NO: Key Value separator
               if '::' in orig_line:
                  raise Err('lconf_validate_source', 'SectionName: {}\nLCONF ERROR: LineNumber: <{}>\n  MAIN `Key-Value-List`: Expected no `Key-Value-Separator in the line.\n    <{}>'.format(section_name, count_lines, orig_line))
            elif main_situation == is_key_value_mapping:
               if cur_indent != ONE_INDENT:
                  raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION ERROR: LineNumber: <{}>\n  <{}>\n    MAIN `Key-Value-Mapping`: Expected: <{}> spaces: but we got: indent of: <{}>'.format(section_name, count_lines, orig_line, ONE_INDENT, cur_indent))
               # Validate: Key Value separator
               if '::' in orig_line:
                  _validate_key_value_separator(section_name, count_lines, orig_line, orig_line_length)
               else:
                  raise Err('lconf_validate_source', 'SectionName: {}\nLCONF ERROR: LineNumber: <{}>\n  MAIN `Key-Value-Mapping`: Expected a `Key-Value-Separator in the line.\n    <{}>'.format(section_name, count_lines, orig_line))
            else:
               raise Err('lconf_validate_source', 'SectionName: {}\nINDENTATION ERROR: LineNumber: <{}>\n  <{}>\n    No previous: `MAIN Block`, `MAIN Key-Value-List` or `MAIN Key-Value-Mapping`\n    Expected no indentation but we got: indent of: <{}>'.format(section_name, count_lines, orig_line, cur_indent))

            prev_indent = cur_indent
   return True


def lconf_validate_source(lconf_source):
   """ Validates a LCONF-Section raw string containing one or more LCONF-Sections
   This does not validate with the corresponding Section-Template classes: like correct names for: Keys, Repeated Block Identifiers ect..

   IMPORTANT NOTE: this uses the function: lconf_extract_all_sections() to extract valid LCONF-Sections. If a code extracts sections in an other way the first/last line might differ

   Validates/Checks for:
      - No Trailing Spaces
      - Most Indentation Errors: inclusive indent of Comment lines
      - if a line is a Key/Value separator line: :
         - only one space before and one space after the double colon
            - for empty string values no space after the double colon
         - MISSING characters after <::>
         - WRONG CHAR/SPACES after <::>
         - WRONG CHAR/SPACES before <::>

   Args:
      lconf_source (raw str): which contains one or more LCONF-Sections

   Returns:
      bool: True  if success else raises an error

   Raises:
      LCONF.Err: if the validation fails
   """
   for section_lconf_source in lconf_extract_all_sections(lconf_source):
      lconf_validate_one_section_str(section_lconf_source)
   return True


def lconf_validate_file(path_to_lconf_file):
   """ Validates a file containing one or more LCONF-Sections
   This does not validate with the corresponding Section-Template classes: like correct names for: Keys, Repeated Block Identifiers ect..

   IMPORTANT NOTE: this uses the function: lconf_extract_all_sections() to extract valid LCONF-Sections. If code extracts sections in an other way the first/last line might differ

   Validates/Checks for:
      - No Trailing Spaces
      - Most Indentation Errors
      - if a line is a Key/Value separator line
         - only one space before and one space after the double colon
         - for empty string values no space after the double colon
         - MISSING characters after <::>
         - WRONG CHAR/SPACES after <::>
         - WRONG CHAR/SPACES before <::>

   Args:
      path_to_lconf_file (str): path to a file

   Returns:
      bool: True  if success else raises an error

   Raises:
      LCONF.Err: if the validation fails
   """
   if not path.isfile(path_to_lconf_file):
      raise Err('lconf_validate_file', 'Input path seems not to be a file:\n   <{}>'.format(path_to_lconf_file))

   print('\n\n====== VALIDATING SECTIONS IN FILE:\n   <{}>'.format(path_to_lconf_file))
   with open(path_to_lconf_file, 'r') as file_:
      for section_lconf_source in lconf_extract_all_sections(file_.read()):
         lconf_validate_one_section_str(section_lconf_source)
   return True


def _prepare_default_obj(lconf_section__template_obj):
   """ Helper: to make a recursively copy of the lconf_section__template_obj with the same `key_order` and `extra_key_order` set to all none `Default-Comment/Empty Lines` keys

   .. seealso:: lconf_prepare_default_obj, lconf_prepare_default_obj_pickled

   Args:
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform func`

   Returns:
      obj: adjusted/prepared copy of the lconf_section__template_obj
   """
   if isinstance(lconf_section__template_obj, RdictFO2):
      # need to output `RdictFO` because we need to overwrite the values
      temp_obj = RdictFO([(key, _prepare_default_obj(lconf_section__template_obj[key][0]) if isinstance(lconf_section__template_obj[key], tuple) else _prepare_default_obj(lconf_section__template_obj[key])) for key in lconf_section__template_obj.__dict__['key_order']], init_extra_key_order=False)
      # set extra_key_order: without any `Default-Comment/Empty Lines`
      temp_obj.replace_extra_key_order([key for key in lconf_section__template_obj.__dict__['key_order'] if key[0] != '#'])
      return temp_obj
   elif isinstance(lconf_section__template_obj, RdictIO):
      return RdictIO([(key, _prepare_default_obj(lconf_section__template_obj[key])) for key in lconf_section__template_obj.__dict__['key_order']], init_extra_key_order=False)
   else:
      return copy.copy(lconf_section__template_obj)


def lconf_prepare_default_obj(lconf_section__template_obj):
   """ Returns a recursively copy of the lconf_section__template_obj with the same `key_order`

   - only supports: RdictFO2/RdictIO recursively - all others are a normal copy.copy

      - No `extra_data` is copied

   - The values tuples are overwritten with the default value: the transform function info is skipped

   Args:
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform func` type-conversion

   Returns:
      lconf_default_obj obj: copy of the lconf_section__template_obj

      - additionally added: 'extra_data': will have keys:

         - l_section_name: init with: missing section name
         - l_parsed: init with False
   """
   lconf_default_obj = _prepare_default_obj(lconf_section__template_obj)
   # set extra data
   lconf_default_obj.update_extra_data({'l_section_name': 'missing section name', 'l_parsed': False})
   return lconf_default_obj


def lconf_prepare_default_obj_pickled(lconf_section__template_obj):
   """ Returns a pickled recursively copy of the lconf_section__template_obj with the same `key_order`

      - Mainly useful if multiple section of the same `lconf_section__template_obj` should be parsed

   - only supports: RdictFO2/RdictIO recursively - all others are a normal copy.copy

      - No `extra_data` is copied

   - The values tuples are overwritten with the default value: the transform function info is skipped

   Args:
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform func` type-conversion

   Returns:
      bytes: (pickled lconf_default_obj obj): copy of the lconf_section__template_obj
   """
   lconf_default_obj = _prepare_default_obj(lconf_section__template_obj)
   # set extra data
   lconf_default_obj.update_extra_data({'l_section_name': 'missing section name', 'l_parsed': False})
   return pdumps(lconf_default_obj)


def lconf_prepare_and_parse_section(lconf_section_raw_str, lconf_section__template_obj, validate=False):
   """ Returns a new parsed lconf obj. Basically it does lconf_prepare_default_obj() and lconf_parse_section

   Args:
      lconf_section_raw_str (raw str): which contains one LCONF-Section
      lconf_section__template_obj (obj): instance of main section template object which has all the info
      validate (bool):

         - if True the `lconf_section_raw_str` is first validated and only afterwards parsed
         - if False: no validation is done

   Returns:
      obj: copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally added: 'extra_data': will have keys:

         - l_section_name: updated with the LCONF-SectionName
         - l_parsed: set to True; so one can know if this obj was already parsed
   """
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   # Prepare
   lconf_default_obj = _prepare_default_obj(lconf_section__template_obj)
   # set extra data
   lconf_default_obj.update_extra_data({'l_section_name': 'missing section name', 'l_parsed': False})
   # Parse
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_prepare_and_parse_section_lines(section_lines, section_name, lconf_section__template_obj):
   """ Returns a new parsed lconf obj. Basically it does lconf_prepare_default_obj() and lconf_parse_section_lines()

   Args:
      section_lines (list): which contains one LCONF-Section raw string already split into lines
      section_name (str): already extracted section name
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform`

   Returns:
      obj: copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally added: 'extra_data': will have keys:

         - l_section_name: updated with the LCONF-SectionName
         - l_parsed: set to True; so one can know if this obj was already parsed
   """
   # Prepare
   lconf_default_obj = _prepare_default_obj(lconf_section__template_obj)
   # set extra data
   lconf_default_obj.update_extra_data({'l_section_name': 'missing section name', 'l_parsed': False})
   # Parse parse_section_lines
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj):
   """ Parses a LCONF-Section raw string already split into lines and updates the section object
   See also: lconf_extract_all_sections

   Args:
      lconf_default_obj (obj): a prepared copy of lconf_section__template_obj: see function: lconf_prepare_default_obj()
      section_lines (list): which contains one LCONF-Section raw string already split into lines
      section_name (str): already extracted section name
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform`

   Returns:
      obj: updated lconf_default_obj: attributes updated by the data in lconf_section_raw_str

         - lconf_section_obj: 'extra_data': updated

            - l_section_name: updated with the LCONF-SectionName
            - l_parsed: set to True; so one can know if this obj was already parsed
   """
   # MAIN LCONF object: enforce type: RdictFO
   if not isinstance(lconf_default_obj, RdictFO):
      raise Err('lconf_parse_section_lines', 'LCONF ERROR: The MAIN LCONF object need to be of type: <RdictFO>. We got: <{}>\n    <{}>'.format(type(lconf_default_obj), lconf_default_obj))

   num_section_lines = len(section_lines)

   lconf_default_obj.extra_data['l_section_name'] = section_name
   is_key_value_mapping = 2
   is_list = 3
   is_blk = 4

   main_situation = None
   block_situation = None

   cur_key_value_mapping = None

   cur_blk_obj_key_value_mapping = None
   cur_blk_obj_items_list = []
   cur_base_blk_obj = None

   base_blk_obj_pickle = None
   cur_dict_blk__names = None

   base_blk__template_obj = None
   key_value_mapping__template_obj = None
   temp_transform_list = object

   next_idx = 1
   for orig_line in section_lines[1:-1]:
      next_idx += 1
      if orig_line:
         # Main list
         if orig_line[NO_INDENT] != ' ':
            if orig_line[0] == '#':
               continue
            main_situation = None
            if ':: ' in orig_line:
               name, value = orig_line.split(' :: ', 1)
               if value[0] == '[':
                  if value == '[]':
                     value = []
                  # TRANSFORM CHECK
                  elif isinstance(lconf_section__template_obj[name], tuple):
                     temp_value = value[1:-1].split(',')
                     value = []
                     for temp_item in temp_value:
                        value.append(lconf_section__template_obj[name][1](temp_item, orig_line))
                  else:
                     value = value[1:-1].split(',')
               # TRANSFORM CHECK
               elif isinstance(lconf_section__template_obj[name], tuple):
                  value = lconf_section__template_obj[name][1](value, orig_line)
               # overwrite it
               lconf_default_obj[name] = value
            elif '::' in orig_line:
               name, value = orig_line.split(' ::', 1)
               if value:
                  raise Err('lconf_parse_section_lines', 'LCONF ERROR: MAIN: Expected an empty string value for `Key :: Value Pair`\n    <{}>'.format(orig_line))
               lconf_default_obj[name] = value
            elif orig_line[0] == '*':
               main_situation = is_blk
               sub_str = orig_line[2:]
               #  NOTE: BLK-Identifier and BLK-Names do not have any `transform`
               base_blk__template_obj = lconf_section__template_obj[sub_str]['dummy_blk']
               # use pickle directly instead of: topickle: it's slightly faster
               base_blk_obj_pickle = pdumps(lconf_default_obj[sub_str]['dummy_blk'], protocol=P_HIGHEST_PROTOCOL)
               # use a new RdictIO
               cur_dict_blk__names = RdictIO([])
               # overwrite it
               lconf_default_obj[sub_str] = cur_dict_blk__names
            else:
               # to know if we have a `Key-Value-Mapping` or `Key-Value-List` we need to check the next `none comment` line
               situation_is_key_value_mapping = _helper_check_list_or_key_value_mapping(section_lines, num_section_lines, next_idx)
               if situation_is_key_value_mapping:
                  main_situation = is_key_value_mapping
                  key_value_mapping__template_obj = lconf_section__template_obj[orig_line]
                  cur_key_value_mapping = lconf_default_obj[orig_line]  # get the default for this `Key-Value-Mapping`
                  # Key-Value-Mapping object: enforce type: RdictFO
                  if not isinstance(cur_key_value_mapping, RdictFO):
                     raise Err('lconf_parse_section_lines', 'LCONF ERROR: MAIN `Key-Value-Mapping` need to be of type: <RdictFO>. We got: <{}>\n    <{}>'.format(type(cur_key_value_mapping), orig_line))
               else:
                  main_situation = is_list
                  # TRANSFORM CHECK
                  if isinstance(lconf_section__template_obj[orig_line], tuple):
                     temp_transform_list = lconf_section__template_obj[orig_line][1]
                  else:
                     temp_transform_list = None
                  cur_list = []
                  lconf_default_obj[orig_line] = cur_list
         # Situation could be:
         #  Block-Name  (Repeated Mapping-Block)
         #  `Key-Value-Mapping`  Key :: Value pair line
         #  `Value or `Key-Value-List` Value line
         elif orig_line[ONE_INDENT] != ' ':
            if orig_line[ONE_INDENT] == '#':
               continue
            if main_situation == is_key_value_mapping:
               sub_str = orig_line[ONE_INDENT:]
               if ':: ' in orig_line:
                  name, value = sub_str.split(' :: ', 1)
                  # TRANSFORM CHECK
                  if isinstance(key_value_mapping__template_obj[name], tuple):
                     cur_key_value_mapping[name] = key_value_mapping__template_obj[name][1](value, name)
                  else:
                     cur_key_value_mapping[name] = value
               elif '::' in orig_line:
                  name, value = sub_str.split(' ::', 1)
                  if value:
                     raise Err('lconf_parse_section_lines', 'LCONF ERROR: MAIN `Key-Value-Mapping`: Expected an empty string value for `Key :: Value Pair`\n    <{}>'.format(orig_line))
                  cur_key_value_mapping[name] = value
            elif main_situation == is_list:
               if temp_transform_list:
                  cur_list.append(temp_transform_list(orig_line[ONE_INDENT:], orig_line))
               else:
                  cur_list.append(orig_line[ONE_INDENT:])
            # Block-Name
            elif main_situation == is_blk:
               cur_base_blk_obj = ploads(base_blk_obj_pickle)
               # BLK object: enforce type: RdictFO
               if not isinstance(cur_base_blk_obj, RdictFO):
                  raise Err('lconf_parse_section_lines', 'LCONF ERROR: `Repeated Blocks` need to be of type: <RdictFO>. We got: <{}>\n    <{}>'.format(type(cur_base_blk_obj), orig_line))
               sub_str = orig_line[ONE_INDENT:]
               cur_dict_blk__names[sub_str] = cur_base_blk_obj
            else:
               raise Err('lconf_parse_section_lines', 'UNKNOWN ERROR: Expected Block-Name: but no `Repeated Mapping-Block` was recognized\n    <{}>'.format(orig_line))
         # Block-Object
         elif orig_line[TWO_INDENT] != ' ':
            if orig_line[TWO_INDENT] == '#':
               continue
            block_situation = None
            sub_str = orig_line[TWO_INDENT:]
            if ':: ' in orig_line:
               name, value = sub_str.split(' :: ', 1)
               if value[0] == '[':
                  if value == '[]':
                     value = []
                  # TRANSFORM CHECK
                  elif isinstance(base_blk__template_obj[name], tuple):
                     temp_value = value[1:-1].split(',')
                     value = []
                     for temp_item in temp_value:
                        value.append(base_blk__template_obj[name][1](temp_item, orig_line))
                  else:
                     value = value[1:-1].split(',')
               # TRANSFORM CHECK
               elif isinstance(base_blk__template_obj[name], tuple):
                  value = base_blk__template_obj[name][1](value, orig_line)
               # overwrite it
               cur_base_blk_obj[name] = value
            elif '::' in orig_line:
               name, value = sub_str.split(' ::', 1)
               if value:
                  raise Err('lconf_parse_section_lines', 'LCONF ERROR: Block-Item: Expected an empty string value for `Key :: Value Pair`\n    <{}>'.format(orig_line))
               cur_base_blk_obj[name] = value
            else:
               # to know if we have a `Key-Value-Mapping` or `Key-Value-List` we need to check the next `none comment` line
               situation_is_key_value_mapping = _helper_check_list_or_key_value_mapping(section_lines, num_section_lines, next_idx)
               if situation_is_key_value_mapping:
                  block_situation = is_key_value_mapping
                  key_value_mapping__template_obj = base_blk__template_obj[sub_str]
                  cur_blk_obj_key_value_mapping = cur_base_blk_obj[sub_str]  # get the default for this `Key-Value-Mapping`
                  # BLK Key-Value-Mapping object: enforce type: RdictFO
                  if not isinstance(cur_blk_obj_key_value_mapping, RdictFO):
                     raise Err('lconf_parse_section_lines', 'LCONF ERROR: BLOCK `Key-Value-Mapping` need to be of type: <RdictFO>. We got: <{}>\n    <{}>'.format(type(cur_blk_obj_key_value_mapping), orig_line))
               else:
                  block_situation = is_list
                  # TRANSFORM CHECK
                  if isinstance(base_blk__template_obj[sub_str], tuple):
                     temp_transform_list = base_blk__template_obj[sub_str][1]
                  else:
                     temp_transform_list = None
                  cur_blk_obj_items_list = []
                  cur_base_blk_obj[sub_str] = cur_blk_obj_items_list
         # Situation could be:
         #  Block-Item  `Key-Value-Mapping`  Key :: Value pair line
         #  Block-Item  `Value or `Key-Value-List` Value line
         elif orig_line[THREE_INDENT] != ' ':
            if orig_line[THREE_INDENT] == '#':
               continue
            if block_situation == is_key_value_mapping:
               sub_str = orig_line[THREE_INDENT:]
               if ':: ' in orig_line:
                  name, value = sub_str.split(' :: ', 1)
                  # TRANSFORM CHECK
                  if isinstance(key_value_mapping__template_obj[name], tuple):
                     cur_blk_obj_key_value_mapping[name] = key_value_mapping__template_obj[name][1](value, name)
                  else:
                     cur_blk_obj_key_value_mapping[name] = value
               elif '::' in orig_line:
                  name, value = sub_str.split(' ::', 1)
                  if value:
                     raise Err('lconf_parse_section_lines', 'LCONF ERROR: BLOCK `Key-Value-Mapping`: Expected an empty string value for `Key :: Value Pair`\n    <{}>'.format(orig_line))
                  cur_blk_obj_key_value_mapping[name] = value
            elif block_situation == is_list:
               if temp_transform_list:
                  cur_blk_obj_items_list.append(temp_transform_list(orig_line[THREE_INDENT:], orig_line))
               else:
                  cur_blk_obj_items_list.append(orig_line[THREE_INDENT:])
         else:
            raise Err('lconf_parse_section_lines', 'LCONF ERROR: <{}>: Wrong indentation'.format(orig_line))

   lconf_default_obj.extra_data['l_parsed'] = True

   return lconf_default_obj


def lconf_parse_section(lconf_default_obj, lconf_section_raw_str, lconf_section__template_obj, validate=False):
   """ Parses a LCONF-Section raw string and updates the section object

   Args:
      lconf_default_obj (obj): a prepared copy of lconf_section__template_obj: see function: lconf_prepare_default_obj()
      lconf_section_raw_str (raw str): which contains one LCONF-Section
      lconf_section__template_obj (obj): instance of main section template object which has all the info
      validate (bool):

         - if True the `lconf_section_raw_str` is first validated and only afterwards parsed
         - if False: no validation is done

   Returns:
      obj: updated lconf_default_obj: attributes updated by the data in lconf_section_raw_str.

         - lconf_section_obj: 'extra_data': updated

            - l_section_name: updated with the LCONF-SectionName
            - l_parsed: set to True; so one can know if this obj was already parsed
   """
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_parse_section_pickled(lconf_default_obj_pickled, lconf_section_raw_str, lconf_section__template_obj, validate=False):
   """ Parses a LCONF-Section raw string and returns an updated copy of the the section object

      - Mainly useful if multiple section of the same `lconf_section__template_obj` should be parsed

   Args:
      lconf_default_obj_pickled (bytes): a prepared copy of lconf_section__template_obj: see function: lconf_prepare_default_obj_pickled()
      lconf_section_raw_str (raw str): which contains one LCONF-Section
      lconf_section__template_obj (obj): instance of main section template object which has all the info
      validate (bool):

         - if True the `lconf_section_raw_str` is first validated and only afterwards parsed
         - if False: no validation is done

   Returns:
      obj: updated unpickled copy of lconf_default_obj_pickled: attributes updated by the data in lconf_section_raw_str.

         - lconf_section_obj: 'extra_data': updated

            - l_section_name: updated with the LCONF-SectionName
            - l_parsed: set to True; so one can know if this obj was already parsed
   """
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   lconf_default_obj = ploads(lconf_default_obj_pickled)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_parse_section_extract_by_name(source, section_name, lconf_section__template_obj, validate=False):
   """ Parses/Extracts one LCONF-Sections from the raw string by name and returns an updated copy of the the section object

   Similar to lconf_prepare_and_parse_section() but also extract the session by name
   - Basically it does lconf_extract_one_section_by_name(), lconf_prepare_default_obj() and lconf_parse_section()

   Main usage: if one needs only one known section from the source: if needs multiple sections it might be better to use lconf_extract_all_sections()

   Args:
      source (raw str): which contains one or more LCONF-Sections
      section_name (str): section name one wants to extract from the source
      lconf_section__template_obj (obj): instance of main section template object which has all the info
      validate (bool):

         - if True the extracted section is first validated and only afterwards parsed
         - if False: no validation is done after the section text is extracted

   Returns:
      obj: copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally added: 'extra_data': will have keys:

         - l_section_name: updated with the LCONF-SectionName
         - l_parsed: set to True; so one can know if this obj was already parsed

   Raises:
      LCONF.Err: if a section with such name (section_name) is not found / could not be parsed
   """
   # Get Section txt
   lconf_section_raw_str = lconf_extract_one_section_by_name(source, section_name)
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   # Prepare
   lconf_default_obj = _prepare_default_obj(lconf_section__template_obj)
   # set extra data
   lconf_default_obj.update_extra_data({'l_section_name': 'missing section name', 'l_parsed': False})
   # Parse
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def _output_helper_emit(result_, key_, item_value_, onelinelists_, indent=''):
   """ Helper for output: processes a MAIN or Block-Key
   """
   if isinstance(item_value_, str):
      if item_value_:
         result_.append('{}{} :: {}'.format(indent, key_, item_value_))
      else:
         result_.append('{}{} ::'.format(indent, key_))
   elif isinstance(item_value_, list):
      if onelinelists_ or not item_value_:
         temp_items = []
         for i_ in item_value_:
            temp_items.append('%s' % i_)
         result_.append('{}{} :: [{}]'.format(indent, key_, ','.join(temp_items)))
      else:
         result_.append('{}{}'.format(indent, key_))
         for a_ in item_value_:
            result_.append('{}   {}'.format(indent, a_))
   # `Key-Value-Mapping`
   elif isinstance(item_value_, RdictFO):
      result_.append('{}{}'.format(indent, key_))
      for mapping_key, mapping_value in item_value_.yield_extra_key_value_order():
         if isinstance(mapping_value, str):
            if mapping_value:
               result_.append('   {}{} :: {}'.format(indent, mapping_key, mapping_value))
            else:
               result_.append('   {}{} ::'.format(indent, mapping_key))
         else:
            result_.append('   {}{} :: {}'.format(indent, mapping_key, mapping_value))
   else:
      result_.append('{}{} :: {}'.format(indent, key_, item_value_))


def _output_helper_emit_with_comments(result_, key_, item_value_, onelinelists_, indent=''):
   """ Helper for output with_comments: processes a MAIN or Block-Key
   """
   # Default Comment/Empty Line
   if key_[0] == '#':
      if item_value_:
         result_.append('{}{}'.format(indent, item_value_))
      else:
         # empty line
         result_.append('')
   elif isinstance(item_value_, str):
      if item_value_:
         result_.append('{}{} :: {}'.format(indent, key_, item_value_))
      else:
         result_.append('{}{} ::'.format(indent, key_))
   elif isinstance(item_value_, list):
      if onelinelists_ or not item_value_:
         temp_items = []
         for i_ in item_value_:
            temp_items.append('%s' % i_)
         result_.append('{}{} :: [{}]'.format(indent, key_, ','.join(temp_items)))
      else:
         result_.append('{}{}'.format(indent, key_))
         for a_ in item_value_:
            result_.append('{}   {}'.format(indent, a_))
   # `Key-Value-Mapping`
   elif isinstance(item_value_, RdictFO):
      result_.append('{}{}'.format(indent, key_))
      for mapping_key, mapping_value in item_value_.yield_key_value_order():
         # Default Comment/Empty Line
         if mapping_key[0] == '#':
            if mapping_value:
               result_.append('   {}{}'.format(indent, mapping_value))
            else:
               # empty line
               result_.append('')
         elif isinstance(mapping_value, str):
            if mapping_value:
               result_.append('   {}{} :: {}'.format(indent, mapping_key, mapping_value))
            else:
               result_.append('   {}{} ::'.format(indent, mapping_key))
         else:
            result_.append('   {}{} :: {}'.format(indent, mapping_key, mapping_value))
   else:
      result_.append('{}{} :: {}'.format(indent, key_, item_value_))


def lconf_emit(lconf_section_obj, onelinelists=True, with_comments=True):
   """ Return a section_string from a lconf_section_obj

   Args:
      lconf_section_obj (obj): instance of main section object which will be dumped
      onelinelists (bool): defines how list items are emitted

         - if True list items are dumped on the same line as the key separated by ` :: ` in an comma separated list
            - KEY1 :: [listitem1,listitem2]
         - if False list items are dumped on separate lines using indentation: EMPTY Lists are always dumped with Key :: []
            - KEY1
                 - listitem1
                 - listitem2

      with_comments: option to emit also any defined: default empty or comment line

         - if True: any `Default Comment lines` (which include also  default EMPTY comment lines) are emitted
         - if False: any `Default Comment lines` are not emitted

   Returns:
      str: a LCONF text string
   """
   if lconf_section_obj.extra_data['l_parsed']:
      # we can assume that the MAIN obj, Blocks, and Mappings have the correct RDICT types because these are checked when they get parsed

      result = ['{} :: {}'.format(SECTION_START_TAG, lconf_section_obj.extra_data['l_section_name'])]

      # loop through main (root) LCONF OBJ
      if with_comments:
         for key, value in lconf_section_obj.yield_key_value_order():
            # Check BLOCK Identifier obj: type RdictIO: need to check that it is not the subclass: RdictFO or RdictFO2
            if isinstance(value, RdictIO) and not isinstance(value, RdictFO):
               result.append('* {}'.format(key))
               for blk_name, blk_obj in value.yield_key_value_order():
                  result.append('   {}'.format(blk_name))
                  for blk_key, block_value in blk_obj.yield_key_value_order():
                     _output_helper_emit_with_comments(result, blk_key, block_value, onelinelists, indent='      ')
            # MAIN: `Key :: Value Pairs`, `Key :: Value-Lists`, `Key-Value-Lists:` or `Key-Value-Mapping`
            else:
               _output_helper_emit_with_comments(result, key, value, onelinelists, indent='')
      else:
         for key, value in lconf_section_obj.yield_extra_key_value_order():
            # Check BLOCK Identifier obj: type RdictIO: need to check that it is not the subclass: RdictFO or RdictFO2
            if isinstance(value, RdictIO) and not isinstance(value, RdictFO):
               result.append('* {}'.format(key))
               for blk_name, blk_obj in value.yield_extra_key_value_order():
                  result.append('   {}'.format(blk_name))
                  for blk_key, block_value in blk_obj.yield_extra_key_value_order():
                     _output_helper_emit(result, blk_key, block_value, onelinelists, indent='      ')
            # MAIN: `Key :: Value Pairs`, `Key :: Value-Lists`, `Key-Value-Lists:` or `Key-Value-Mapping`
            else:
               _output_helper_emit(result, key, value, onelinelists, indent='')
   else:
      raise Err('lconf_emit', 'LCONF NOT PARSED ERROR: The `lconf_section_obj` seems not be parsed.\n    lconf_section_obj.extra_data[l_parsed]: <{}>\n    obj: <{}>'.format(lconf_section_obj.extra_data['l_parsed'], lconf_section_obj))

   result.append(SECTION_END_TAG)
   return '\n'.join(result)


def lconf_emit_default_obj(lconf_section__template_obj, section_name, onelinelists=True, emit_dummy_blks=False, with_comments=True):
   """ Return a section_string from a none parsed lconf_section_obj

   Args:
      lconf_section__template_obj (obj): instance of main section template object which has all the info: inclusive any `l_transform func` type-conversion
      section_name (str): section name: to use
      onelinelists (bool): defines how list items are emitted

         - if True list items are dumped on the same line as the key separated by ` :: ` in an comma separated list
            - KEY1 :: [listitem1,listitem2]
         - if False list items are dumped on separate lines using indentation: EMPTY Lists are always dumped with Key :: []
            - KEY1
                 - listitem1
                 - listitem2

      emit_dummy_blks: option to emit dummy block default values

         - if True for each Repeated Block identifier a 'Dummy Block' with default values is emitted as Comment-Lines
         - if False for each Repeated Block identifier only the 'Block identifier line' is emitted

      with_comments: option to emit also any defined: default empty or comment line

         - if True: any `Default-Comment/Empty Lines` are emitted
         - if False: any `Default-Comment/Empty Lines`` are not emitted

   Returns:
      str: a LCONF text string
   """
   lconf_default_obj = lconf_prepare_default_obj(lconf_section__template_obj)
   result = ['{} :: {}'.format(SECTION_START_TAG, section_name)]

   # loop through main (root) LCONF OBJ
   if with_comments:
      for key, value in lconf_default_obj.yield_key_value_order():
         # Check BLOCK Identifier obj: type RdictIO: need to check that it is not the subclass: RdictFO or RdictFO2
         if isinstance(value, RdictIO) and not isinstance(value, RdictFO):
            result.append('* {}'.format(key))
            if emit_dummy_blks:
               for blk_name, blk_obj in value.yield_key_value_order():
                  # skip any wrong `Default-Comment/Empty Lines`
                  if blk_name[0] != '#':
                     result.append('   {}'.format(blk_name))
                     for blk_key, block_value in blk_obj.yield_key_value_order():
                        _output_helper_emit_with_comments(result, blk_key, block_value, onelinelists, indent='      ')
         # MAIN: `Key :: Value Pairs`, `Key :: Value-Lists`, `Key-Value-Lists:` or `Key-Value-Mapping`
         else:
            _output_helper_emit_with_comments(result, key, value, onelinelists, indent='')
   else:
      for key, value in lconf_default_obj.yield_extra_key_value_order():
         # Check BLOCK Identifier obj: type RdictIO: need to check that it is not the subclass: RdictFO or RdictFO2
         if isinstance(value, RdictIO) and not isinstance(value, RdictFO):
            result.append('* {}'.format(key))
            if emit_dummy_blks:
               # IMPORTANT: need for the BLK names the: yield_key_value_order
               for blk_name, blk_obj in value.yield_key_value_order():
                  # skip any wrong `Default-Comment/Empty Lines`
                  if blk_name[0] != '#':
                     result.append('   {}'.format(blk_name))
                     for blk_key, block_value in blk_obj.yield_extra_key_value_order():
                        _output_helper_emit(result, blk_key, block_value, onelinelists, indent='      ')
         # MAIN: `Key :: Value Pairs`, `Key :: Value-Lists`, `Key-Value-Lists:` or `Key-Value-Mapping`
         else:
            _output_helper_emit(result, key, value, onelinelists, indent='')

   result.append(SECTION_END_TAG)
   return '\n'.join(result)


def lconf_remove_comments(lconf_section_obj):
   """ Return a copy of lconf_section_obj with all `Default-Comment/Empty Lines` removed

   e.g. helpful for dumping to json

   Args:
      lconf_section_obj (obj): instance of main section object which will be dumped

   Returns:
      obj: lconf_section_obj (obj) with all `Default-Comment/Empty Lines` removed
   """
   def inner_copy(input_):
      if isinstance(input_, RdictIO):
         temp_new = type(input_)([(key, inner_copy(input_[key])) for key in input_.__dict__['extra_key_order']])
         temp_new.__dict__['extra_data'] = input_.__dict__['extra_data'].copy()
         # key_order: no need to copy that separately is done at __init__
         return temp_new
      elif isinstance(input_, Rdict):
         temp_new = type(input_)([(key, inner_copy(value)) for key, value in input_.items()])
         if 'extra_data' in input_.__dict__:
            temp_new.__dict__['extra_data'] = input_.__dict__['extra_data'].copy()
         return temp_new
      elif isinstance(input_, dict):
         return type(input_)((key, inner_copy(value)) for key, value in input_.items())
      elif isinstance(input_, (list, tuple)):
         return type(input_)(inner_copy(value) for value in input_)
      else:
         return copy.deepcopy(input_)
   return inner_copy(lconf_section_obj)


def lconf_dict_to_lconf(in_dict, section_name, onelinelists=True, skip_none_value=True):
   """ Return a section_string from a `regular dictionary` or RDICT.

   - if the dict contains a: LCONF START-TAG it is used instead of the supplied section_name

   Known Limitations:
      - in_dict supports only minimal nesting

   Args:
      in_dict (obj): dictionary of section which will be converted to a LCONF-Section string
      section_name (str): section name: in normal cases a json will not have such
      onelinelists (bool): defines how list items are emitted

         - if True list items are dumped on the same line as the key separated by ` :: ` in an comma separated list
            - KEY1 :: [listitem1,listitem2]
         - if False list items are dumped on separate lines using indentation: EMPTY Lists are always dumped with Key :: []
            - KEY1
                 - listitem1
                 - listitem2

      skip_none_value(bool): if True: json: `null/python None` is transformed to a python empty string (value skipped) else it is transformed to python None

   Returns:
      str: a LCONF text string.

   Raises:
      LCONF.Err: if the conversion fails.
   """
   result = ['']

   # remove any '___END' TAG
   if SECTION_END_TAG in in_dict:
      del in_dict[SECTION_END_TAG]

   for key, item_value in in_dict.items():
      if key == SECTION_START_TAG:
         result[0] = '{} :: {}'.format(SECTION_START_TAG, item_value)
         continue

      if isinstance(item_value, list):
         if onelinelists or not item_value:
            temp_items = []
            for i_ in item_value:
               if isinstance(i_, dict) or isinstance(i_, list):
                  raise Err('_to_lconf_output_helper_checked', 'i_ may not be a list or a dict\n  <{}>'.format(i_))
               temp_items.append('%s' % i_)
            result.append('{} :: [{}]'.format(key, ','.join(temp_items)))
         else:
            result.append('{}'.format(key))
            for a_ in item_value:
               if isinstance(a_, dict) or isinstance(a_, list):
                  raise Err('_to_lconf_output_helper_checked', 'a_ may not be a list or a dict\n  <{}>'.format(a_))
               result.append('   {}'.format(a_))
      elif isinstance(item_value, dict):
         result.append('{}'.format(key))
         for mapping_key, mapping_value in item_value.items():
            # check not empty string and None, False
            if mapping_value:
               if isinstance(mapping_value, dict) or isinstance(mapping_value, list):
                  raise Err('_to_lconf_output_helper_checked', 'mapping_value may not be a list or a dict\n  <{}>'.format(mapping_value))
               result.append('   {} :: {}'.format(mapping_key, mapping_value))
            # Empty string
            elif isinstance(mapping_value, str):
               result.append('   {} ::'.format(mapping_key))
            elif skip_none_value and mapping_value is None:
               result.append('   {} ::'.format(mapping_key))
            else:
               result.append('   {} :: {}'.format(mapping_key, mapping_value))
      else:
         # check not empty string and None, False
         if item_value:
            result.append('{} :: {}'.format(key, item_value))
         # Empty string
         elif isinstance(item_value, str):
            result.append('{} ::'.format(key))
         elif skip_none_value and item_value is None:
            result.append('{} ::'.format(key))
         else:
            result.append('{} :: {}'.format(key, item_value))

   if result[0] == '':
      result[0] = '{} :: {}'.format(SECTION_START_TAG, section_name)
   result.append(SECTION_END_TAG)
   return '\n'.join(result)
