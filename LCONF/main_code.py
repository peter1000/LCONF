"""
===============
LCONF.main_code
===============

Overview
========
This module is the main `LCONF` code module


Constants
=========

.. py:data:: LCONF_BASE_INDENT

    (int) the lconf base indentation (number of spaces for one indentation level)

   .. important:: This **MUST** be kept at 3


.. py:data:: SECTION_START_TAG

    (str) `___SECTION` The Lconf-Section Start TAG

.. py:data:: SECTION_END_TAG

    (str) `___END` The Lconf-Section End TAG

.. py:data:: LCONF_NO

    (int) used for arguments instead of a bool if there are more options than 2

.. py:data:: LCONF_YES

    (int) used for arguments instead of a bool if there are more options than 2

.. py:data:: LCONF_DEFAULT

    (int) used for arguments instead of a bool if there are more options than 2


Functions
=========
.. autofunction:: lconf_extract_all_sections
.. autofunction:: lconf_extract_one_section_by_name
.. autofunction:: lconf_section_splitlines
.. autofunction:: lconf_validate_one_section_str
.. autofunction:: lconf_validate_source
.. autofunction:: lconf_validate_file
.. autofunction:: lconf_prepare_default_obj
.. autofunction:: lconf_prepare_and_parse_section
.. autofunction:: lconf_prepare_and_parse_section_lines
.. autofunction:: lconf_parse_section_lines
.. autofunction:: lconf_parse_section
.. autofunction:: lconf_parse_section_extract_by_name
.. autofunction:: lconf_emit
.. autofunction:: lconf_emit_default_obj
.. autofunction:: lconf_dict_to_lconf
.. autofunction:: lconf_to_ordered_native_type
.. autofunction:: lconf_to_native_type

"""
from collections import OrderedDict
import copy
from datetime import datetime
from os.path import isfile as path_isfile

from LCONF.lconf_structure_classes import (
   Blk,
   BlkI,
   KVList,
   KVMap,
   ListOT
)
from LCONF.lconf_classes import (
   LconfBlk,
   LconfBlkI,
   LconfKVList,
   LconfKVMap,
   LconfRoot,
   LconfListOT
)
from LCONF.utils import Err


LCONF_BASE_INDENT = 3
SECTION_START_TAG = '___SECTION'
SECTION_END_TAG = '___END'

LCONF_NO = 0
LCONF_YES = 1
LCONF_DEFAULT = -1


def lconf_extract_all_sections(source):
   """ Extracts all LCONF-Sections from the raw string.

   :param source: (raw str) which contains one or more LCONF-Sections
   :return: (list) of LCONF-Sections text each inclusive the ___SECTION, ___END TAG
      these are not split by line but each in one txt

   :raise Err: project error
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
               raise Err('lconf_extract_all_sections', [
                  'END_TAG_NOT_FOUND: expected <{}> Search text was: main_text_source[from_here_idx:] '.format(
                     SECTION_END_TAG
                  ),
                  '',
                  '',
                  '{}'.format(main_text_source[from_here_idx:])
               ])
            # add doc
            end_idx_with_tag = from_here_idx + end_idx + len_section_end_tag
            tmp_section_txt = main_text_source[from_here_idx:end_idx_with_tag]
            if SECTION_START_TAG in tmp_section_txt[len_section_start_tag:]:
               raise Err('lconf_extract_all_sections', [
                  'START-TAG FOUND within LCONF-Section. Section text:',
                  '',
                  '',
                  '==================',
                  '{}'.format(tmp_section_txt),
                  '',
                  '==================',
                  ''
               ])
            lconf_sections.append(main_text_source[from_here_idx:end_idx_with_tag])
            search_for_start = True
            from_here_idx = end_idx_with_tag
   else:
      if SECTION_END_TAG in main_text_source[:-len_section_end_tag]:
         raise Err('lconf_extract_all_sections', [
            'END-TAG FOUND within LCONF-Section. Section text:',
            '',
            '',
            '==================',
            '{}'.format(main_text_source),
            '',
            '==================',
            ''
         ])
      lconf_sections.append(main_text_source)
   return lconf_sections


def lconf_extract_one_section_by_name(source, section_name):
   """ Extracts one LCONF-Sections from the raw string.

   This will immediately return if the given section is found and not scan the whole source

   :param source: (raw str) which contains one or more LCONF-Sections
   :param section_name: (str) section name: which one wants to extract from the `source`
   :return: (str) Extracted LCONF-Sections text inclusive the ___SECTION, ___END TAG
      these are not split by line but all in one txt
   :raise Err: project error e.g: if a section with `section_name` is not found
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
      raise Err('lconf_extract_one_section_by_name', [
         'No Section with section_name: <{}> was found in the source:'.format(section_name),
         '',
         '<{}>'.format(source)
      ])
   return main_text_source


def lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False):
   """ Split a section raw string into lines and validate the first line

   :param lconf_section_raw_str: (raw str) which contains one LCONF-Section
   :param validate_first_line: (bool) if true the first line is validated
   :return: (tuple) section_lines, section_name
   :raise Err:
   """
   section_lines = lconf_section_raw_str.splitlines()
   first_line = section_lines[0]

   if validate_first_line:
      # FIRST LINE: special
      if first_line[-1] == ' ':
         raise Err('lconf_section_splitlines', [
            'TRAILING SPACE ERROR: LineNumber: <1>',
            '',
            '<{}>'.format(first_line)
         ])
      elif not first_line.startswith('{} :: '.format(SECTION_START_TAG)):
         raise Err('lconf_section_splitlines', [
            'FIRST LINE ERROR: Must start with <{} :: > LineNumber: <1>'.format(SECTION_START_TAG),
            '',
            '    <{}>'.format(first_line)
         ])
      elif first_line[len(SECTION_START_TAG) + 4] == ' ':
         raise Err('lconf_section_splitlines', [
            'TOO MANY SPACES around < :: > ERROR: LineNumber: <1>',
            '',
            '<{}>'.format(first_line)
         ])
      not_needed_start_tag, section_name = first_line.split(' :: ', 1)
   else:
      not_needed_start_tag, section_name = first_line.split(' :: ', 1)
   return section_lines, section_name


def lconf_validate_one_section_str(lconf_section_raw_str):
   """ Validates one LCONF-Section raw string: the section must be already correctly extracted

   .. warning:: **does not validate**

      This does not validate correct names for Keys, Repeated Block Identifiers ect.. as implemented in the corresponding
      :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>`

      It does also not validate for unique keys: :ref:`Restrictions: Unique names <restrictions_unique_names>`

   Validates/Checks for:

      - No Trailing Spaces
      - Most Indentation Errors: inclusive indent of Comment lines

      - correct `Key :: Value Separators` :ref:` <key_value_separator>`

      - number of other related checks like correct:

         - :ref:`List Identifier <list_identifier>`
         - :ref:`Key-Value-Mapping Identifier <key_value_mapping_identifier>`
         - :ref:`Repeated-Block Identifier <repeated_block_identifier>`

   :param lconf_section_raw_str: raw str) which contains one extracted LCONF-Sections inclusive the Start/End Tags
   :return: (bool) True if success else raises an error
   :raise Err:
   """
   is_key_value_mapping = 'is_key_value_mapping'
   is_kvlist = 'is_kvlist'
   is_list_of_tuples = 'is_list_of_tuples'
   is_blk = 'is_blk'
   is_blk_name = 'is_blk_name'
   is_root = 'is_root'

   list_of_tuples_expected_commas = -1

   # splitlines / validate_first_line
   section_lines = lconf_section_raw_str.splitlines()
   first_line = section_lines[0]
   if first_line[-1] == ' ':
      raise Err('lconf_validate_one_section_str_new', [
         'TRAILING SPACE ERROR: LineNumber: <1>',
         '    <{}>'.format(first_line)
      ])
   elif not first_line.startswith('{} :: '.format(SECTION_START_TAG)):
      raise Err('lconf_validate_one_section_str_new', [
         'FIRST LINE ERROR: Must start with <{} :: > LineNumber: <1>'.format(SECTION_START_TAG),
         '    <{}>'.format(first_line)
      ])
   elif first_line[len(SECTION_START_TAG) + 4] == ' ':
      raise Err('lconf_validate_one_section_str_new', [
         'TOO MANY SPACES around < :: > ERROR: LineNumber: <1>',
         '    <{}>'.format(first_line)
      ])
   not_needed_start_tag, section_name = first_line.split(' :: ', 1)

   prev_indent = 0
   check_indent = 0
   stack = ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK']
   len_stack = 10
   cur_stack_idx = -1
   stack_situation = is_root
   next_idx = 0

   # Validate END-TAG (last line) has no indent
   if section_lines[-1] != SECTION_END_TAG:
      raise Err('lconf_validate_one_section_str_new', [
         'SectionName: {}'.format(section_name),
         'END-TAG LINE ERROR: EXPECTED: <{}>'.format(SECTION_END_TAG),
         '    LineNumber: <{}>'.format(len(section_lines)),
         '      <{}>'.format(section_lines[len(section_lines) - 1])
      ])

   prepared_lines = [(orig_line, len(orig_line) - len(orig_line.lstrip())) for orig_line in section_lines[1:] if orig_line]

   len_prepared_lines = len(prepared_lines)

   for orig_line, cur_indent in prepared_lines:
      next_idx += 1
      if next_idx < len_prepared_lines:
         if orig_line[-1] == ' ':
            raise Err('lconf_validate_one_section_str_new', [
               'SectionName: {}'.format(section_name),
               'TRAILING SPACE ERROR:',
               '<{}>'.format(orig_line)
            ])
         # CHECK NESTED STACK
         if cur_stack_idx >= 0:
            if cur_indent > check_indent:
               if cur_indent != (check_indent + LCONF_BASE_INDENT):
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'INDENTATION LEVEL WRONG ERROR:',
                     '  <{}>'.format(orig_line),
                     '    prev_indent: <{}> check indent: <{}> - current indent: <{}>'.format(
                        prev_indent,
                        check_indent,
                        cur_indent
                     ),
                     '    Maximum expected indent: <{}> !! Indentation must be a multiple of <3>'.format(
                        check_indent + LCONF_BASE_INDENT
                     )
                  ])
            # Current Indent same or less than: check_indent
            else:
               if (cur_indent % 3) != 0:
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'INDENTATION LEVEL WRONG DECREASED ERROR:',
                     '  <{}>'.format(orig_line),
                     '    previous indent: <{}> - current indent: <{}> !! Indentation must be a multiple of <3>'.format(
                        prev_indent,
                        cur_indent
                     )
                  ])
               check_idx = int(cur_indent / 3)
               if check_idx == 0:
                  stack = ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK']
                  len_stack = 10
                  cur_stack_idx = -1
                  stack_situation = is_root
                  check_indent = 0
               else:
                  cur_stack_idx = check_idx - 1
                  stack_situation = stack[cur_stack_idx]
         else:
            if orig_line[0] == ' ':
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'INDENTATION ROOT/MAIN LINE ERROR:',
                  '  <{}>'.format(orig_line),
                  '    cur_indent: <{}>'.format(cur_indent),
                  '      But for `ROOT/MAIN lines` we expect no indent: <0> spaces'
               ])
            cur_indent = 0
            check_indent = cur_indent
            cur_stack_idx = -1

         # PROCESS ALL
         if orig_line[cur_indent] == '#':
            # check next line indent
            next_section_line, next_section_line_indent = prepared_lines[next_idx]
            if next_section_line_indent == cur_indent:
               continue
            else:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'INDENTATION COMMENT LINE ERROR:',
                  '  <{}>'.format(orig_line),
                  '    Current Comment Line indent: <{}> spaces'.format(cur_indent),
                  '      must be the same as the `next none empty line` indent: <{}>'.format(next_section_line_indent),
                  '      !! Indentation must also be a multiple of <3>',
                  '        next_line: <{}>'.format(next_section_line)
               ])

         orig_stack_situation = stack_situation

         # ====  ==== ==== continue orig_stack_situation ====  ==== ====   #
         # `Key-Value-List`
         if orig_stack_situation == is_kvlist:
            # may not contain as items: `Blk-Identifier`, or `Key :: Value Separator` or any other `Lists`
            if orig_line[cur_indent] == '*' or orig_line[cur_indent] == '-' or '::' in orig_line:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  '`Key-Value-List` WRONG ITEM ERROR:',
                  '  <{}>'.format(orig_line),
                  '    orig_stack_situation: <{}>'.format(orig_stack_situation),
                  '      `Lists` may not contain: `Blk-Identifier`, other `Lists-Identifier` or `Key :: Value Separator`'
               ])

         # `List-Of-Tuples`
         elif orig_stack_situation == is_list_of_tuples:
            # may not contain as items: `Blk-Identifier`, or `Key :: Value Separator` or any other `Lists`
            if orig_line[cur_indent] == '*' or orig_line[cur_indent] == '-' or '::' in orig_line:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  '`List-Of-Tuples` WRONG ITEM ERROR:',
                  '  <{}>'.format(orig_line),
                  '    orig_stack_situation: <{}>'.format(orig_stack_situation),
                  '      `Lists` may not contain: `Blk-Identifier`, other `Lists-Identifier` or `Key :: Value Separator`'
               ])

            # Item Lines must contain at least list_of_lists_expected_commas
            if orig_line.count(',') != list_of_tuples_expected_commas:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'List-Of-Tuples ITEM Line ERROR:',
                  '  <{}>'.format(orig_line),
                  '    orig_stack_situation: <{}>'.format(orig_stack_situation),
                  '      Number of expected `commas`: <{}>. Counted `commas`: <{}>'.format(
                     list_of_tuples_expected_commas,
                     orig_line.count(',')
                  )
               ])

         # Blk-Identifier may only contain single indented values: Block names
         elif orig_stack_situation == is_blk:
            if orig_line[cur_indent] == '*' or orig_line[cur_indent] == '-' or '::' in orig_line:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'WRONG TYPE ERROR:',
                  '  <{}>'.format(orig_line),
                  '    orig_stack_situation: <{}>'.format(orig_stack_situation),
                  '      `Blk-Identifier` may not contain other: `Blk-Identifier`, `Lists` or `Key :: Value Pairs`'
               ])

            # Check Empty one blk_name
            next_section_line, next_section_line_indent = prepared_lines[next_idx]
            if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
               stack_situation = is_blk_name
               check_indent = cur_indent
               cur_stack_idx += 1
               stack[cur_stack_idx] = stack_situation
               if cur_stack_idx > len_stack - 3:
                  stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                  len_stack += 10
                  # else: EMPTY BLK-NAME:  No need to adjust the stack for this

         # Key-Value-Mapping: no need to do anything here: orig_stack_situation == is_key_value_mapping

         # Block-Name: check any new situation: no need to do anything here: orig_stack_situation == is_blk_name

         # Root: check any new situation: no need to do anything here: orig_stack_situation == is_root

         # ====  ==== ==== check new orig_stack_situation ====  ==== ====   #
         else:
            # `Key-Value-List` / Key :: Value-Lists / `List-Of-Tuples` Identifier
            if orig_line[cur_indent] == '-':
               if orig_line[cur_indent + 1] != ' ' or orig_line[cur_indent + 2] == ' ':
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'LIST IDENTIFIER ERROR:',
                     '  <{}>'.format(orig_line),
                     '    There must be ONE SPACE after the `minus`. Expected `minus, one space`.'
                  ])
               # `Key :: Value-Lists`
               if '::' in orig_line:
                  # Validate: Key Value separator:  No need to adjust the stack for this
                  if '  ::' in orig_line or '::  ' in orig_line or (' :: ' not in orig_line and orig_line[-3:] != ' ::'):
                     raise Err('lconf_validate_one_section_str_new', [
                        'SectionName: {}'.format(section_name),
                        'KEY-VALUE-SEPARATOR < :: > ERROR:',
                        '  <{}>'.format(orig_line)
                     ])
               # Check `List-Of-Tuples`
               elif orig_line[-1] == '|':
                  # Check Empty one
                  next_section_line, next_section_line_indent = prepared_lines[next_idx]
                  if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                     check_indent = cur_indent
                     stack_situation = is_list_of_tuples
                     cur_stack_idx += 1
                     stack[cur_stack_idx] = stack_situation
                     if cur_stack_idx > len_stack - 3:
                        stack.extend(
                           ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                        len_stack += 10
                  # else: EMPTY List-Of-Tuples:  No need to adjust the stack for this

                  # list_of_lists_num_items
                  list_of_tuples_expected_commas = orig_line.count(
                     '|') - 2  # the leading and ending pipe is not expected as a comma

               # `Key-Value-List`
               else:
                  # Check Empty one
                  next_section_line, next_section_line_indent = prepared_lines[next_idx]
                  if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                     check_indent = cur_indent
                     stack_situation = is_kvlist
                     cur_stack_idx += 1
                     stack[cur_stack_idx] = stack_situation
                     if cur_stack_idx > len_stack - 3:
                        stack.extend(
                           ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                        len_stack += 10
                        # else: EMPTY `Key-Value-List`:  No need to adjust the stack for this

            # `Key-Value-Mapping Identifier`
            elif orig_line[cur_indent] == '.':
               if orig_line[cur_indent + 1] != ' ' or orig_line[cur_indent + 2] == ' ':
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'Key-Value-Mapping IDENTIFIER ERROR:',
                     '  <{}>'.format(orig_line),
                     '    There must be ONE SPACE after the `dot`. Expected `dot, one space`.'
                  ])
               # Check Empty one
               next_section_line, next_section_line_indent = prepared_lines[next_idx]
               if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                  stack_situation = is_key_value_mapping
                  check_indent = cur_indent
                  cur_stack_idx += 1
                  stack[cur_stack_idx] = stack_situation
                  if cur_stack_idx > len_stack - 3:
                     stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                     len_stack += 10
                     # else: EMPTY `Key-Value-Mapping Identifier`:  No need to adjust the stack for this

            # `BLOCK Identifier`
            elif orig_line[cur_indent] == '*':
               if orig_line[cur_indent + 1] != ' ' or orig_line[cur_indent + 2] == ' ':
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'BLOCK IDENTIFIER ERROR:',
                     '  <{}>'.format(orig_line),
                     '    There must be ONE SPACE after the `asterisk`. Expected `asterisk, one space`.'
                  ])
               # Check Empty one
               next_section_line, next_section_line_indent = prepared_lines[next_idx]
               if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                  stack_situation = is_blk
                  check_indent = cur_indent
                  cur_stack_idx += 1
                  stack[cur_stack_idx] = stack_situation
                  if cur_stack_idx > len_stack - 3:
                     stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                     len_stack += 10
                     # else: EMPTY `BLOCK Identifier`:  No need to adjust the stack for this

            # `Key :: Value Pair`:  we checked already for: Key :: Value-Lists
            elif '::' in orig_line:
               if '  ::' in orig_line or '::  ' in orig_line or (' :: ' not in orig_line and orig_line[-3:] != ' ::'):
                  raise Err('lconf_validate_one_section_str_new', [
                     'SectionName: {}'.format(section_name),
                     'KEY-VALUE-SEPARATOR < :: > ERROR:',
                     '  <{}>'.format(orig_line)
                  ])

            # SOMETHING WRONG SHOULD NEVER REACH THIS
            else:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'SOMETHING WRONG SHOULD NEVER REACH THIS: ERROR',
                  '  Maybe a missing `List, Mapping or Block Identifier` but could be anything else.',
                  '    <{}>'.format(orig_line)
               ])
         prev_indent = cur_indent
   return True


def lconf_validate_source(lconf_source):
   """ Validates a LCONF-Section raw string containing one or more LCONF-Sections
   This does not validate with the corresponding Section-Template classes: like correct names for: Keys, Repeated Block
   Identifiers ect..

   IMPORTANT NOTE: this uses the function: lconf_extract_all_sections() to extract valid LCONF-Sections. If a code extracts
   sections in an other way the first/last line might differ

   Validates/Checks for:
      - No Trailing Spaces
      - Most Indentation Errors: inclusive indent of Comment lines
      - if a line is a Key/Value separator line: :
         - only one space before and one space after the double colon
            - for empty string values no space after the double colon
         - MISSING characters after <::>
         - WRONG CHAR/SPACES after <::>
         - WRONG CHAR/SPACES before <::>

   :param lconf_source: (raw str) which contains one or more LCONF-Sections
   :return: (bool) True if success else raises an error
   """
   for section_lconf_source in lconf_extract_all_sections(lconf_source):
      lconf_validate_one_section_str(section_lconf_source)
   return True


def lconf_validate_file(path_to_lconf_file):
   """ Validates a file containing one or more LCONF-Sections
   This does not validate with the corresponding Section-Template classes: like correct names for: Keys, Repeated Block
   Identifiers ect..

   IMPORTANT NOTE: this uses the function: lconf_extract_all_sections() to extract valid LCONF-Sections. If code extracts
   sections in an other way the first/last line might differ

   Validates/Checks for:
      - No Trailing Spaces
      - Most Indentation Errors
      - if a line is a Key/Value separator line
         - only one space before and one space after the double colon
         - for empty string values no space after the double colon
         - MISSING characters after <::>
         - WRONG CHAR/SPACES after <::>
         - WRONG CHAR/SPACES before <::>

   :param path_to_lconf_file: (str) path to a file
   :return: (bool) True if success else raises an error
   :raise Err:
   """
   if not path_isfile(path_to_lconf_file):
      raise Err('lconf_validate_file', [
         'Input path seems not to be a file:'
         '   <{}>'.format(path_to_lconf_file)
      ])

   print('\n\n====== VALIDATING SECTIONS IN FILE:\n   <{}>'.format(path_to_lconf_file))
   with open(path_to_lconf_file, 'r') as file_:
      for section_lconf_source in lconf_extract_all_sections(file_.read()):
         lconf_validate_one_section_str(section_lconf_source)
   return True


def _prepare_default_obj__with_comments(input_obj):
   """ Helper: to make a recursively copy of the lconf_section__template_obj: with the same `key_order` and keeping any
   `Default-Comment/Empty Lines`

   - only supports: Root/KVMap/Blk recursively
   - KVList/ListOT: return a new obj of themselves
   - BlkI: are 'empty' without any `Block-Name`
   - str, bool, int, float, datetime are only returned
   - all others are normal copy.copy

   - No `extra_data` is copied

   - The values tuples are overwritten with the default value: the transform function info is skipped

   .. note:: Dummy-Blocks are not prepared by default but the function must be called separately with the dummy-blk obj

   :param input_obj: (obj) instance of main section template object (or sub parts of it) which has all the info: inclusive
      any `transform func`

   :return: (obj) adjusted/prepared copy of the lconf_section__template_obj
   """
   if input_obj.__class__ is str:
      return input_obj
   elif input_obj.__class__ in {bool, int, float}:
      return input_obj
   elif input_obj.__class__ is KVMap:
      return LconfKVMap({key: _prepare_default_obj__with_comments(input_obj[key][0]) for key in input_obj.key_order},
         input_obj.key_order)
   elif input_obj.__class__ is KVList:
      return LconfKVList(input_obj, input_obj.use_oneline)
   elif input_obj.__class__ is Blk:
      return LconfBlk({key: _prepare_default_obj__with_comments(input_obj[key][0]) for key in input_obj.key_order},
         input_obj.key_order)
   elif input_obj.__class__ is BlkI:
      # Note: the `input_obj['dummy_blk']` blk is prepared each time anew when it gets parsed: seems to be faster
      # INIT without any Block-Names
      data = {}
      block_names_list = []
      temp_obj = LconfBlkI(data, block_names_list, input_obj.min_required_blocks, input_obj.max_allowed_blocks)
      temp_obj.set_class__dict__item('has_comments', True)
      return temp_obj
   elif input_obj.__class__ is ListOT:
      return LconfListOT(input_obj, input_obj.column_names, input_obj.column_names_idx_lookup,
         input_obj.column_names_counted, input_obj.column_replace_missing)
   # the ones which are not so often expected
   elif input_obj.__class__ is datetime:
      return input_obj
   else:
      return copy.copy(input_obj)


def _prepare_default_obj__no_comments(input_obj):
   """ Helper: to make a recursively copy of the lconf_section__template_obj: with the same `key_order` but without any
   `Default-Comment/Empty Lines`

   - only supports: Root/KVMap/Blk recursively
   - KVList/ListOT: return a new obj of themselves
   - BlkI: are 'empty' without any `Block-Name`
   - str, bool, int, float, datetime are only returned
   - all others are normal copy.copy

   - No `extra_data` is copied

   - The values tuples are overwritten with the default value: the transform function info is skipped

   .. note:: Dummy-Blocks are not prepared by default but the function must be called separately with the dummy-blk obj

   :param input_obj: (obj) instance of main section template object (or sub parts of it) which has all the info: inclusive
      any `transform func`

   :return: (obj) adjusted/prepared copy of the lconf_section__template_obj
   """
   if input_obj.__class__ is str:
      return input_obj
   elif input_obj.__class__ in {bool, int, float}:
      return input_obj
   elif input_obj.__class__ is KVMap:
      return LconfKVMap(
         {key: _prepare_default_obj__no_comments(input_obj[key][0]) for key in input_obj.key_order_no_comments},
         input_obj.key_order_no_comments)
   elif input_obj.__class__ is KVList:
      return LconfKVList(input_obj, input_obj.use_oneline)
   elif input_obj.__class__ is Blk:
      return LconfBlk({key: _prepare_default_obj__no_comments(input_obj[key][0]) for key in input_obj.key_order_no_comments},
         input_obj.key_order_no_comments)
   elif input_obj.__class__ is BlkI:
      # Note: the `input_obj['dummy_blk']` blk is prepared each time anew when it gets parsed: seems to be faster
      # INIT without any Block-Names
      data = {}
      block_names_list = []
      temp_obj = LconfBlkI(data, block_names_list, input_obj.min_required_blocks, input_obj.max_allowed_blocks)
      temp_obj.set_class__dict__item('has_comments', False)
      return temp_obj
   elif input_obj.__class__ is ListOT:
      return LconfListOT(input_obj, input_obj.column_names, input_obj.column_names_idx_lookup,
         input_obj.column_names_counted, input_obj.column_replace_missing)
   # the ones which are not so often expected
   elif input_obj.__class__ is datetime:
      return input_obj
   else:
      return copy.copy(input_obj)


def lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False):
   """ Returns a recursively copy of the lconf_section__template_obj: with the same `key_order` but without
   `Default Comment/Empty Line`

   .. seealso:: _prepare_default_obj__with_comments(), _prepare_default_obj__no_comments()

   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info: inclusive any
      `l_transform func` type-conversion

   :param with_comments: (bool) option to parse also any defined: default empty or comment line

         - if True: any `Default-Comment/Empty Lines` are parse
         - if False: any `Default-Comment/Empty Lines`` are not parse

   :return: (lconf_default_obj obj) prepared copy of the lconf_section__template_obj
   """
   if with_comments:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__with_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order}, lconf_section__template_obj.key_order)
      lconf_default_obj.set_class__dict__item('has_comments', True)
   else:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__no_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order_no_comments}, lconf_section__template_obj.key_order_no_comments)
      lconf_default_obj.set_class__dict__item('has_comments', False)
   return lconf_default_obj


def lconf_prepare_and_parse_section(lconf_section_raw_str, lconf_section__template_obj, with_comments=False, validate=False):
   """ Returns a new parsed lconf obj. Basically it does lconf_prepare_default_obj() and lconf_parse_section

   :param lconf_section_raw_str: (raw str) which contains one LCONF-Section
   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info
   :param with_comments: (bool) option to parse also any defined: default empty or comment line

         - if True: any `Default-Comment/Empty Lines` are parse
         - if False: any `Default-Comment/Empty Lines`` are not parse

   :param validate: (bool)

         - if True the `lconf_section_raw_str` is first validated and only afterwards parsed
         - if False: no validation is done

   :return: (obj) copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally updated: attributes

         - section_name: updated with the LCONF-SectionName
         - is_parsed: set to True; so one can know if this obj was already parsed

   """
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   # Prepare
   if with_comments:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__with_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order}, lconf_section__template_obj.key_order)
      lconf_default_obj.set_class__dict__item('has_comments', True)
   else:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__no_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order_no_comments}, lconf_section__template_obj.key_order_no_comments)
      lconf_default_obj.set_class__dict__item('has_comments', False)
   # Parse
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_prepare_and_parse_section_lines(section_lines, section_name, lconf_section__template_obj, with_comments=False):
   """ Returns a new parsed lconf obj. Basically it does lconf_prepare_default_obj() and lconf_parse_section_lines()

   :param section_lines: (list) which contains one LCONF-Section raw string already split into lines
   :param section_name: (str) already extracted section name
   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info: inclusive any
      `l_transform`
   :param with_comments: (bool) option to parse also any defined: default empty or comment line

         - if True: any `Default-Comment/Empty Lines` are parse
         - if False: any `Default-Comment/Empty Lines`` are not parse

   :return: (obj) copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally updated: attributes

         - section_name: updated with the LCONF-SectionName
         - is_parsed: set to True; so one can know if this obj was already parsed

   """
   if with_comments:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__with_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order}, lconf_section__template_obj.key_order)
      lconf_default_obj.set_class__dict__item('has_comments', True)
   else:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__no_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order_no_comments}, lconf_section__template_obj.key_order_no_comments)
      lconf_default_obj.set_class__dict__item('has_comments', False)
   # Parse parse_section_lines
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def _check_correct_number_of_blocks(input_obj):
   """ Helper: to check recursively if the parsed lconf object's `Repeated-Blocks

   :param input_obj: (obj) instance of parsed lconf object (or sub parts of it)
   """
   if input_obj.__class__ is LconfBlkI:
      number_of_blks = len(input_obj.key_order)
      if input_obj.min_required_blocks > 0:
         if number_of_blks < input_obj.min_required_blocks:
            raise Err('_check_correct_number_of_blocks', [
               'WRONG NUMBER OF BLOCK-NAMES ERROR:',
               'number_of_blks: {} min_required_blocks: <{}>'.format(number_of_blks, input_obj.min_required_blocks),
               '  BLK NAMES: <{}>'.format(input_obj.key_order)
            ])
      if input_obj.max_allowed_blocks > 0:
         if number_of_blks > input_obj.max_allowed_blocks:
            raise Err('_check_correct_number_of_blocks', [
               'WRONG NUMBER OF BLOCK-NAMES ERROR:',
               'number_of_blks: {} max_allowed_blocks: <{}>'.format(number_of_blks, input_obj.max_allowed_blocks),
               '  BLK NAMES: <{}>'.format(input_obj.key_order)
            ])
   elif input_obj.__class__ in {LconfKVMap, LconfBlk}:
      _check_correct_number_of_blocks([input_obj[key] for key in input_obj.key_order])
      # else: nothing to do


# noinspection PyCallingNonCallable
def lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj):
   """ Parses a LCONF-Section raw string already split into lines and updates the section object

   .. seealso:: :py:meth:`lconf_extract_all_sections`

   .. note:: Does not validate the section_lines for correct LCONF: e.g. indentation

   :param lconf_default_obj: (obj) a prepared copy of lconf_section__template_obj: see function: lconf_prepare_default_obj()
   :param section_lines: (list) which contains one LCONF-Section raw string already split into lines
   :param section_name: (str) already extracted section name
   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info: inclusive any
      `l_transform`
   :return: (obj) updated lconf_default_obj attributes updated by the data in section_lines

      - additionally updated: attributes

         - section_name: updated with the LCONF-SectionName
         - is_parsed: set to True; so one can know if this obj was already parsed

   :raise Err:

   .. todo:: maybe try to speed up `checking correct number of blocks` without looping through all again

   """
   lconf_default_obj.set_class__dict__item('section_name', section_name)
   is_key_value_mapping = 'is_key_value_mapping'
   is_kvlist = 'is_kvlist'
   is_list_of_tuples = 'is_list_of_tuples'
   is_blk = 'is_blk'
   is_blk_name = 'is_blk_name'
   is_root = 'is_root'

   check_indent = 0
   stack = ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK']
   len_stack = 10
   cur_stack_idx = -1
   stack_situation = is_root
   next_idx = 0

   cur_adjust_obj = lconf_default_obj
   cur_template_obj = lconf_section__template_obj
   cur_transform_func = None

   del section_lines[0]    # This is faster than making a slice copy: section_lines[1:]

   prepared_lines = [
      # FORMAT:  orig_line, cur_indent, line_no_cur_indent
      (orig_line, 0, orig_line) if orig_line[0] != ' ' else
      (orig_line, 3, orig_line[3:]) if orig_line[3] != ' ' else
      (orig_line, 6, orig_line[6:]) if orig_line[6] != ' ' else
      (orig_line, 9, orig_line[9:]) if orig_line[9] != ' ' else
      (orig_line, 12, orig_line[12:]) if orig_line[12] != ' ' else
      (orig_line, 15, orig_line[15:]) if orig_line[15] != ' ' else
      (orig_line, 18, orig_line[18:]) if orig_line[18] != ' ' else
      (orig_line, 21, orig_line[21:]) if orig_line[21] != ' ' else
      (orig_line, len(orig_line) - len(orig_line.lstrip()), orig_line[len(orig_line) - len(orig_line.lstrip())])
      for orig_line in section_lines if orig_line
   ]

   len_prepared_lines = len(prepared_lines)
   for orig_line, cur_indent, line_no_indent in prepared_lines:
      # Get once the first/last char as we need it a couple of times
      first_char_cur_line = line_no_indent[0]
      last_char_cur_line = line_no_indent[-1]
      # What if there was an empty line with only whitespace:
      # no need to check for line_no_indent better check the last_char_cur_line which does much more
      if last_char_cur_line == ' ':
         raise Err('lconf_parse_section_lines', [
            'SectionName: {}'.format(section_name),
            'TRAILING SPACE ERROR:',
            '  <{}>'.format(orig_line)
         ])
      next_idx += 1

      if next_idx < len_prepared_lines:
         # CHECK NESTED STACK
         if cur_stack_idx >= 0:
            # Current Indent same or less than: check_indent
            if cur_indent <= check_indent:
               check_idx = int(cur_indent / 3)
               if check_idx == 0:
                  stack = ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK']
                  len_stack = 10
                  cur_stack_idx = -1
                  stack_situation = is_root
                  cur_adjust_obj = lconf_default_obj
                  cur_template_obj = lconf_section__template_obj
                  check_indent = 0
               else:
                  cur_stack_idx = check_idx - 1
                  stack_situation, cur_adjust_obj, cur_template_obj = stack[cur_stack_idx]
         else:
            cur_indent = 0
            cur_adjust_obj = lconf_default_obj
            cur_template_obj = lconf_section__template_obj
            check_indent = 0
            cur_stack_idx = -1

         # PROCESS ALL

         if first_char_cur_line == '#':
            # check next line indent
            next_section_line, next_section_line_indent, next_line_no_indent = prepared_lines[next_idx]
            if next_section_line_indent == cur_indent:
               continue
            else:
               raise Err('lconf_parse_section_lines', [
                  'SectionName: {}'.format(section_name),
                  'INDENTATION COMMENT LINE ERROR:',
                  '  <{}>'.format(orig_line),
                  '    Current Comment Line indent: <{}> spaces'.format(cur_indent),
                  '      must be the same as the `next none empty line` indent: <{}>'.format(next_section_line_indent),
                  '      !! Indentation must also be a multiple of <3>',
                  '        next_line: <{}>'.format(next_section_line)
               ])

         orig_stack_situation = stack_situation

         # ====  ==== ==== continue orig_stack_situation ====  ==== ====   #
         # `Key-Value-List` ITEMS
         if orig_stack_situation == is_kvlist:
            if cur_transform_func:
               cur_adjust_obj.append(cur_transform_func(line_no_indent, orig_line))
            else:
               cur_adjust_obj.append(line_no_indent)

         # `List-Of-Tuples` ITEM ROWS
         elif orig_stack_situation == is_list_of_tuples:
            # CHECK: `Empty/Missing Values` Replacement
            if cur_adjust_obj.column_replace_missing:
               if cur_transform_func:
                  # Check if we use multiple ones
                  if cur_transform_func.__class__ is tuple:
                     temp_column_replace_missing = cur_adjust_obj.column_replace_missing
                     val_list = []
                     idx = 0
                     for orig_value in line_no_indent.split(','):
                        orig_value_stripped = orig_value.strip()
                        this_transform_func = cur_transform_func[idx]
                        if this_transform_func:
                           val_list.append(this_transform_func(orig_value_stripped,
                              orig_value) if orig_value_stripped else this_transform_func(temp_column_replace_missing[idx],
                              orig_value))
                        else:
                           val_list.append(orig_value_stripped if orig_value_stripped else temp_column_replace_missing[idx])
                        idx += 1
                     cur_adjust_obj.append(tuple(val_list))
                  # single transform function for all items
                  else:
                     temp_column_replace_missing = cur_adjust_obj.column_replace_missing
                     val_list = []
                     idx = 0
                     for orig_value in line_no_indent.split(','):
                        orig_value_stripped = orig_value.strip()
                        if cur_transform_func:
                           val_list.append(cur_transform_func(orig_value_stripped,
                              orig_value) if orig_value_stripped else cur_transform_func(temp_column_replace_missing[idx],
                              orig_value))
                        else:
                           val_list.append(orig_value_stripped if orig_value_stripped else temp_column_replace_missing[idx])
                        idx += 1
                     cur_adjust_obj.append(tuple(val_list))
               else:
                  temp_column_replace_missing = cur_adjust_obj.column_replace_missing
                  val_list = []
                  idx = 0
                  for orig_value in line_no_indent.split(','):
                     orig_value_stripped = orig_value.strip()
                     val_list.append(orig_value_stripped if orig_value_stripped else temp_column_replace_missing[idx])
                     idx += 1
                  cur_adjust_obj.append(tuple(val_list))
            # NO: `Empty/Missing Values` Replacement
            else:
               if cur_transform_func:
                  # Check if we use multiple ones
                  if cur_transform_func.__class__ is tuple:
                     val_list = []
                     idx = 0
                     for orig_value in line_no_indent.split(','):
                        orig_value_stripped = orig_value.strip()
                        this_transform_func = cur_transform_func[idx]
                        val_list.append(this_transform_func(orig_value_stripped,
                           orig_value) if orig_value_stripped and this_transform_func else orig_value_stripped)
                        idx += 1
                     cur_adjust_obj.append(tuple(val_list))
                  # single transform function for all items
                  else:
                     cur_adjust_obj.append(
                        tuple(
                           [cur_transform_func(orig_value.strip(), orig_value) for orig_value in line_no_indent.split(',')])
                     )
               else:
                  cur_adjust_obj.append(
                     tuple([orig_value.strip() for orig_value in line_no_indent.split(',')])
                  )

         # Blk-Identifier may only contain single indented values: Block names
         elif orig_stack_situation == is_blk:
            # Add the Block-Name: with a new _prepare_default_obj Block
            if cur_adjust_obj.has_comments:
               cur_adjust_obj[line_no_indent] = _prepare_default_obj__with_comments(cur_template_obj['dummy_blk'])
            else:
               cur_adjust_obj[line_no_indent] = _prepare_default_obj__no_comments(cur_template_obj['dummy_blk'])

            # Check NONE Empty one

            next_section_line, next_section_line_indent, next_line_no_indent = prepared_lines[next_idx]
            if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
               # Set the new: cur_adjust_obj/cur_template_obj
               cur_adjust_obj = cur_adjust_obj[line_no_indent]
               # Get the template Block
               cur_template_obj = cur_template_obj['dummy_blk']

               # ADD THE STACK
               check_indent = cur_indent
               stack_situation = is_blk_name
               cur_stack_idx += 1
               stack[cur_stack_idx] = (stack_situation, cur_adjust_obj, cur_template_obj)
               if cur_stack_idx > len_stack - 3:
                  stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                  len_stack += 10
                  # else: EMPTY BLK-NAME:  No need to adjust the stack for this

         # Key-Value-Mapping: check any new situation: no need to do anything here:
         # orig_stack_situation == is_key_value_mapping

         # Block-Name: check any new situation: no need to do anything here: orig_stack_situation == is_blk_name

         # Root: check any new situation: no need to do anything here: orig_stack_situation == is_root

         #  ====  ==== ==== check new orig_stack_situation ====  ==== ====   #
         else:
            # `Key-Value-List` / Key :: Value-Lists / `List-Of-Tuples` Identifier
            if first_char_cur_line == '-':
               corrected_line_no_indent = line_no_indent[2:]
               # `Key :: Value-List`
               if ' ::' in corrected_line_no_indent:
                  if ':: ' in corrected_line_no_indent:
                     name, value = corrected_line_no_indent.split(' :: ', 1)
                     use_oneline = cur_template_obj[name][0].use_oneline
                     # TRANSFORM CHECK: len more than 1
                     if len(cur_template_obj[name]) > 1:
                        cur_adjust_obj[name] = LconfKVList(
                           [cur_template_obj[name][1](temp_item, orig_line) for temp_item in value.split(',')], use_oneline)
                     else:
                        cur_adjust_obj[name] = LconfKVList(value.split(','), use_oneline)
                  # Empty
                  else:
                     temp_corrected_line_no_indent = corrected_line_no_indent[:-3]
                     use_oneline = cur_template_obj[temp_corrected_line_no_indent][0].use_oneline
                     cur_adjust_obj[temp_corrected_line_no_indent] = LconfKVList([], use_oneline)

               # Check `List-Of-Tuples`
               elif corrected_line_no_indent[-1] == '|':
                  # Get the name, column_names
                  name, column_names_not_used = corrected_line_no_indent.split(' |', 1)  # split also the space
                  # Do not change the main: cur_adjust_obj/cur_template_obj in case we have an empty List-Of-Tuples and do
                  #  not adjust the stack
                  this_template_obj = cur_template_obj[name][0]
                  column_names = this_template_obj.column_names
                  column_names_idx_lookup = this_template_obj.column_names_idx_lookup
                  column_names_counted = this_template_obj.column_names_counted
                  column_replace_missing = this_template_obj.column_replace_missing
                  cur_adjust_obj[name] = LconfListOT([], column_names, column_names_idx_lookup, column_names_counted,
                     column_replace_missing)
                  # Check NONE Empty one
                  next_section_line, next_section_line_indent, next_name = prepared_lines[next_idx]
                  if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                     # TRANSFORM CHECK: len more than 1
                     if len(cur_template_obj[name]) > 1:
                        cur_transform_func = cur_template_obj[name][1]
                     else:
                        cur_transform_func = None

                     # Set the new: cur_adjust_obj/cur_template_obj
                     cur_adjust_obj = cur_adjust_obj[name]
                     cur_template_obj = this_template_obj
                     # ADD THE STACK
                     check_indent = cur_indent
                     stack_situation = is_list_of_tuples
                     cur_stack_idx += 1
                     stack[cur_stack_idx] = (stack_situation, cur_adjust_obj, cur_template_obj)
                     if cur_stack_idx > len_stack - 3:
                        stack.extend(
                           ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                        len_stack += 10
                        # else: EMPTY List-Of-Tuples:  No need to adjust the stack for this

               # `Key-Value-List`
               else:
                  # Do not change the main: cur_adjust_obj/cur_template_obj in case we have an empty List-Of-Tuples and do
                  #  not adjust the stack
                  this_template_obj = cur_template_obj[corrected_line_no_indent][0]
                  use_oneline = this_template_obj.use_oneline
                  cur_adjust_obj[corrected_line_no_indent] = LconfKVList([], use_oneline)
                  # Check NONE Empty one
                  next_section_line, next_section_line_indent, next_line_no_indent = prepared_lines[next_idx]
                  if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                     # TRANSFORM CHECK: len more than 1
                     if len(cur_template_obj[corrected_line_no_indent]) > 1:
                        cur_transform_func = cur_template_obj[corrected_line_no_indent][1]
                     else:
                        cur_transform_func = None

                     # Set the new: cur_adjust_obj/cur_template_obj
                     cur_adjust_obj = cur_adjust_obj[corrected_line_no_indent]
                     cur_template_obj = this_template_obj
                     # ADD THE STACK
                     check_indent = cur_indent
                     stack_situation = is_kvlist
                     cur_stack_idx += 1
                     stack[cur_stack_idx] = (stack_situation, cur_adjust_obj, cur_template_obj)
                     if cur_stack_idx > len_stack - 3:
                        stack.extend(
                           ['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                        len_stack += 10
                        # else: EMPTY `Key-Value-List`:  No need to adjust the stack for this

            # `Key-Value-Mapping Identifier`
            elif first_char_cur_line == '.':
               # Check NONE Empty one
               next_section_line, next_section_line_indent, next_line_no_indent = prepared_lines[next_idx]
               if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                  corrected_line_no_indent = line_no_indent[2:]
                  # Set the new: cur_adjust_obj/cur_template_obj
                  cur_adjust_obj = cur_adjust_obj[corrected_line_no_indent]
                  cur_template_obj = cur_template_obj[corrected_line_no_indent][0]
                  # ADD THE STACK
                  check_indent = cur_indent
                  stack_situation = is_key_value_mapping
                  cur_stack_idx += 1
                  stack[cur_stack_idx] = (stack_situation, cur_adjust_obj, cur_template_obj)
                  if cur_stack_idx > len_stack - 3:
                     stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                     len_stack += 10
                     # else: EMPTY `Key-Value-Mapping Identifier`:  No need to adjust the stack for this

            # `BLOCK Identifier`
            elif first_char_cur_line == '*':
               # Check NONE Empty one
               next_section_line, next_section_line_indent, next_line_no_indent = prepared_lines[next_idx]
               if next_section_line_indent == cur_indent + LCONF_BASE_INDENT:
                  corrected_line_no_indent = line_no_indent[2:]
                  # Set the new: cur_adjust_obj/cur_template_obj
                  cur_adjust_obj = cur_adjust_obj[corrected_line_no_indent]
                  cur_template_obj = cur_template_obj[corrected_line_no_indent][0]
                  # ADD THE STACK
                  check_indent = cur_indent
                  stack_situation = is_blk
                  cur_stack_idx += 1
                  stack[cur_stack_idx] = (stack_situation, cur_adjust_obj, cur_template_obj)
                  if cur_stack_idx > len_stack - 3:
                     stack.extend(['STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK', 'STACK'])
                     len_stack += 10
                     # else: EMPTY `BLOCK Identifier`:  No need to adjust the stack for this

            # `Key :: Value Pair`:  we checked already for: Key :: Value-Lists
            elif ' ::' in line_no_indent:
               if ':: ' in line_no_indent:
                  name, value = line_no_indent.split(' :: ', 1)
                  # TRANSFORM CHECK: len more than 1
                  if len(cur_template_obj[name]) > 1:
                     cur_adjust_obj[name] = cur_template_obj[name][1](value, orig_line)
                  else:
                     cur_adjust_obj[name] = value
               # Empty
               else:
                  cur_adjust_obj[line_no_indent[:-3]] = ''

            # SOMETHING WRONG SHOULD NEVER REACH THIS
            else:
               raise Err('lconf_validate_one_section_str_new', [
                  'SectionName: {}'.format(section_name),
                  'SOMETHING WRONG SHOULD NEVER REACH THIS: ERROR',
                  '  Maybe a missing `List, Mapping or Block Identifier` but could be anything else.',
                  '    <{}>'.format(orig_line)
               ])

   lconf_default_obj.set_class__dict__item('is_parsed', True)

   # check_correct_number_of_blocks
   for key in lconf_default_obj.key_order:
      _check_correct_number_of_blocks(lconf_default_obj[key])
   return lconf_default_obj


def lconf_parse_section(lconf_default_obj, lconf_section_raw_str, lconf_section__template_obj, validate=False):
   """ Parses a LCONF-Section raw string and updates the section object

   :param lconf_default_obj: (obj) a prepared copy of lconf_section__template_obj: see function: lconf_prepare_default_obj()
   :param lconf_section_raw_str: (raw str) which contains one LCONF-Section
   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info
   :param validate: (bool)

         - if True the `lconf_section_raw_str` is first validated and only afterwards parsed
         - if False: no validation is done

   :return: (obj) updated lconf_default_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally updated: attributes

         - section_name: updated with the LCONF-SectionName
         - is_parsed: set to True; so one can know if this obj was already parsed
   """
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def lconf_parse_section_extract_by_name(source, section_name, lconf_section__template_obj, with_comments=False,
                                        validate=False):
   """ Parses/Extracts one LCONF-Sections from the raw string by name and returns an updated copy of the the section object

   Similar to lconf_prepare_and_parse_section() but also extract the session by name
   - Basically it does lconf_extract_one_section_by_name(), lconf_prepare_default_obj() and lconf_parse_section()

   Main usage: if one needs only one known section from the source:

      - if one needs multiple sections it might be better to use lconf_extract_all_sections()

   :param source: (raw str) which contains one or more LCONF-Sections
   :param section_name: (str) section name one wants to extract from the source
   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info
   :param with_comments: (bool) option to parse also any defined: default empty or comment line

      - if True: any `Default-Comment/Empty Lines` are parse
      - if False: any `Default-Comment/Empty Lines`` are not parse

   :param validate: (bool)

      - if True the extracted section is first validated and only afterwards parsed
      - if False: no validation is done after the section text is extracted

   :return: (obj) copy of the lconf_section__template_obj: attributes updated by the data in lconf_section_raw_str.

      - additionally updated: attributes

         - section_name: updated with the LCONF-SectionName
         - is_parsed: set to True; so one can know if this obj was already parsed

   """
   # Get Section txt
   lconf_section_raw_str = lconf_extract_one_section_by_name(source, section_name)
   if validate:
      lconf_validate_one_section_str(lconf_section_raw_str)
   # Prepare
   if with_comments:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__with_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order}, lconf_section__template_obj.key_order)
      lconf_default_obj.set_class__dict__item('has_comments', True)
   else:
      lconf_default_obj = LconfRoot({key: _prepare_default_obj__no_comments(lconf_section__template_obj[key][0]) for key in
         lconf_section__template_obj.key_order_no_comments}, lconf_section__template_obj.key_order_no_comments)
      lconf_default_obj.set_class__dict__item('has_comments', False)
   # Parse
   section_lines = lconf_section_raw_str.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   return lconf_parse_section_lines(lconf_default_obj, section_lines, section_name, lconf_section__template_obj)


def _output_helper_emit(result_, key_, item_value_, onelinelists_, indent, has_comments):
   """ Helper for output: processes a MAIN or Block-Key

   :param result_:
   :param key_:
   :param item_value_:
   :param onelinelists_:
   :param indent:
   :param has_comments:
   """
   do_rest = True
   if has_comments:
      # Default Comment/Empty Line
      if key_[0] == '#':
         if item_value_:
            result_.append('{}{}'.format(indent, item_value_))
         else:
            # empty line
            result_.append('')
         do_rest = False

   if do_rest:
      if item_value_.__class__ is str:
         if item_value_:
            result_.append('{}{} :: {}'.format(indent, key_, item_value_))
         else:
            result_.append('{}{} ::'.format(indent, key_))
      # `Key-Value-Mapping`
      elif item_value_.__class__ is LconfKVMap:
         result_.append('{}. {}'.format(indent, key_))
         for mapping_key in item_value_.key_order:
            _output_helper_emit(result_, mapping_key, item_value_[mapping_key], onelinelists_, indent + '   ', has_comments)
      elif item_value_.__class__ is LconfKVList:
         if onelinelists_ == LCONF_DEFAULT:
            use_oneline_list_type = LCONF_YES if item_value_.use_oneline else LCONF_NO
         else:
            use_oneline_list_type = onelinelists_
         # do the check
         if use_oneline_list_type == LCONF_YES:
            temp_items = []
            for i_ in item_value_:
               temp_items.append('%s' % i_)
            if temp_items:
               result_.append('{}- {} :: {}'.format(indent, key_, ','.join(temp_items)))
            else:
               result_.append('{}- {} ::'.format(indent, key_))
         elif use_oneline_list_type == LCONF_NO:
            result_.append('{}- {}'.format(indent, key_))
            for a_ in item_value_:
               result_.append('{}   {}'.format(indent, a_))
      elif item_value_.__class__ is LconfListOT:
         result_.append('{}- {} |{}|'.format(indent, key_, '|'.join(item_value_.column_names)))
         for row_ in item_value_:
            temp_items = []
            for i_ in row_:
               temp_items.append('%s' % i_)
            result_.append('{}   {}'.format(indent, ','.join(temp_items)))
      elif item_value_.__class__ is LconfBlkI:
         result_.append('{}* {}'.format(indent, key_))
         for blk_name in item_value_.key_order:
            result_.append('{}   {}'.format(indent, blk_name))
            blk_obj = item_value_[blk_name]
            for mapping_key in blk_obj.key_order:
               _output_helper_emit(result_, mapping_key, blk_obj[mapping_key], onelinelists_, indent + '      ',
                  has_comments)  # indent: 3 for blk-name + 3 new for the blk items
      else:
         result_.append('{}{} :: {}'.format(indent, key_, item_value_))


def lconf_emit(lconf_section_obj, onelinelists=LCONF_DEFAULT):
   """ Return a section_string from a lconf_section_obj

   .. note::

      - if the `lconf_section_obj` was parsed/prepared with `Default-Comment/Empty Lines` it will emit it with such
      - if the `lconf_section_obj` was parsed/prepared without `Default-Comment/Empty Lines` it will not emit any

   :param lconf_section_obj: (obj) instance of main section object which will be dumped
   :param onelinelists: (CONSTANTS) defines how list (`Key :: Value-Lists` and `Key-Value-Lists`) items are emitted

         uses the CONSTANTS:

         - LCONF_NO: all list items are dumped on separate lines using indentation

            - KEY1
                 - listitem1
                 - listitem2

         - LCONF_YES: all list items are dumped on the same line as the key separated by ` :: ` in an comma separated list

            - KEY1 :: [listitem1,listitem2]

         - LCONF_DEFAULT: uses one of the two above for each list the option defined in the:
            `LCONF-Default-Template-Structure`

   :return: (str) a LCONF text string
   :raise Err:
   """
   if lconf_section_obj.is_parsed:
      result = ['{} :: {}'.format(SECTION_START_TAG, lconf_section_obj.section_name)]

      # loop through main (root) LCONF OBJ
      has_comments = lconf_section_obj.has_comments  # get it once in a var
      for key in lconf_section_obj.key_order:
         _output_helper_emit(result, key, lconf_section_obj[key], onelinelists, '', has_comments)
   else:
      raise Err('lconf_emit', [
         'LCONF NOT PARSED ERROR: The `lconf_section_obj` seems not be parsed.',
         '    lconf_section_obj.is_parsed: <{}>'.format(lconf_section_obj.is_parsed)
      ])

   result.append(SECTION_END_TAG)
   return '\n'.join(result)


def _output_helper_emit__default_obj(result_, key_, item_value_, onelinelists_, with_comments_, indent):
   """ Helper for output: processes a MAIN or Block-Key

   :param result_:
   :param key_:
   :param item_value_:
   :param onelinelists_:
   :param with_comments_:
   :param indent:
   """
   # Default Comment/Empty Line

   if key_[0] == '#':
      if with_comments_:
         if item_value_:
            result_.append('{}{}'.format(indent, item_value_))
         else:
            # empty line
            result_.append('')
   else:
      if item_value_.__class__ is str:
         if item_value_:
            result_.append('{}{} :: {}'.format(indent, key_, item_value_))
         else:
            result_.append('{}{} ::'.format(indent, key_))
      # `Key-Value-Mapping`
      elif item_value_.__class__ is KVMap:
         result_.append('{}. {}'.format(indent, key_))
         for mapping_key in item_value_.key_order:
            _output_helper_emit__default_obj(result_, mapping_key, item_value_[mapping_key][0], onelinelists_,
               with_comments_, indent + '   ')
      elif item_value_.__class__ is KVList:
         if onelinelists_ == LCONF_DEFAULT:
            use_oneline_list_type = LCONF_YES if item_value_.use_oneline else LCONF_NO
         else:
            use_oneline_list_type = onelinelists_

         # do the check
         if use_oneline_list_type == LCONF_YES:
            temp_items = []
            for i_ in item_value_:
               temp_items.append('%s' % i_)
            if temp_items:
               result_.append('{}- {} :: {}'.format(indent, key_, ','.join(temp_items)))
            else:
               result_.append('{}- {} ::'.format(indent, key_))

         elif use_oneline_list_type == LCONF_NO:
            result_.append('{}- {}'.format(indent, key_))
            for a_ in item_value_:
               result_.append('{}   {}'.format(indent, a_))
      elif item_value_.__class__ is ListOT:
         result_.append('{}- {} |{}|'.format(indent, key_, '|'.join(item_value_.column_names)))
         for row_ in item_value_:
            temp_items = []
            for i_ in row_:
               temp_items.append('%s' % i_)
            result_.append('{}   {}'.format(indent, ','.join(temp_items)))
      elif item_value_.__class__ is BlkI:
         result_.append('{}* {}'.format(indent, key_))
         # IMPORTANT: Dummy Blk
         result_.append('{}   dummy_blk'.format(indent))
         dummy_blk = item_value_['dummy_blk']
         for mapping_key in dummy_blk.key_order:
            _output_helper_emit__default_obj(result_, mapping_key, dummy_blk[mapping_key][0], onelinelists_, with_comments_,
               indent + '      ')  # 3 for blk-name + 3 new for the blk items
      else:
         result_.append('{}{} :: {}'.format(indent, key_, item_value_))


def lconf_emit_default_obj(lconf_section__template_obj, section_name, onelinelists=LCONF_DEFAULT, with_comments=True):
   """ Return a section_string from a none parsed lconf_section_obj

   :param lconf_section__template_obj: (obj) instance of main section template object which has all the info: inclusive any
      `transform func` type-conversion
   :param section_name: (str) section name: to use
   :param onelinelists: (CONSTANTS) defines how list (`Key :: Value-Lists` and `Key-Value-Lists`) items are emitted

      uses the CONSTANTS:

      - LCONF_NO: all list items are dumped on separate lines using indentation

         - KEY1
              - listitem1
              - listitem2

      - LCONF_YES: all list items are dumped on the same line as the key separated by ` :: ` in an comma separated list

         - KEY1 :: [listitem1,listitem2]

      - LCONF_DEFAULT: uses one of the two above for each list the option defined in the: `LCONF-Default-Template-Structure`

   :param with_comments: (str) a LCONF text string
   :return:
   """
   result = ['{} :: {}'.format(SECTION_START_TAG, section_name)]

   # loop through main (root) LCONF OBJ
   for key in lconf_section__template_obj.key_order:
      _output_helper_emit__default_obj(result, key, lconf_section__template_obj[key][0], onelinelists, with_comments, '')

   result.append(SECTION_END_TAG)
   return '\n'.join(result)


def _helper_dict_to_lconf(result, key, item_value, onelinelists, skip_none_value, indent):
   """ Helper for python dict_to_lconf conversion

   :param result:
   :param key:
   :param item_value:
   :param onelinelists:
   :param skip_none_value:
   :param indent:
   :raise Err:
   """
   if item_value.__class__ is list:
      if item_value:
         # check list of lists/ list of tuples
         temp_item0 = item_value[0]
         if temp_item0.__class__ in {list, tuple}:
            # add it as longs as they are the same length
            check_length = len(temp_item0)
            # do identifier: use dummy names
            result.append('{}- {} |{}|'.format(indent, key,
               '|'.join(['item{}'.format(idx + 1) for idx, item in enumerate(temp_item0)])))
            for list_item in item_value:
               if list_item.__class__ in {list, tuple}:
                  if len(list_item) == check_length:
                     result.append('{}   {}'.format(indent, ','.join(['{}'.format(i_) for i_ in list_item])))
                  else:
                     raise Err('_helper_dict_to_lconf', [
                        '`List-Of-Tuples` rows must all be of same length. <check_length>: <{}>'.format(check_length),
                        '  We got: <{}>'.format(len(list_item)),
                        '    <{}>'.format(list_item)
                     ])
               else:
                  raise Err('_helper_dict_to_lconf', [
                     '`List-Of-Tuples` rows must be of type: <list or tuple>. We got: <{}>'.format(type(list_item)),
                     '    <{}>'.format(list_item)
                  ])
         elif onelinelists:
            print('    elif onelinelists:: ', onelinelists, type(item_value), item_value)
            temp_list = []
            for a_ in item_value:
               if a_.__class__ in {dict, list}:
                  raise Err('_helper_dict_to_lconf', [
                     'List items may not be an other dict or list: (Except multidimentional lists).',
                     '  We got: <{}>'.format(type(a_)),
                     '    <{}>'.format(a_)
                  ])
               temp_list.append(a_)
            result.append('{}- {} :: {}'.format(indent, key, ','.join(['{}'.format(i_) for i_ in temp_list])))
         else:
            result.append('{}- {}'.format(indent, key))
            for a_ in item_value:
               if a_.__class__ in {dict, list, OrderedDict}:
                  raise Err('_helper_dict_to_lconf', [
                     'List items may not be an other dict/OrderedDict or list: (Except multidimentional lists).',
                     '  We got: <{}>'.format(type(a_)),
                     '    <{}>'.format(a_)
                  ])
               result.append('{}   {}'.format(indent, a_))
      # empty list
      else:
         if onelinelists:
            result.append('{}- {} ::'.format(indent, key))
         else:
            result.append('{}- {}'.format(indent, key))
   elif item_value.__class__ in {dict, OrderedDict}:
      result.append('{}. {}'.format(indent, key))
      for mapping_key, mapping_value in item_value.items():
         # check not empty string and None, False
         if mapping_value.__class__ in {list, dict, OrderedDict}:
            _helper_dict_to_lconf(result, mapping_key, mapping_value, onelinelists, skip_none_value, indent + '   ')
         # check not empty string and None, False
         elif mapping_value.__class__ is str:
            result.append('{}   {} ::'.format(indent, mapping_key))
         elif skip_none_value and mapping_value is None:
            result.append('{}   {} ::'.format(indent, mapping_key))
         else:
            result.append('{}   {} :: {}'.format(indent, mapping_key, mapping_value))
   else:
      # check not empty string and None, False
      if item_value:
         result.append('{}{} :: {}'.format(indent, key, item_value))
      # Empty string
      elif item_value.__class__ is str:
         result.append('{}{} ::'.format(indent, key))
      elif skip_none_value and item_value is None:
         result.append('{}{} ::'.format(indent, key))
      else:
         result.append('{}{} :: {}'.format(indent, key, item_value))


def lconf_dict_to_lconf(in_dict, section_name, onelinelists=True, skip_none_value=True):
   """ Return a section_string from a `regular dictionary` as well as `OrderedDict`.

   - if the dict contains a: LCONF START-TAG (only direct keys (root keys) are checked)
      it is used instead of the supplied section_name

   Known Limitations:
      - in_dict supports only simple lists: may not contain other dict, lists
      - there won't be any `Repeated-Block Identifier` but only nested `Key-Value-Mapping` if required

   :param in_dict: (obj) dictionary of section which will be converted to a LCONF-Section string
   :param section_name: (str) section name: in normal cases a json will not have such
   :param onelinelists: (bool) defines how list items are emitted

         - if True list items are dumped on the same line as the key separated by ` :: ` in an comma separated list
            - KEY1 :: [listitem1,listitem2]
         - if False list items are dumped on separate lines using indentation
            - KEY1
                 - listitem1
                 - listitem2

   :param skip_none_value: (bool)

      - if True: json `null/python None` is transformed to a python empty string (value skipped)
      - else it is transformed to python None

   :return: (str) a LCONF text string.
   """
   result = ['']

   # remove any '___END' TAG
   if SECTION_END_TAG in in_dict:
      del in_dict[SECTION_END_TAG]

   # loop through main (root) keys
   for key, item_value in in_dict.items():
      if key == SECTION_START_TAG:
         result[0] = '{} :: {}'.format(SECTION_START_TAG, item_value)
         continue
      _helper_dict_to_lconf(result, key, item_value, onelinelists, skip_none_value, '')

   if result[0] == '':
      result[0] = '{} :: {}'.format(SECTION_START_TAG, section_name)
   result.append(SECTION_END_TAG)
   return '\n'.join(result)


def _helper_lconf_to_ordered_native_type(input_obj):
   """ Helper: to make a recursively copy of a lconf_section_obj: changing all `LCONF DICT objs` to `OrderedDict` ready to
   output with json.

   :param input_obj:
   :return:
   """
   if input_obj.__class__ in {LconfRoot, LconfKVMap, LconfBlkI, LconfBlk}:
      return OrderedDict([(key, _helper_lconf_to_ordered_native_type(input_obj[key])) for key in input_obj.key_order])
   elif input_obj.__class__ in {LconfKVList, LconfListOT}:
      return list(input_obj)
   else:
      return copy.copy(input_obj)


def lconf_to_ordered_native_type(lconf_section_obj):
   """ Return a recursive copy of the lconf_section_obj with `Lconf objs` replaced by python native objs keeping order
   - e.g. uses OrderedDict

   e.g. useful for dumping ordered json

   - `LconfRoot, LconfKVMap, LconfBlkI, LconfBlk` will be recursively copied the types will be cast to: OrderedDict
   - `LconfKVList, LconfListOT`: will be cast to: list

   :param lconf_section_obj: (obj) instance of lconf section object
   :return: (OrderedDict) recursive copy of the lconf_section_obj with `Lconf objs` replaced by python native objs
   """
   return _helper_lconf_to_ordered_native_type(lconf_section_obj)


def _helper_lconf_to_native_type(input_obj):
   """ Helper: to make a recursively copy of a lconf_section_obj: changing all `LCONF DICT objs` to `dict ready to
   output with e.g. json or yaml.

   :param input_obj:
   :return:
   """
   if input_obj.__class__ in {LconfRoot, LconfKVMap, LconfBlkI, LconfBlk}:
      return dict([(key, _helper_lconf_to_native_type(value)) for key, value in input_obj.items()])
   elif input_obj.__class__ == LconfKVList:
      return list(input_obj)
   elif input_obj.__class__ == LconfListOT:
      return list([list(tuple_) for tuple_ in input_obj])
   else:
      return copy.copy(input_obj)


def lconf_to_native_type(lconf_section_obj):
   """ Return a recursive copy of the lconf_section_obj with `Lconf objs` replaced by python native objs

   e.g. useful for dumping yaml

   - `LconfRoot, LconfKVMap, LconfBlkI, LconfBlk` will be recursively copied the types will be cast to: dict
   - `LconfKVList, LconfListOT`: will be cast to: list

      - LconfListOT tuple items will be cast to lists

   :param lconf_section_obj: (obj) instance of lconf section object
   :return: (dict) recursive copy of the lconf_section_obj with `Lconf objs` replaced by python native objs
   """
   return _helper_lconf_to_native_type(lconf_section_obj)
