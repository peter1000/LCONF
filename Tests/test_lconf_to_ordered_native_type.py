""" test lconf to ordered native type
"""
from collections import OrderedDict
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from json import (
   dumps as json_dumps,
   loads as json_loads
)
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path

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
   lconf_to_ordered_native_type,
)

# noinspection PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj,
   get_lconf_section__base_example_lconf_section_raw_str,
)


def test_lconf_to_ordered_native_type_ok0():
   """ Tests: test_lconf_to_ordered_native_type_ok0
   """
   print('::: TEST: test_lconf_to_ordered_native_type_ok0()')

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
      with_comments=True,
      validate=True
   )

   result_ordered_native_type = lconf_to_ordered_native_type(lconf_obj)
   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(result_ordered_native_type, OrderedDict), msg=None)

   ok_(isinstance(lconf_obj['interests'], LconfKVList), msg=None)
   ok_(isinstance(result_ordered_native_type['interests'], list), msg=None)

   # RE DUMP AS JSON
   re_dump_json = json_dumps(result_ordered_native_type, indent=3)

   # RE CONVERT TO LCONF
   result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json, object_pairs_hook=OrderedDict),
      'EXAMPLE 1',
      onelinelists=False,
      skip_none_value=False
   )
   eq_(lconf_section_raw_str, result_reconverted_dict_to_lconf2, msg=None)


# noinspection PyUnusedLocal,PyPep8
def test_lconf_to_ordered_native_type_ok1():
   """ Tests: test_lconf_to_ordered_native_type_ok1
   """
   print('::: TEST: test_lconf_to_ordered_native_type_ok1()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True)

   result_ordered_native_type = lconf_to_ordered_native_type(lconf_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(result_ordered_native_type, OrderedDict), msg=None)

   # RE DUMP AS JSON: NOTE SPECIAL characters might not be handled correctly
   # IMPORTANT: datetime.datetime(2014, 5, 8, 13, 39) is not JSON serializable
   result_ordered_native_type['key11value_mapping']['mapping11_key2_mapping'][
      'mapping11_key2_nested_mapping_key1'] = '2014-05-08 13:39:00'
   re_dump_json = json_dumps(result_ordered_native_type, indent=3)
   re_dump_json_lines = re_dump_json.splitlines()

   eq_(re_dump_json_lines[1], '   "key1value_pair": "NOT-DEFINED",', msg=None)
   eq_(re_dump_json_lines[3], '   "key3value_pair": "",', msg=None)
   eq_(re_dump_json_lines[10], '   "key10value_mapping": {', msg=None)
   eq_(re_dump_json_lines[32], '      "mapping10_key7_list": [', msg=None)
   eq_(re_dump_json_lines[35], '            2.0,', msg=None)
   eq_(re_dump_json_lines[72], '   "key14list_of_color_tuples": [', msg=None)
   eq_(re_dump_json_lines[80], '         "brick",', msg=None)
   eq_(re_dump_json_lines[96], '               "nested_mapping_key1": "franz",', msg=None)
   eq_(re_dump_json_lines[103], '                     "block-item_key1": 12345.99,', msg=None)
   eq_(re_dump_json_lines[144], '            "blk_mapping_key2": -9999999999.055,', msg=None)
   eq_(re_dump_json_lines[224], '               "Nested Repeated Block Identifier": {}', msg=None)

   # RE CONVERT TO LCONF - NOTE: there will not be any Block-Identifier
   result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json, object_pairs_hook=OrderedDict),
      'EXAMPLE 1',
      onelinelists=False,
      skip_none_value=False
   )

   # NOTE: there will not be any Block-Identifier
   result_reconverted_dict_to_lconf2_lines = result_reconverted_dict_to_lconf2.splitlines()

   eq_(result_reconverted_dict_to_lconf2_lines[4], 'key4value_pair :: True', msg=None)
   eq_(result_reconverted_dict_to_lconf2_lines[9],
      r'key9value_pair :: different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ  翻訳する μεταφράζω',
      msg=None)
   eq_(result_reconverted_dict_to_lconf2_lines[23], '   - mapping10_key7_list |item1|item2|item3|', msg=None)
   eq_(result_reconverted_dict_to_lconf2_lines[31], '         . sky_blue_blk_name1', msg=None)
   eq_(result_reconverted_dict_to_lconf2_lines[70], '                  - block-item_key3_list |item1|item2|item3|', msg=None)
   eq_(result_reconverted_dict_to_lconf2_lines[104], '                  - block-item_key3_list', msg=None)

   # REDO AGAIN
   redo__lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True)

   redo__result_ordered_native_type = lconf_to_ordered_native_type(redo__lconf_obj)
   redo__dump_json = json_dumps(result_ordered_native_type, indent=3)

   eq_(redo__dump_json, re_dump_json, msg=None)

   redo__result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json, object_pairs_hook=OrderedDict),
      'EXAMPLE 1',
      onelinelists=False,
      skip_none_value=False
   )

   eq_(redo__result_reconverted_dict_to_lconf2, result_reconverted_dict_to_lconf2, msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_to_ordered_native_type_ok0()
   test_lconf_to_ordered_native_type_ok1()
