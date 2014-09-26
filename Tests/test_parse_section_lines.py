""" tests parse lconf sections lines
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
   ok_,
   raises as nose_raises
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
   Blk,
   BlkI,
   KVList,
   KVMap,
   Root,
   ListOT,
)
from LCONF.main_code import (
   lconf_extract_one_section_by_name,
   lconf_prepare_default_obj,
   lconf_parse_section_lines,
   lconf_section_splitlines,
   lconf_validate_one_section_str,
)
from LCONF.transform import (
   lconf_to_int,
   lconf_to_float,
   lconf_to_number,
)
from LCONF.utils import Err

# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj,
   get_lconf_section__base_example_lconf_section_raw_str
)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def test_lconf_prepare_default_obj__parse_section_lines_ok0():
   """ Tests: test_lconf_prepare_default_obj__parse_section_lines_ok0
   """
   print('::: TEST: test_lconf_prepare_default_obj__parse_section_lines_ok0()')

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
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   eq_(lconf_obj['first'], 'Joe', msg=None)
   eq_(lconf_obj['last'], 'Smith', msg=None)
   eq_(lconf_obj['sex'], 'm', msg=None)
   eq_(lconf_obj['age'], '18', msg=None)
   eq_(lconf_obj['salary'], '12500', msg=None)

   ok_(isinstance(lconf_obj['interests'], LconfKVList), msg=None)
   eq_(lconf_obj['interests'], ['soccer', 'tennis'], msg=None)
   eq_(lconf_obj['interests'].use_oneline, True, msg=None)

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__parse_section_lines_ok1():
   """ Tests: test_lconf_prepare_default_obj__parse_section_lines_ok1
   """
   print('::: TEST: test_lconf_prepare_default_obj__parse_section_lines_ok1()')

   lconf_section__template_obj = Root([
      ('keyvalue_mapping', KVMap([
         ('#1', '# Comment-Line:  Key-Value-Mapping items: `Key :: Value Pairs`'),
         ('mapping1_key1', 'default'),
         ('mapping1_key2', 'default'),
         ('mapping1_key3', 'default'),
      ])),
      ('keyvalue_mapping2', KVMap([
         ('mapping2_key1', 'default'),
      ])),
      ('keyvalue_mapping3', KVMap([
         ('mapping3_key1', 'default'),
      ])),
   ])

   lconf_section_raw_str = r'''___SECTION :: Test Example1

# Comment: Key-Value-Mapping
. keyvalue_mapping
   mapping1_key1 :: Something
   mapping1_key2 :: Something2
   mapping1_key3 :: Something3

# Comment: empty Key-Value-Mapping: uses all default values similar if it would not be defined
. keyvalue_mapping2
___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(lconf_obj['keyvalue_mapping'], LconfKVMap), msg=None)
   eq_(lconf_obj['keyvalue_mapping']['mapping1_key1'], 'Something', msg=None)
   eq_(lconf_obj['keyvalue_mapping']['mapping1_key3'], 'Something3', msg=None)
   eq_(lconf_obj['keyvalue_mapping'].key_order, ['mapping1_key1', 'mapping1_key2', 'mapping1_key3'], msg=None)

   ok_(isinstance(lconf_obj['keyvalue_mapping2'], LconfKVMap), msg=None)
   eq_(lconf_obj['keyvalue_mapping2']['mapping2_key1'], 'default', msg=None)

   ok_(isinstance(lconf_obj['keyvalue_mapping3'], LconfKVMap), msg=None)
   eq_(lconf_obj['keyvalue_mapping3']['mapping3_key1'], 'default', msg=None)

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__parse_section_lines_ok2():
   """ Tests: test_lconf_prepare_default_obj__parse_section_lines_ok2
   """
   print('::: TEST: test_lconf_prepare_default_obj__parse_section_lines_ok2()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('#1', '# Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'),
      ('list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), []),
      (None, lconf_to_int, lconf_to_int, lconf_to_int)),

      ('#2', '# Comment-Line: below is a Main `List-Of-Tuples` with 3 columns: |a|b|c|'),
      ('list_of_tuples2', ListOT(('a', 'b', 'c'), [
         ('1', '2', '3'),
         ('44', '55', '66')
      ]), (lconf_to_int, lconf_to_int, lconf_to_int)),

      ('#3', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples3', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ]), lconf_to_float),

      ('#4', '# Comment-Line: using no transform function'),
      ('list_of_tuples4', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ])),

      ('#5', '# Comment-Line: using no transform'),
      ('list_of_tuples5', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ], column_replace_missing=('-1.0', '-1.0', '-1.0'))),

      ('#6', '# Comment-Line: using multiple transform function'),
      ('list_of_tuples6', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ], column_replace_missing=('-1.0', '-1.0', '-1.0')), (lconf_to_float, lconf_to_float, lconf_to_float)),

      ('#7', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples7', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ], column_replace_missing=('-1.0', '-1.0', '-1.0')), lconf_to_float),
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample

# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   34,   139,  34
   brick,         156,  102,  31

- list_of_tuples2 |a|b|c|
   100,200,300
   400,500,600

- list_of_tuples3 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0,600.0

- list_of_tuples4 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0,600.0

- list_of_tuples5 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0

- list_of_tuples6 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0

- list_of_tuples7 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0
___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(lconf_obj['list_of_color_tuples'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples2'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples3'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples4'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples5'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples6'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples7'], LconfListOT), msg=None)

   eq_(lconf_obj['list_of_color_tuples'][0], ('forestgreen', 34, 139, 34), msg=None)
   eq_(lconf_obj['list_of_tuples2'][0], (100, 200, 300), msg=None)
   eq_(lconf_obj['list_of_tuples3'][0], (100.0, 200.0, 300.0), msg=None)
   eq_(lconf_obj['list_of_tuples4'][0], ('100.0', '200.0', '300.0'), msg=None)
   eq_(lconf_obj['list_of_tuples5'][0], ('100.0', '-1.0', '300.0'), msg=None)
   eq_(lconf_obj['list_of_tuples6'][0], (100.0, -1.0, 300.0), msg=None)
   eq_(lconf_obj['list_of_tuples7'][0], (100.0, -1.0, 300.0), msg=None)

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__parse_section_lines_ok3():
   """ Tests: test_lconf_prepare_default_obj__parse_section_lines_ok3
   """
   print('::: TEST: test_lconf_prepare_default_obj__parse_section_lines_ok3()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('#1', '# Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'),
      ('list_of_color_tuples', ListOT(
         ('Color Name', 'Red', 'Green', 'Blue'),
         [],
         column_replace_missing=('Not Defined', '-1', '-1', '-1')
      ),
      (None, lconf_to_int, lconf_to_int, lconf_to_int)),

      ('#2', '# Comment-Line: below is a Main `List-Of-Tuples` with 3 columns: |a|b|c|'),
      ('list_of_tuples2', ListOT(
         ('a', 'b', 'c'),
         [('1', '2', '3'), ('44', '55', '66')],
         column_replace_missing=('-1', '-1', '-1')
      ), (lconf_to_int, lconf_to_int, lconf_to_int)),

      ('#3', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples3', ListOT(
         ('a', 'b', 'c'),
         [('1.0', '2.0', '3.0'), ('44.0', '55.0', '66.0')],
         column_replace_missing=('-1.0', '-1.0', '-1.0')
      ), lconf_to_float),
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample

# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   ,   139,  34
   brick,         156,  102,  31

- list_of_tuples2 |a|b|c|
   100,,300
   400,500,600

- list_of_tuples3 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0

___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)

   ok_(isinstance(lconf_obj, LconfRoot), msg=None)
   ok_(isinstance(lconf_obj['list_of_color_tuples'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples2'], LconfListOT), msg=None)
   ok_(isinstance(lconf_obj['list_of_tuples3'], LconfListOT), msg=None)

   eq_(lconf_obj['list_of_color_tuples'][0], ('forestgreen', -1, 139, 34), msg=None)
   eq_(lconf_obj['list_of_tuples2'][0], (100, -1, 300), msg=None)
   eq_(lconf_obj['list_of_tuples3'][0], (100.0, -1.0, 300.0), msg=None)

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal,PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines_expect_failure1():
   """ Tests: test_lconf_section_splitlines_expect_failure1
   """
   print('::: TEST: test_lconf_section_splitlines_expect_failure1()')

   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err5.lconf')
   with open(path_to_lconf_file, 'r') as file_:
      section_lines, section_name = lconf_section_splitlines(file_.read(), validate_first_line=True)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines_expect_failure2():
   """ Tests: test_lconf_section_splitlines_expect_failure2
   """
   print('::: TEST: test_lconf_section_splitlines_expect_failure2()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('#1', '# Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'),
      ('list_of_color_tuples', ListOT(
         ('Color Name', 'Red', 'Green', 'Blue'),
         [],
         column_replace_missing=('Not Defined', '-1', '-1', '-1')
      ),
      (None, lconf_to_int, lconf_to_int, lconf_to_int)),
      ('mapping', KVMap([
         ('key1', ''),
         ('key2', ''),
      ])),
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample

# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   ,   139,  34
   brick,         156,  102,  31
. mapping
   key1 ::

      # Wrong comment Indent
   key2 :: value
___END
'''
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal,PyUnusedLocal
@nose_raises(ValueError)
def test_lconf_section_splitlines_expect_failure3():
   """ Tests: test_lconf_section_splitlines_expect_failure3
   """
   print('::: TEST: test_lconf_section_splitlines_expect_failure3()')

   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err5.lconf')
   with open(path_to_lconf_file, 'r') as file_:
      section_lines, section_name = lconf_section_splitlines(file_.read(), validate_first_line=False)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__parse_section_lines__base_example_ok():
   """ Tests: test_lconf_prepare_default_obj__parse_section_lines__base_example_ok
   """
   print('::: TEST: test_lconf_prepare_default_obj__parse_section_lines__base_example_ok()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)

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
      msg=None)
   ok_(isinstance(
      lconf_obj['key11value_mapping']['mapping11_key2_mapping']['mapping11_key2_nested_mapping_key2_block_identifier'][
         'sky_blue_blk_name1'],
      LconfBlk),
      msg=None)
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

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines__limited_number_of_blocks__expect_failure1():
   """ Tests: test_lconf_section_splitlines__limited_number_of_blocks__expect_failure1
   """
   print('::: TEST: test_lconf_section_splitlines__limited_number_of_blocks__expect_failure1()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('RepeatedBlk1', BlkI(3, 2,
         Blk([
            ('#1', '# Comment-Line: below Block-Item'),
            ('blk_key1', ''),
            ('blk_key2', 9999.999, lconf_to_number),
         ])
      )),
      ('key', '')
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample

# test comment

* RepeatedBlk1
   BLK0
      blk_key1 :: value
      blk_key2 :: -1

   BLK1
      blk_key1 :: value
      blk_key2 :: -1

key :: value
___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines__limited_number_of_blocks__expect_failure2():
   """ Tests: test_lconf_section_splitlines__limited_number_of_blocks__expect_failure2
   """
   print('::: TEST: test_lconf_section_splitlines__limited_number_of_blocks__expect_failure2()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('RepeatedBlk1', BlkI(0, 1,
         Blk([
            ('#1', '# Comment-Line: below Block-Item'),
            ('blk_key1', ''),
            ('blk_key2', 9999.999, lconf_to_number),
         ])
      )),
      ('key', '')
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample

# test comment

* RepeatedBlk1
   BLK0
      blk_key1 :: value
      blk_key2 :: -1

   BLK1
      blk_key1 :: value
      blk_key2 :: -1

key :: value
___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines__trailing_space__expect_failure():
   """ Tests: test_lconf_section_splitlines__trailing_space__expect_failure
   """
   print('::: TEST: test_lconf_section_splitlines__trailing_space__expect_failure()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = Root([
      ('#1', '# Comment-Line'),
      ('key1value_pair', ''),
      ('key2value_pair', 9999.999, lconf_to_number),
      ('key3value_pair', '')
   ])

   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err6.lconf')
   with open(path_to_lconf_file, 'r') as file_:
      lconf_section_raw_str = lconf_extract_one_section_by_name(file_.read(), 'Example')

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   for line in section_lines:
      print('<{}>'.format(line))
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_section_splitlines__missing_identifier__expect_failure():
   """ Tests: test_lconf_section_splitlines__missing_identifier__expect_failure
   """
   print('::: TEST: test_lconf_section_splitlines__missing_identifier__expect_failure()')

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
interests
   soccer
   tennis

# Comment-Line: `Key :: Value Pair`
registered :: False
___END
'''
   lconf_validate_one_section_str(lconf_section_raw_str)
   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   lconf_obj = lconf_parse_section_lines(default_lconf_obj, section_lines, section_name, lconf_section__template_obj)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_prepare_default_obj__parse_section_lines_ok0()
   test_lconf_prepare_default_obj__parse_section_lines_ok1()
   test_lconf_prepare_default_obj__parse_section_lines_ok2()
   test_lconf_prepare_default_obj__parse_section_lines_ok3()

   test_lconf_section_splitlines_expect_failure1()
   test_lconf_section_splitlines_expect_failure2()
   test_lconf_section_splitlines_expect_failure3()

   test_lconf_prepare_default_obj__parse_section_lines__base_example_ok()

   test_lconf_section_splitlines__limited_number_of_blocks__expect_failure1()
   test_lconf_section_splitlines__limited_number_of_blocks__expect_failure2()

   test_lconf_section_splitlines__trailing_space__expect_failure()
   test_lconf_section_splitlines__missing_identifier__expect_failure()
