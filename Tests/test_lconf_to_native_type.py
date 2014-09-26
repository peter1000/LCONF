""" test lconf to native type
"""
from json import (
   dumps as json_dumps,
   loads as json_loads
)
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path

# optional yaml for some example
try:
   # noinspection PyUnresolvedReferences
   from yaml import (
      load as yaml_load,
      dump as yaml_dump,
   )

   has_yaml = True
except ImportError:
   has_yaml = False

from nose.tools import (
   eq_,
   ok_
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.lconf_classes import (
   LconfKVList,
   LconfRoot,
)
from LCONF.lconf_structure_classes import (
   KVList,
   Root,
)
from LCONF.main_code import (
   lconf_dict_to_lconf,
   lconf_parse_section_extract_by_name,
   lconf_to_native_type,
   lconf_validate_one_section_str,
)

# noinspection PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj,
   get_lconf_section__base_example_lconf_section_raw_str,
)


def test_lconf_to_native_type_ok0():
   """ Tests: test_lconf_to_native_type_ok0
   """
   print('::: TEST: test_lconf_to_native_type_ok0()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', ''),
      ('sex', ''),
      ('age', ''),
      ('salary', ''),
      ('#3', '# Comment-Line: `Key-Value-List`'),
      ('interests', KVList(True, [])),
      ('#4', '# Comment-Line: `Key :: Value Pair`'),
      ('registered', ''),
   ])

   lconf_section_raw_str = r'''___SECTION :: EXAMPLE 1
#1 ::
#2 :: # Comment-Line: `Key :: Value Pair`
first :: Joe
last :: Smith
sex :: m
age :: 18
salary :: 12500
#3 :: # Comment-Line: `Key-Value-List`
- interests
   soccer
   tennis
#4 :: # Comment-Line: `Key :: Value Pair`
registered :: False
___END'''
   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'EXAMPLE 1',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   result_native_type = lconf_to_native_type(lconf_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(result_native_type, dict), msg=None)

   ok_(isinstance(lconf_obj['interests'], LconfKVList), msg=None)
   ok_(isinstance(result_native_type['interests'], list), msg=None)

   # RE DUMP AS JSON
   re_dump_json = json_dumps(result_native_type, indent=3)

   # RE CONVERT TO LCONF
   result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json),
      'EXAMPLE 1',
      onelinelists=False,
      skip_none_value=False
   )
   lconf_validate_one_section_str(result_reconverted_dict_to_lconf2)

   if has_yaml:
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)
      parsed_load_yaml = yaml_load(dump_yaml)
      ok_(isinstance(parsed_load_yaml, dict), msg=None)
      ok_(isinstance(parsed_load_yaml['interests'], list), msg=None)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_to_native_type_ok1():
   """ Tests: test_lconf_to_native_type_ok1
   """
   print('::: TEST: test_lconf_to_native_type_ok1()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True)

   result_native_type = lconf_to_native_type(lconf_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(result_native_type, dict), msg=None)

   # RE DUMP AS JSON: NOTE SPECIAL characters might not be handled correctly
   # IMPORTANT: datetime.datetime(2014, 5, 8, 13, 39) is not JSON serializable
   result_native_type['key11value_mapping']['mapping11_key2_mapping'][
      'mapping11_key2_nested_mapping_key1'] = '2014-05-08 13:39:00'
   re_dump_json = json_dumps(result_native_type, indent=3)


   # RE CONVERT TO LCONF - NOTE: there will not be any Block-Identifier
   result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json),
      'BaseEXAMPLE',
      onelinelists=False,
      skip_none_value=False
   )

   # REDO AGAIN
   redo__lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   redo__result_native_type = lconf_to_native_type(redo__lconf_obj)
   redo__dump_json = json_dumps(result_native_type, indent=3)
   eq_(redo__dump_json, re_dump_json, msg=None)

   redo__result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json),
      'BaseEXAMPLE',
      onelinelists=False,
      skip_none_value=False
   )

   lconf_validate_one_section_str(redo__result_reconverted_dict_to_lconf2)

   if has_yaml:
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)
      parsed_load_yaml = yaml_load(dump_yaml)
      ok_(isinstance(parsed_load_yaml, dict), msg=None)
      eq_(
         parsed_load_yaml['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key1'],
         '2014-05-08 13:39:00'
      )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_to_native_type_ok0()
   test_lconf_to_native_type_ok1()
