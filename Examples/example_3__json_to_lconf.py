""" LCONF: Specification Examples: EXAMPLE 3: JSON - LCONF
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
   KVMap,
   Root,
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


lconf_section__example_3__template_obj = Root([
   # Default Empty Line
   ('#1', ''),
   # Default Comment Line
   ('#2', '# Comment-Line: `Key :: Value Pair`'),
   ('first', ''),
   ('last', ''),
   ('sex', ''),
   ('age', ''),
   ('salary', ''),
   ('#3', '# Comment-Line: `Key-Value-Mapping`'),
   ('favorites', KVMap([
      ('food', ''),
      ('sport', ''),
      ('color', ''),
   ])),
   ('#4', '# Comment-Line: `Key :: Value Pair`'),
   ('registered', ''),
])

lconf_section__example_3_lconf_section_raw_str = r'''___SECTION :: EXAMPLE 3
first :: John
last :: Doe
sex :: M
age :: 39
salary :: 70000
# Comment-Line: `Key-Value-Mapping`
. favorites
   food :: Spaghetti
   sport :: Soccer
   color :: Blue
registered :: True
___END'''


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# noinspection PyPep8
def main():
   # ---------------------------------- EXAMPLE 3 ---------------------------------- #

   # EXAMPLE 3: ONLY VALIDATE
   lconf_validate_one_section_str(lconf_section__example_3_lconf_section_raw_str)

   # EXAMPLE 3: ONLY PREPARE DEFAULT OBJ
   lconf_default_obj = lconf_prepare_default_obj(lconf_section__example_3__template_obj, with_comments=False)
   print('\n\n============== EXAMPLE 3: ONLY PREPARE DEFAULT OBJ ==============\n')
   print(lconf_default_obj)

   # EXAMPLE 3: VALIDATE, PREPARE, PARSE:
   # validate a `LCONF-Section string` and prepare a default lconf obj from the template obj and parse the LCONF-Section
   print('\n\n============== EXAMPLE 3: VALIDATE, PREPARE, PARSE ==============\n')
   lconf_parse_obj = lconf_prepare_and_parse_section(
      lconf_section__example_3_lconf_section_raw_str,
      lconf_section__example_3__template_obj,
      with_comments=True,
      validate=True
   )
   print(lconf_parse_obj)

   # EXAMPLE 3: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: this is also useful to extract from files
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_3_lconf_section_raw_str,
      'EXAMPLE 3',
      lconf_section__example_3__template_obj,
      with_comments=True,
      validate=True
   )
   print(
      '\n\n============== EXAMPLE 3: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: this is also useful to extract from files ==============\n')
   print(lconf_parse_obj)

   # EXAMPLE 3: ACCESS The Section-INFO
   print('\n\n============== EXAMPLE 3: ACCESS The Section-INFO ==============\n')
   print('  lconf_parse_obj.key_order: ', lconf_parse_obj.key_order)
   print('  lconf_parse_obj.section_name: ', lconf_parse_obj.section_name)
   print('  lconf_parse_obj.is_parsed: ', lconf_parse_obj.is_parsed)
   print('  lconf_parse_obj.has_comments: ', lconf_parse_obj.has_comments)

   # EXAMPLE 3: EMIT DEFAULT OBJ
   lconf_section_emitted_default_obj_str = lconf_emit__default_obj(
      lconf_section__example_3__template_obj,
      'EMITTED EXAMPLE 3',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )
   print('\n\n============== EXAMPLE 3: EMIT DEFAULT OBJ ==============\n')
   print(lconf_section_emitted_default_obj_str)

   # EXAMPLE: EMIT PARSED LCONF OBJ
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_3_lconf_section_raw_str,
      'EXAMPLE 3',
      lconf_section__example_3__template_obj,
      with_comments=True,
      validate=True
   )
   lconf_section_emitted_parsed_obj_str = lconf_emit(lconf_parse_obj, onelinelists=LCONF_DEFAULT)

   print('\n\n============== EXAMPLE 3: EMIT PARSED LCONF OBJ ==============\n')
   print(lconf_section_emitted_parsed_obj_str)

   # EXAMPLE 3: EMIT TO JSON
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__example_3_lconf_section_raw_str,
      'EXAMPLE 3',
      lconf_section__example_3__template_obj,
      with_comments=False,
      validate=True
   )
   result_ordered_native_type = lconf_to_ordered_native_type(lconf_parse_obj)
   dump_json = json_dumps(result_ordered_native_type, indent=3)

   print('\n\n============== EXAMPLE 3: EMIT TO ORDERED JSON ==============\n')
   print(dump_json)

   # EXAMPLE: EMIT TO YAML
   if has_yaml:
      lconf_parse_obj = lconf_parse_section_extract_by_name(
         lconf_section__example_3_lconf_section_raw_str,
         'EXAMPLE 3',
         lconf_section__example_3__template_obj,
         with_comments=False,
         validate=True
      )
      result_native_type = lconf_to_native_type(lconf_parse_obj)
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)

      print('\n\n============== EXAMPLE 3: EMIT TO YAML ==============\n')
      print(dump_yaml)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   main()
