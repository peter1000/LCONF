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
from LCONF.transform import (
   lconf_to_int,
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
      ('last', '', None, 'NOT-DEFINED'),
      ('sex', '', None, 'NOT-DEFINED'),
      ('age', '', lconf_to_int, -1),
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

   ok_(lconf_obj['last'] == result_native_type['last'] == 'Smith', msg=None)
   ok_(lconf_obj['age'] == result_native_type['age'] == 18, msg=None)


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
      ok_(parsed_load_yaml['last'] == lconf_obj['last'] == result_native_type['last'] == 'Smith', msg=None)
      ok_(parsed_load_yaml['age'] == lconf_obj['age'] == result_native_type['age'] == 18, msg=None)


def test_lconf_to_native_type_ok1():
   """ Tests: test_lconf_to_native_type_ok1
   """
   print('::: TEST: test_lconf_to_native_type_ok1()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', '', None, 'NOT-DEFINED'),
      ('sex', '', None, 'NOT-DEFINED'),
      ('age', '', lconf_to_int, -1),
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
last ::
sex ::
age ::
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

   ok_(lconf_obj['last'] == result_native_type['last'] == 'NOT-DEFINED', msg=None)
   ok_(lconf_obj['sex'] == result_native_type['sex'] == 'NOT-DEFINED', msg=None)
   ok_(lconf_obj['age'] == result_native_type['age'] == -1, msg=None)


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
      ok_(parsed_load_yaml['last'] == lconf_obj['last'] == result_native_type['last'] == 'NOT-DEFINED', msg=None)
      ok_(parsed_load_yaml['sex'] == lconf_obj['sex'] == result_native_type['sex'] == 'NOT-DEFINED', msg=None)
      ok_(parsed_load_yaml['age'] == lconf_obj['age'] == result_native_type['age'] == -1, msg=None)


# noinspection PyUnusedLocal
def test_lconf_to_native_type_ok2():
   """ Tests: test_lconf_to_native_type_ok2
   """
   print('::: TEST: test_lconf_to_native_type_ok2()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()
   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True)

   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
      'sky_blue_blk_name1']['blk_item_green'],
      206,
      msg=None)

   eq_(lconf_obj.key_order,
      ['key1value_pair', 'key2value_pair', 'key3value_pair', 'key4value_pair', 'key5value_pair', 'key6value_pair',
         'key7value_pair', 'key8value_pair', 'key9value_pair', 'key10value_mapping', 'key11value_mapping', 'key12list',
         'key13value_pairlist', 'key14list_of_color_tuples', 'key15value_pairlist', 'key16value_pairlist',
         'key17list_of_tuples', 'RepeatedBlk1'],
      msg=None)

   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
      'sky_blue_blk_name1'].key_order,
      ['blk_item_red', 'blk_item_green', 'blk_item_blue'],
      msg=None)

   eq_(lconf_obj['key11value_mapping']['mapping11_key1'], '/home/examples', msg=None)
   eq_(lconf_obj['key1value_pair'], 'NOT-DEFINED', msg=None)  # `Empty-KeyValuePair-ReplacementValue` "NOT-DEFINED"
   eq_(lconf_obj['key7value_pair'], -94599.5, msg=None)  # `Empty-KeyValuePair-ReplacementValue` "-94599.5"

   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key3'], 'car', msg=None)
   # `Empty-KeyValuePair-ReplacementValue` "0"
   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
      'sky_blue_blk_name1']['blk_item_red'], 0, msg=None)

   eq_(lconf_obj['key14list_of_color_tuples'].column_names, ('Color Name', 'Red', 'Green', 'Blue'), msg=None)
   eq_(
      lconf_obj['key14list_of_color_tuples'].column_names_idx_lookup,
      {'Color Name': 0, 'Red': 1, 'Green': 2, 'Blue': 3},
      msg=None
   )

   eq_(lconf_obj['key14list_of_color_tuples'][0], ('forestgreen', 34, 139, 34), msg=None)

   eq_(lconf_obj['RepeatedBlk1'].key_order, ['BLK_OBJ1', 'BLK_OBJ2', 'BLK_OBJ3', 'BLK_OBJ4'], msg=None)
   eq_(lconf_obj['RepeatedBlk1'].min_required_blocks, 2, msg=None)
   eq_(lconf_obj['RepeatedBlk1'].max_allowed_blocks, 5, msg=None)
   eq_(lconf_obj['RepeatedBlk1'].has_comments, False, msg=None)

   eq_(
      lconf_obj['RepeatedBlk1']['BLK_OBJ4'].key_order,
      ['MyKey1_mapping', 'MyKey2', 'MyKey3', 'MyKey4', 'MyKey5list', 'MyKey6list', 'MyKey7list', 'MyKey8'],
      msg=None
   )
   # `Empty-KeyValuePair-ReplacementValue` "-9999999999.055"
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ1']['MyKey1_mapping']['blk_mapping_key2'], 12345.99, msg=None)
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ2']['MyKey1_mapping']['blk_mapping_key2'], -9999999999.055, msg=None)
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ3']['MyKey1_mapping']['blk_mapping_key2'], 9999.999, msg=None)
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ4']['MyKey1_mapping']['blk_mapping_key2'], 9999.999, msg=None)

   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ4']['MyKey5list'], ['one item'], msg=None)
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ4']['MyKey4'], 'GREAT LIFE', msg=None)

   result_native_type = lconf_to_native_type(lconf_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(result_native_type, dict), msg=None)

   ok_(lconf_obj['key1value_pair'] == result_native_type['key1value_pair'] == 'NOT-DEFINED', msg=None)
   ok_(lconf_obj['key7value_pair'] == result_native_type['key7value_pair'] == -94599.5, msg=None)

   # RE DUMP AS JSON: NOTE SPECIAL characters might not be handled correctly
   # IMPORTANT: datetime.datetime(2014, 5, 8, 13, 39) is not JSON serializable
   result_native_type['key11value_mapping']['mapping11_key2_mapping'][
      'mapping11_key2_nested_mapping_key1'] = '2014-05-08 13:39:00'
   re_dump_json = json_dumps(result_native_type, indent=3)

   # RE CONVERT TO LCONF - NOTE: there will not be any Block-Identifier also the order might be messed up which does not work
   # with comment lines
   result_reconverted_dict_to_lconf2 = lconf_dict_to_lconf(
      json_loads(re_dump_json),
      'BaseEXAMPLE',
      onelinelists=False,
      skip_none_value=False
   )

   lconf_validate_one_section_str(result_reconverted_dict_to_lconf2)

   # do yaml of result_native_type
   if has_yaml:
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)
      parsed_load_yaml = yaml_load(dump_yaml)
      ok_(isinstance(parsed_load_yaml, dict), msg=None)
      eq_(
         parsed_load_yaml['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key1'],
         '2014-05-08 13:39:00'
      )
      eq_(parsed_load_yaml['key11value_mapping']['mapping11_key2_mapping'][
         'mapping11_key2_nested_mapping_key2_block_identifier']['sky_blue_blk_name1']['blk_item_green'],
         206,
         msg=None)

      eq_(parsed_load_yaml['key11value_mapping']['mapping11_key1'], '/home/examples', msg=None)
      eq_(parsed_load_yaml['key1value_pair'], 'NOT-DEFINED', msg=None)  # `Empty-KeyValuePair-ReplacementValue` "NOT-DEFINED"
      eq_(parsed_load_yaml['key7value_pair'], -94599.5, msg=None)  # `Empty-KeyValuePair-ReplacementValue` "-94599.5"

      eq_(parsed_load_yaml['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key3'],
         'car',
         msg=None)
      # `Empty-KeyValuePair-ReplacementValue` "0"
      eq_(parsed_load_yaml['key11value_mapping']['mapping11_key2_mapping'][
         'mapping11_key2_nested_mapping_key2_block_identifier']['sky_blue_blk_name1']['blk_item_red'],
         0,
         msg=None)

      # Tuple are changed to lists
      eq_(parsed_load_yaml['key14list_of_color_tuples'][0], ['forestgreen', 34, 139, 34], msg=None)

      # `Empty-KeyValuePair-ReplacementValue` "-9999999999.055"
      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ1']['MyKey1_mapping']['blk_mapping_key2'], 12345.99, msg=None)
      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ2']['MyKey1_mapping']['blk_mapping_key2'], -9999999999.055, msg=None)
      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ3']['MyKey1_mapping']['blk_mapping_key2'], 9999.999, msg=None)
      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ4']['MyKey1_mapping']['blk_mapping_key2'], 9999.999, msg=None)

      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ4']['MyKey5list'], ['one item'], msg=None)
      eq_(parsed_load_yaml['RepeatedBlk1']['BLK_OBJ4']['MyKey4'], 'GREAT LIFE', msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_to_native_type_ok0()
   test_lconf_to_native_type_ok1()
   test_lconf_to_native_type_ok2()
