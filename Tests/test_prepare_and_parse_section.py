""" tests prepare and parse section
"""
from datetime import datetime
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
   LconfBlk,
   LconfBlkI,
   LconfKVList,
   LconfKVMap,
   LconfRoot,
   LconfListOT,
)
from LCONF.lconf_structure_classes import (
   KVList,
   KVMap,
   Root,
)
from LCONF.main_code import lconf_prepare_and_parse_section

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj,
   get_lconf_section__base_example_lconf_section_raw_str,
)


# noinspection PyUnusedLocal
def test_lconf_prepare_and_parse_section_ok0():
   """ Tests: test_lconf_prepare_and_parse_section_ok0
   """
   print('::: TEST: test_lconf_prepare_and_parse_section_ok0()')

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

   lconf_section_raw_str = r'''___SECTION :: Test Example1

# Comment-Line: `Key :: Value Pair`
first :: Joe
last :: Smith
sex :: m
age :: 18
salary :: 12500
# Comment-Line
- interests
   soccer
   tennis

# Comment-Line: `Key :: Value Pair`
registered :: False
___END
'''
   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   eq_(lconf_obj['first'], 'Joe', msg=None)
   eq_(lconf_obj['last'], 'Smith', msg=None)
   eq_(lconf_obj['sex'], 'm', msg=None)
   eq_(lconf_obj['age'], '18', msg=None)
   eq_(lconf_obj['salary'], '12500', msg=None)

   ok_(isinstance(lconf_obj['interests'], LconfKVList), msg=None)
   eq_(lconf_obj['interests'], ['soccer', 'tennis'], msg=None)
   eq_(lconf_obj['interests'].use_oneline, True, msg=None)

   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=False,
      validate=False
   )


def test_lconf_prepare_and_parse_section_ok1():
   """ Tests: test_lconf_prepare_and_parse_section_ok1
   """
   print('::: TEST: test_lconf_prepare_and_parse_section_ok1()')

   lconf_section__template_obj = Root([
      ('keyvalue_mapping', KVMap([
         ('#1', '# Comment-Line:  Key-Value-Mapping items: `Key :: Value Pairs`'),
         ('mapping_key1', 'default'),
         ('mapping_key2', 'default'),
         ('mapping_key3', 'default'),
      ])),
   ])

   lconf_section_raw_str = r'''___SECTION :: Test Example1

. keyvalue_mapping
   mapping_key1 :: Something
   mapping_key2 :: Something2
   mapping_key3 :: Something3
___END
'''
   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )
   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(lconf_obj['keyvalue_mapping'], LconfKVMap), msg=None)
   eq_(lconf_obj['keyvalue_mapping']['mapping_key1'], 'Something', msg=None)
   eq_(lconf_obj['keyvalue_mapping']['mapping_key3'], 'Something3', msg=None)
   eq_(lconf_obj['keyvalue_mapping'].key_order, ['mapping_key1', 'mapping_key2', 'mapping_key3'], msg=None)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def test_lconf_prepare_and_parse_section_ok2():
   """ Tests: test_lconf_prepare_and_parse_section_ok2
   """
   print('::: TEST: test_lconf_prepare_and_parse_section_ok2()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )
   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(lconf_obj['key10value_mapping'], LconfKVMap), msg=None)
   ok_(isinstance(lconf_obj['key10value_mapping']['mapping10_key4_list'], LconfKVList), msg=None)
   ok_(isinstance(lconf_obj['key10value_mapping']['mapping10_key5_list'], LconfKVList), msg=None)
   ok_(isinstance(lconf_obj['key10value_mapping']['mapping10_key6_list'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['key10value_mapping']['mapping10_key7_list'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['key11value_mapping'], LconfKVMap), msg=None)
   ok_(isinstance(lconf_obj['key11value_mapping']['mapping11_key2_mapping'], LconfKVMap), msg=None)
   ok_(isinstance(
      lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'],
      LconfBlkI),
      msg=None
   )
   ok_(isinstance(
      lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
         'sky_blue_blk_name1'],
      LconfBlk),
      msg=None
   )
   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
      'sky_blue_blk_name1']['blk_item_green'],
      206,
      msg=None
   )

   eq_(lconf_obj.key_order,
      ['key1value_pair', 'key2value_pair', 'key3value_pair', 'key4value_pair', 'key5value_pair', 'key6value_pair',
         'key7value_pair', 'key8value_pair', 'key9value_pair', 'key10value_mapping', 'key11value_mapping', 'key12list',
         'key13value_pairlist', 'key14list_of_color_tuples', 'key15value_pairlist', 'key16value_pairlist',
         'key17list_of_tuples', 'RepeatedBlk1'],
      msg=None
   )

   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
      'sky_blue_blk_name1'].key_order,
      ['blk_item_red', 'blk_item_green', 'blk_item_blue'],
      msg=None
   )

   eq_(lconf_obj['key11value_mapping']['mapping11_key1'], '/home/examples', msg=None)
   ok_(isinstance(
      lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key1'],
      datetime),
      msg=None
   )
   eq_(lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key3'], 'car', msg=None)

   ok_(isinstance(lconf_obj['key14list_of_color_tuples'], LconfListOT), msg=None)

   eq_(lconf_obj['key14list_of_color_tuples'].column_names, ('Color Name', 'Red', 'Green', 'Blue'), msg=None)
   eq_(
      lconf_obj['key14list_of_color_tuples'].column_names_idx_lookup,
      {'Color Name': 0, 'Red': 1, 'Green': 2, 'Blue': 3},
      msg=None
   )

   eq_(lconf_obj['key14list_of_color_tuples'][0], ('forestgreen', 34, 139, 34), msg=None)

   ok_(isinstance(lconf_obj['RepeatedBlk1'], LconfBlkI), msg=None)

   eq_(lconf_obj['RepeatedBlk1'].key_order, ['BLK_OBJ1', 'BLK_OBJ2', 'BLK_OBJ3', 'BLK_OBJ4'], msg=None)
   eq_(lconf_obj['RepeatedBlk1'].min_required_blocks, 2, msg=None)
   eq_(lconf_obj['RepeatedBlk1'].max_allowed_blocks, 5, msg=None)
   eq_(lconf_obj['RepeatedBlk1'].has_comments, False, msg=None)

   eq_(
      lconf_obj['RepeatedBlk1']['BLK_OBJ4'].key_order,
      ['MyKey1_mapping', 'MyKey2', 'MyKey3', 'MyKey4', 'MyKey5list', 'MyKey6list', 'MyKey7list', 'MyKey8'],
      msg=None
   )

   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ4']['MyKey5list'], ['one item'], msg=None)
   eq_(lconf_obj['RepeatedBlk1']['BLK_OBJ4']['MyKey4'], 'GREAT LIFE', msg=None)

   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=True,
      validate=False
   )
   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=False,
      validate=False
   )
   lconf_obj = lconf_prepare_and_parse_section(
      lconf_section_raw_str,
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_prepare_and_parse_section_ok0()
   test_lconf_prepare_and_parse_section_ok1()
   test_lconf_prepare_and_parse_section_ok2()
