""" tests lconf default template structure usage: from lconf_structure_classes.py
"""
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
   lconf_prepare_default_obj,
   lconf_parse_section,
)


# noinspection PyUnusedLocal,PyUnresolvedReferences
def transform_function(value_str, extra_err_info):
   """ Just a dummy function for the test

   :param bool_str: (str) must be any of: True, true, False, false
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (value_str) as is
   """
   return value_str


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_main_root_obj_ok():
   """ Tests: test_lconf_main_root_obj_ok
   """
   print('::: TEST: test_lconf_main_root_obj_ok()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF Root
key1 :: value1
key2 :: value2
# Comment-Line: Root/Main LCONF-Section END TAG Line
___END'''

   example_lconf_template = Root([
      # Comment-Line: Root/Main key value pair
      ('key1', 'default_value1'),
      # Comment-Line: Root/Main key value pair with transform_function
      ('key2', 'default_value2', transform_function),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_mapping_ok():
   """ Tests: test_lconf_key_value_mapping_ok
   """
   print('::: TEST: test_lconf_key_value_mapping_ok()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key-Value-Mapping`
# Comment-Line: below is a Main `Key-Value-Mapping`
. key_value_mapping
   key1 :: value1
   key2 :: value2
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `Key-Value-Mapping`
      ('key_value_mapping', KVMap([
         ('key1', 'default_value1'),
         ('key2', 'default_value2', transform_function),
      ])),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_separated_list_ok1():
   """ Tests: test_lconf_key_value_separated_list_ok1
   """
   print('::: TEST: test_lconf_key_value_separated_list_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value-List`
# Comment-Line: below is a Main `Key :: Value-List`
- list :: 1,2,3
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `Key :: Value-List`: use_oneline is True
      ('list', KVList(True, ['default_value1', 'default_value2']))
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_separated_list_ok2():
   """ Tests: test_lconf_key_value_separated_list_ok2
   """
   print('::: TEST: test_lconf_key_value_separated_list_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value-List`
# Comment-Line: below is a Main `Key :: Value-List`
- list :: 1,2,3
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `Key :: Value-List`: use_oneline is True
      ('list', KVList(True, ['default_value1', 'default_value2']), transform_function)
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_list_ok1():
   """ Tests: test_lconf_key_value_list_ok1
   """
   print('::: TEST: test_lconf_key_value_list_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key-Value-List`
# Comment-Line: below is a Main `Key-Value-List`
- list
   1
   2
   3
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `Key :: Value-List`: use_oneline is False
      ('list', KVList(False, ['default_value1', 'default_value2']))
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_list_ok2():
   """ Tests: test_lconf_key_value_list_ok2
   """
   print('::: TEST: test_lconf_key_value_list_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key-Value-List`
# Comment-Line: below is a Main `Key-Value-List`
- list
   1
   2
   3
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `Key :: Value-List`: use_oneline is False
      ('list', KVList(False, ['default_value1', 'default_value2']), transform_function)
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok1():
   """ Tests: test_lconf_list_of_tuples_ok1
   """
   print('::: TEST: test_lconf_list_of_tuples_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   34,   139,  34
   brick,         156,  102,  31
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'
      ('list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), [
         ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue'),
         ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue')
      ])),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok2():
   """ Tests: test_lconf_list_of_tuples_ok2
   """
   print('::: TEST: test_lconf_list_of_tuples_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   34,   139,  34
   brick,         156,  102,  31
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'
      ('list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), [
         ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue'),
         ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue')
      ]), (None, transform_function, transform_function, transform_function)),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok3():
   """ Tests: test_lconf_list_of_tuples_ok3
   """
   print('::: TEST: test_lconf_list_of_tuples_ok3()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
- list_of_point_tuples |x|y|z|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   1,3,7
   2,6,14
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
         ('default_value_x', 'default_value_y', 'default_value_z'),
         ('default_value_x', 'default_value_y', 'default_value_z'),
      ]), transform_function),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok4():
   """ Tests: test_lconf_list_of_tuples_ok4
   """
   print('::: TEST: test_lconf_list_of_tuples_ok4()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
- list_of_point_tuples |x|y|z|
   # Comment-Line: `List-Of-Tuples` item lines (rows) with missing items
   ,,
   2, ,14
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
         ('default_value_x', 'default_value_y', 'default_value_z'),
         ('default_value_x', 'default_value_y', 'default_value_z'),
      ])),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok5():
   """ Tests: test_lconf_list_of_tuples_ok5
   """
   print('::: TEST: test_lconf_list_of_tuples_ok5()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
- list_of_point_tuples |x|y|z|
   # Comment-Line: `List-Of-Tuples` item lines (rows) with missing items
   ,,
   2, ,14
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
         ('default_value_x', 'default_value_y', 'default_value_z'),
         ('default_value_x', 'default_value_y', 'default_value_z'),
      ], column_replace_missing=('-1', '-1', '-1'))),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok6():
   """ Tests: test_lconf_list_of_tuples_ok6
   """
   print('::: TEST: test_lconf_list_of_tuples_ok6()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
- list_of_point_tuples |x|y|z|
   # Comment-Line: `List-Of-Tuples` item lines (rows) with missing items
   ,,
   2, ,14
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
         ('default_value_x', 'default_value_y', 'default_value_z'),
         ('default_value_x', 'default_value_y', 'default_value_z'),
      ], column_replace_missing=('-1', '-1', '-1')), transform_function),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_list_of_tuples_ok7():
   """ Tests: test_lconf_list_of_tuples_ok7
   """
   print('::: TEST: test_lconf_list_of_tuples_ok7()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `List-Of-Tuples`
# Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
- list_of_point_tuples |x|y|z|
   # Comment-Line: `List-Of-Tuples` item lines (rows) with missing items
   ,,
   2, ,14
___END'''

   example_lconf_template = Root([
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
         ('default_value_x', 'default_value_y', 'default_value_z'),
         ('default_value_x', 'default_value_y', 'default_value_z'),
      ], column_replace_missing=('-1', '-1', '-1')), (transform_function, transform_function, transform_function)),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_repeated_block_identifier_ok1():
   """ Tests: test_lconf_repeated_block_identifier_ok1
   """
   print('::: TEST: test_lconf_repeated_block_identifier_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Repeated-Block-Identifier`
# Comment-Line: below is a Main `Repeated-Block-Identifier`
* My_Repeated_Block

   BlockName1
      key1 :: value1
      key2 :: value2

   BlockName2
      key1 :: value1
      key2 :: value2
___END'''

   example_lconf_template = Root([
      # Comment-Line: Root/Main `Repeated-Block-Identifier`: **min_required_blocks, max_allowed_blocks** not defined (-1)
      ('My_Repeated_Block', BlkI(-1, -1,
         # Comment-Line: Dummy Block
         Blk([
            # Comment-Line: Block key value pair
            ('key1', 'default_value1`'),
            # Comment-Line: Block key value pair with transform_function
            ('key2', 'default_value2', transform_function),
         ])
      )),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_repeated_block_identifier_ok2():
   """ Tests: test_lconf_repeated_block_identifier_ok2
   """
   print('::: TEST: test_lconf_repeated_block_identifier_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Repeated-Block-Identifier`
# Comment-Line: below is a Main `Repeated-Block-Identifier`
* My_Repeated_Block

   BlockName1
      key1 :: value1
      key2 :: value2

   BlockName2
      key1 :: value1
      key2 :: value2
___END'''

   example_lconf_template = Root([
      # Comment-Line: Root/Main `Repeated-Block-Identifier`: **min_required_blocks, max_allowed_blocks** set both to 2
      ('My_Repeated_Block', BlkI(2, 2,
         # Comment-Line: Dummy Block
         Blk([
            # Comment-Line: Block key value pair
            ('key1', 'default_value1'),
            # Comment-Line: Block key value pair with transform_function
            ('key2', 'default_value2', transform_function),
         ])
      )),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_block_name_ok1():
   """ Tests: test_lconf_block_name_ok1
   """
   print('::: TEST: test_lconf_block_name_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Block-Name` - `Block` (dummy block)
* My_Repeated_Block
   # Comment-Line: below is a `Block-Name` - `Block` (dummy block)
   BlockName1
      key1 :: value1
      key2 :: value2
   # Comment-Line: below is another `Block-Name` - `Block` (dummy block)
   BlockName2
      key1 :: value1
      key2 :: value2
___END'''

   example_lconf_template = Root([
      ('My_Repeated_Block', BlkI(2, 5,
         # Comment-Line: Dummy Block
         Blk([
            ('key1', 'default_value1'),
            ('key2', 'default_value2', transform_function),
         ])
      )),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_separator_items_ok1():
   """ Tests: test_lconf_key_value_separator_items_ok1
   """
   print('::: TEST: test_lconf_key_value_separator_items_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value Pairs`
# Comment-Line: Root/Main key value pair
key1 :: value1
___END'''

   example_lconf_template = Root([
      # Comment-Line: Root/Main key value pair
      ('key1', 'default_value1'),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_key_value_separator_items_ok2():
   """ Tests: test_lconf_key_value_separator_items_ok2
   """
   print('::: TEST: test_lconf_key_value_separator_items_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value Pairs`
# Comment-Line: Root/Main key value pair
key1 :: value1
___END'''

   example_lconf_template = Root([
      # Comment-Line: Root/Main key value pair with transform_function
      ('key1', 'default_value1', transform_function),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_default_comment_lines_ok1():
   """ Tests: test_lconf_default_comment_lines_ok1
   """
   print('::: TEST: test_lconf_default_comment_lines_ok1()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value Pairs`
key1 :: value1
key2 :: value2
___END'''

   example_lconf_template = Root([
      ('#1', '# Comment this is a `Default Comment Line` which can be emitted'),
      ('key1', 'default_value1'),
      ('#2', '# this is another `Default Comment Line` which can be emitted'),
      ('key2', 'default_value1'),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# noinspection PyUnusedLocal,PyUnusedLocal
def test_lconf_default_comment_lines_ok2():
   """ Tests: test_lconf_default_comment_lines_ok2
   """
   print('::: TEST: test_lconf_default_comment_lines_ok2()')

   lconf_section_raw_str = r'''___SECTION :: Example LCONF `Key :: Value Pairs`
key1 :: value1
key2 :: value2
___END'''

   example_lconf_template = Root([
      # Comment below is an `Empty default Comment Line` which can be emitted
      ('#1', ''),
      ('key1', 'default_value1'),
      # Comment below is another `Empty default Comment Line` which can be emitted
      ('#2', ''),
      ('key2', 'default_value1'),
   ])

   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=True)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=True)
   default_lconf_obj = lconf_prepare_default_obj(example_lconf_template, with_comments=False)
   lconf_obj = lconf_parse_section(default_lconf_obj, lconf_section_raw_str, example_lconf_template, validate=False)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_main_root_obj_ok()
   test_lconf_key_value_mapping_ok()
   test_lconf_key_value_separated_list_ok1()
   test_lconf_key_value_separated_list_ok2()
   test_lconf_key_value_list_ok1()
   test_lconf_key_value_list_ok2()
   test_lconf_list_of_tuples_ok1()
   test_lconf_list_of_tuples_ok2()
   test_lconf_list_of_tuples_ok3()
   test_lconf_list_of_tuples_ok4()
   test_lconf_list_of_tuples_ok5()
   test_lconf_list_of_tuples_ok6()
   test_lconf_repeated_block_identifier_ok1()
   test_lconf_repeated_block_identifier_ok2()
   test_lconf_block_name_ok1()
   test_lconf_key_value_separator_items_ok1()
   test_lconf_key_value_separator_items_ok2()
   test_lconf_default_comment_lines_ok1()
   test_lconf_default_comment_lines_ok2()
