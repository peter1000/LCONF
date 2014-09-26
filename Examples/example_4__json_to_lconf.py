""" LCONF: Specification Examples: EXAMPLE 4: JSON - LCONF
"""
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from json import dumps as json_dumps
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path

# optional yaml for some example: needs pyyaml installed
try:
   # noinspection PyUnresolvedReferences
   from yaml import dump as yaml_dump
   has_yaml = True
except ImportError:
   has_yaml = False

SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.lconf_structure_classes import (
   Blk,
   BlkI,
   KVList,
   KVMap,
   Root,
   ListOT,
)
from LCONF.main_code import (
   LCONF_DEFAULT,
   lconf_emit,
   lconf_emit__default_obj,
   lconf_parse_section_extract_by_name,
   lconf_prepare_and_parse_section,
   lconf_prepare_default_obj,
   lconf_to_native_type,
   lconf_to_ordered_native_type,
   lconf_validate_one_section_str,
)
from LCONF.transform import (
   lconf_to_int,
)


lconf_section__example_4a__template_obj = Root([
   # Default Empty Line
   ('#1', ''),
   ('registered_employees', 0, lconf_to_int),
   ('#2', '# Comment-Line: `Repeated-Block-Identifier`'),
   ('Employee', BlkI(-1, -1,
      Blk([
         ('first', ''),
         ('last', ''),
         ('sex', ''),
         ('age', ''),
         ('past_salary', KVMap([
            ('year2012', ''),
            ('year2013', -1, lconf_to_int),
         ])),
         ('emails', KVList(True, [])),
      ]),
   )),
   ('registered_customer', 0, lconf_to_int),
   ('#3', '# Comment-Line: `List-Of-Tuples`'),
   ('accounting', ListOT(('item1', 'item2', 'item3', 'item4'), [])),
])

lconf_section__example_4a_lconf_section_raw_str = r'''___SECTION :: EXAMPLE 4 a
registered_employees :: 28594
* Employee
   Person1
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      . past_salary
         year2012 :: 45000
         year2013 :: 62000
      - emails
         <xaver@dot.com>
         <xaver23@yahoo.com>
registered_customer :: 28594
- accounting |item1|item2|item3|item4|
   2010,38459845,15835945,3000945
   2011,38459845,15835945,3000945
   2012,28456849,4846123,2599901
   2013,38459845,15835945,3000945
___END'''

lconf_section__example_4b__template_obj = Root([
   # Default Empty Line
   ('#1', ''),
   ('registered_employees', 0, lconf_to_int),
   ('#2', '# Comment-Line: `Repeated-Block-Identifier`'),
   ('Employee', KVMap([
      ('Person1', KVMap([
         ('first', ''),
         ('last', ''),
         ('sex', ''),
         ('age', ''),
         ('past_salary', KVMap([
            ('year2012', ''),
            ('year2013', -1, lconf_to_int),
         ])),
         ('emails', KVList(True, [])),
      ])),
   ])),
   ('registered_customer', 0, lconf_to_int),
   ('#3', '# Comment-Line: `List-Of-Tuples`'),
   ('accounting', ListOT(('item1', 'item2', 'item3', 'item4'), [])),
])

lconf_section__example_4b_lconf_section_raw_str = r'''___SECTION :: EXAMPLE 4 b
registered_employees :: 28594
. Employee
   . Person1
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      . past_salary
         year2012 :: 45000
         year2013 :: 62000
      - emails
         <xaver@dot.com>
         <xaver23@yahoo.com>
registered_customer :: 28594
- accounting |item1|item2|item3|item4|
   2010,38459845,15835945,3000945
   2011,38459845,15835945,3000945
   2012,28456849,4846123,2599901
   2013,38459845,15835945,3000945
___END'''


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # ---------------------------------- EXAMPLE 4 a ---------------------------------- #

   # EXAMPLE 4 a: ONLY VALIDATE
   lconf_validate_one_section_str(lconf_section__example_4a_lconf_section_raw_str)

   # EXAMPLE 4 a: ONLY PREPARE DEFAULT OBJ
   lconf_default_obj = lconf_prepare_default_obj(lconf_section__example_4a__template_obj, with_comments=False)
   print('\n\n============== EXAMPLE 4 a: ONLY PREPARE DEFAULT OBJ ==============\n')
   print(lconf_default_obj)

   # EXAMPLE 4 a: VALIDATE, PREPARE, PARSE:
   # validate a `LCONF-Section string` and prepare a default lconf obj from the template obj and parse the LCONF-Section
   print('\n\n============== EXAMPLE 4 a: VALIDATE, PREPARE, PARSE ==============\n')
   lconf_parse_obj = lconf_prepare_and_parse_section(
      lconf_section__example_4a_lconf_section_raw_str,
      lconf_section__example_4a__template_obj,
      with_comments=True,
      validate=True
   )
   print(lconf_parse_obj)

   # EXAMPLE 4 a: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: this is also useful to extract from files
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4a_lconf_section_raw_str,
      'EXAMPLE 4 a',
      lconf_section__example_4a__template_obj,
      with_comments=True,
      validate=True
   )
   print(
      '\n\n============== EXAMPLE 4 a: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: also for files ==============\n')
   print(lconf_parse_obj)

   # EXAMPLE 4 a: ACCESS The Section-INFO
   print('\n\n============== EXAMPLE 4 a: ACCESS The Section-INFO ==============\n')
   print('  lconf_parse_obj.key_order: ', lconf_parse_obj.key_order)
   print('  lconf_parse_obj.section_name: ', lconf_parse_obj.section_name)
   print('  lconf_parse_obj.is_parsed: ', lconf_parse_obj.is_parsed)
   print('  lconf_parse_obj.has_comments: ', lconf_parse_obj.has_comments)

   # EXAMPLE 4 a: EMIT DEFAULT OBJ
   lconf_section_emitted_default_obj_str = lconf_emit__default_obj(
      lconf_section__example_4a__template_obj,
      'EMITTED EXAMPLE 4 a',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )
   print('\n\n============== EXAMPLE 4 a: EMIT DEFAULT OBJ ==============\n')
   print(lconf_section_emitted_default_obj_str)

   # EXAMPLE: EMIT PARSED LCONF OBJ
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4a_lconf_section_raw_str,
      'EXAMPLE 4 a',
      lconf_section__example_4a__template_obj,
      with_comments=True,
      validate=True
   )
   lconf_section_emitted_parsed_obj_str = lconf_emit(lconf_parse_obj, onelinelists=LCONF_DEFAULT)

   print('\n\n============== EXAMPLE 4 a: EMIT PARSED LCONF OBJ ==============\n')
   print(lconf_section_emitted_parsed_obj_str)

   # EXAMPLE 4 a: EMIT TO JSON
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4a_lconf_section_raw_str,
      'EXAMPLE 4 a',
      lconf_section__example_4a__template_obj,
      with_comments=False,
      validate=True
   )
   result_ordered_native_type = lconf_to_ordered_native_type(lconf_parse_obj)
   dump_json = json_dumps(result_ordered_native_type, indent=3)

   print('\n\n============== EXAMPLE 4 a: EMIT TO ORDERED JSON ==============\n')
   print(dump_json)

   # EXAMPLE: EMIT TO YAML
   if has_yaml:
      lconf_parse_obj = lconf_parse_section_extract_by_name(
         lconf_section__example_4a_lconf_section_raw_str,
         'EXAMPLE 4 a',
         lconf_section__example_4a__template_obj,
         with_comments=False,
         validate=True
      )
      result_native_type = lconf_to_native_type(lconf_parse_obj)
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)

      print('\n\n============== EXAMPLE 4 a: EMIT TO YAML ==============\n')
      print(dump_yaml)


   # ---------------------------------- EXAMPLE 4 b ---------------------------------- #

   # EXAMPLE 4 b: ONLY VALIDATE
   lconf_validate_one_section_str(lconf_section__example_4b_lconf_section_raw_str)

   # EXAMPLE 4 b: ONLY PREPARE DEFAULT OBJ
   lconf_default_obj = lconf_prepare_default_obj(lconf_section__example_4b__template_obj, with_comments=False)
   print('\n\n============== EXAMPLE 4 b: ONLY PREPARE DEFAULT OBJ ==============\n')
   print(lconf_default_obj)

   # EXAMPLE 4 b: VALIDATE, PREPARE, PARSE:
   # validate a `LCONF-Section string` and prepare a default lconf obj from the template obj and parse the LCONF-Section
   print('\n\n============== EXAMPLE 4 b: VALIDATE, PREPARE, PARSE ==============\n')
   lconf_parse_obj = lconf_prepare_and_parse_section(
      lconf_section__example_4b_lconf_section_raw_str,
      lconf_section__example_4b__template_obj,
      with_comments=True,
      validate=True
   )
   print(lconf_parse_obj)

   # EXAMPLE 4 b: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: this is also useful to extract from files
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4b_lconf_section_raw_str,
      'EXAMPLE 4 b',
      lconf_section__example_4b__template_obj,
      with_comments=True,
      validate=True
   )
   print(
      '\n\n============== EXAMPLE 4 b: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: also for files ==============\n')
   print(lconf_parse_obj)

   # EXAMPLE 4 b: ACCESS The Section-INFO
   print('\n\n============== EXAMPLE 4 b: ACCESS The Section-INFO ==============\n')
   print('  lconf_parse_obj.key_order: ', lconf_parse_obj.key_order)
   print('  lconf_parse_obj.section_name: ', lconf_parse_obj.section_name)
   print('  lconf_parse_obj.is_parsed: ', lconf_parse_obj.is_parsed)
   print('  lconf_parse_obj.has_comments: ', lconf_parse_obj.has_comments)

   # EXAMPLE 4 b: EMIT DEFAULT OBJ
   lconf_section_emitted_default_obj_str = lconf_emit__default_obj(
      lconf_section__example_4b__template_obj,
      'EMITTED EXAMPLE 4 b',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )
   print('\n\n============== EXAMPLE 4 b: EMIT DEFAULT OBJ ==============\n')
   print(lconf_section_emitted_default_obj_str)

   # EXAMPLE: EMIT PARSED LCONF OBJ
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4b_lconf_section_raw_str,
      'EXAMPLE 4 b',
      lconf_section__example_4b__template_obj,
      with_comments=True,
      validate=True
   )
   lconf_section_emitted_parsed_obj_str = lconf_emit(lconf_parse_obj, onelinelists=LCONF_DEFAULT)

   print('\n\n============== EXAMPLE 4 b: EMIT PARSED LCONF OBJ ==============\n')
   print(lconf_section_emitted_parsed_obj_str)

   # EXAMPLE 4 b: EMIT TO JSON
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_4b_lconf_section_raw_str,
      'EXAMPLE 4 b',
      lconf_section__example_4b__template_obj,
      with_comments=False,
      validate=True
   )
   result_ordered_native_type = lconf_to_ordered_native_type(lconf_parse_obj)
   dump_json = json_dumps(result_ordered_native_type, indent=3)

   print('\n\n============== EXAMPLE 4 b: EMIT TO ORDERED JSON ==============\n')
   print(dump_json)

   # EXAMPLE: EMIT TO YAML
   if has_yaml:
      lconf_parse_obj = lconf_parse_section_extract_by_name(
         lconf_section__example_4b_lconf_section_raw_str,
         'EXAMPLE 4 b',
         lconf_section__example_4b__template_obj,
         with_comments=False,
         validate=True
      )
      result_native_type = lconf_to_native_type(lconf_parse_obj)
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)

      print('\n\n============== EXAMPLE 4 b: EMIT TO YAML ==============\n')
      print(dump_yaml)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   main()
