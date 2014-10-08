""" tests prepare default lconf obj
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
   ok_,
   eq_,
)


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
)
from LCONF.main_code import lconf_prepare_default_obj
from LCONF.transform import (
   lconf_to_bool,
   lconf_to_datetime,
   lconf_to_int,
   lconf_to_float,
   lconf_to_pathexpanduser,
)

# noinspection PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj
)


def test_lconf_prepare_default_obj__ok0():
   """ Tests: test_lconf_prepare_default_obj__ok0
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok0()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', ''),
      ('sex', '', None, 'NOT-DEFINED'),
      ('age', ''),
      ('salary', ''),
      ('#3', '# Comment-Line: `Key-Value-List`'),
      ('interests', KVList(True, [])),
      ('#4', '# Comment-Line: `Key :: Value Pair`'),
      ('registered', ''),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   eq_(default_lconf_obj.key_order, ['first', 'last', 'sex', 'age', 'salary', 'interests', 'registered'], msg=None)
   eq_(default_lconf_obj.key_empty_replacementvalue, {'sex': 'NOT-DEFINED'}, msg=None)

   eq_(default_lconf_obj.has_comments, False, msg=None)

   eq_(type(default_lconf_obj['age']), str, msg=None)
   eq_(default_lconf_obj['age'], '', msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(
      default_lconf_obj.key_order,
      ['#1', '#2', 'first', 'last', 'sex', 'age', 'salary', '#3', 'interests', '#4', 'registered'],
      msg=None
   )
   eq_(default_lconf_obj.has_comments, True, msg=None)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__ok1():
   """ Tests: test_lconf_prepare_default_obj__ok1
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok1()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', ''),
      ('sex', '', None, 'NOT-DEFINED'),
      ('age', '', lconf_to_int, -1),
      ('salary', 0.0, lconf_to_float),
      ('#3', '# Comment-Line: `Key-Value-List`'),
      ('interests', KVList(True, [])),
      ('#4', '# Comment-Line: `Key :: Value Pair`'),
      ('registered', True, lconf_to_bool),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   eq_(default_lconf_obj.key_empty_replacementvalue, {'age': -1, 'sex': 'NOT-DEFINED'}, msg=None)

   eq_(type(default_lconf_obj['age']), int, msg=None)
   eq_(default_lconf_obj['age'], -1, msg=None)  # `Empty-KeyValuePair-ReplacementValues`
   eq_(type(default_lconf_obj['salary']), float, msg=None)
   eq_(type(default_lconf_obj['registered']), bool, msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(default_lconf_obj.key_empty_replacementvalue, {'age': -1, 'sex': 'NOT-DEFINED'}, msg=None)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__ok2():
   """ Tests: test_lconf_prepare_default_obj__ok2
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok2()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', ''),
      ('sex', ''),
      ('age', '', lconf_to_int),
      ('salary', 0.0, lconf_to_float),
      ('#3', '# Comment-Line: `Key-Value-Mapping`'),
      ('favorites', KVMap([
         ('food', ''),
         ('sport', '', None, 'Not-Defined'),
         ('color', ''),
      ])),
      ('#4', '# Comment-Line: `Key :: Value Pair`'),
      ('registered', True, lconf_to_bool),
   ])

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   eq_(default_lconf_obj.key_order, ['first', 'last', 'sex', 'age', 'salary', 'favorites', 'registered'], msg=None)
   eq_(default_lconf_obj['favorites'].key_order, ['food', 'sport', 'color'], msg=None)
   eq_(default_lconf_obj['favorites'].key_empty_replacementvalue, {'sport': 'Not-Defined'}, msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(
      default_lconf_obj.key_order,
      ['#1', '#2', 'first', 'last', 'sex', 'age', 'salary', '#3', 'favorites', '#4', 'registered'],
      msg=None
   )
   eq_(default_lconf_obj['favorites'].key_order, ['food', 'sport', 'color'], msg=None)
   eq_(default_lconf_obj['favorites'].key_empty_replacementvalue, {'sport': 'Not-Defined'}, msg=None)


def test_lconf_prepare_default_obj__ok3():
   """ Tests: test_lconf_prepare_default_obj__ok3
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok3()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      ('executiontime', datetime.strptime('2014-05-08 13:39', '%Y-%m-%d %H:%M'), lconf_to_datetime),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   eq_(type(default_lconf_obj['executiontime']), datetime, msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(type(default_lconf_obj['executiontime']), datetime, msg=None)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__ok4():
   """ Tests: test_lconf_prepare_default_obj__ok4
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok4()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      ('conf_path', '/home/test', lconf_to_pathexpanduser),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(type(default_lconf_obj['conf_path']), str, msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__ok5():
   """ Tests: test_lconf_prepare_default_obj__ok5
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok5()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      ('other type', set()),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)


def test_lconf_prepare_default_obj__ok6():
   """ Tests: test_lconf_prepare_default_obj__ok6
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok6()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      ('RepeatedBlk1', BlkI(-1, -1,
         Blk([
            ('MyKey1', ''),
            ('MyKey2', '', None, 'Not-Defined'),
         ])
      )),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   eq_(default_lconf_obj['RepeatedBlk1'], {}, msg=None)

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(default_lconf_obj, {'RepeatedBlk1': {}, '#1': ''}, msg=None)


# noinspection PyUnusedLocal
def test_lconf_prepare_default_obj__ok7():
   """ Tests: test_lconf_prepare_default_obj__ok7
   """
   print('::: TEST: test_lconf_prepare_default_obj__ok7()')

   # noinspection PySetFunctionToLiteral
   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      ('other type', set({'1', '2'})),
   ])
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)
   ok_(isinstance(default_lconf_obj['other type'], set), msg=None)
   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)


def test_lconf_prepare_default_obj__baseexample_ok():
   """ Tests: test_lconf_prepare_default_obj__baseexample_ok
   """
   print('::: TEST: test_lconf_prepare_default_obj__baseexample_ok()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)

   eq_(default_lconf_obj.key_empty_replacementvalue, {'key7value_pair': -94599.5, 'key1value_pair': 'NOT-DEFINED'}, msg=None)
   eq_(
      default_lconf_obj.key_order,
      [
         'key1value_pair',
         'key2value_pair',
         'key3value_pair',
         'key4value_pair',
         'key5value_pair',
         'key6value_pair',
         'key7value_pair',
         'key8value_pair',
         'key9value_pair',
         'key10value_mapping',
         'key11value_mapping',
         'key12list',
         'key13value_pairlist',
         'key14list_of_color_tuples',
         'key15value_pairlist',
         'key16value_pairlist',
         'key17list_of_tuples',
         'RepeatedBlk1',
      ],
      msg=None
   )

   eq_(default_lconf_obj['key10value_mapping'].key_empty_replacementvalue, {}, msg=None)
   eq_(
      default_lconf_obj['key10value_mapping'].key_order,
      [
         'mapping10_key1',
         'mapping10_key2',
         'mapping10_key3',
         'mapping10_key4_list',
         'mapping10_key5_list',
         'mapping10_key6_list',
         'mapping10_key7_list'
      ],
      msg=None
   )

   eq_(default_lconf_obj['key1value_pair'], 'NOT-DEFINED', msg=None)
   eq_(default_lconf_obj['key7value_pair'], -94599.5, msg=None)

   eq_(default_lconf_obj['key10value_mapping']['mapping10_key7_list'].column_names, ('name', 'b', 'c'), msg=None)
   eq_(default_lconf_obj['key11value_mapping']['mapping11_key2_mapping'].key_empty_replacementvalue, {}, msg=None)
   eq_(
      default_lconf_obj['key11value_mapping']['mapping11_key2_mapping'].key_order,
      [
         'mapping11_key2_nested_mapping_key1',
         'mapping11_key2_nested_mapping_key2_block_identifier',
         'mapping11_key2_nested_mapping_key3',
         'mapping11_key2_nested_mapping_key4_list'
      ],
      msg=None
   )

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=True)
   eq_(
      default_lconf_obj.key_order,
      [
         '#1',
         '#2a',
         '#2b',
         'key1value_pair',
         '#3',
         'key2value_pair',
         '#4',
         'key3value_pair',
         'key4value_pair',
         'key5value_pair',
         'key6value_pair',
         '#5a',
         '#5b',
         'key7value_pair',
         'key8value_pair',
         'key9value_pair',
         '#6',
         '#7',
         'key10value_mapping',
         '#16',
         '#17',
         'key11value_mapping',
         '#28',
         '#29',
         'key12list',
         '#30',
         '#31',
         'key13value_pairlist',
         '#32',
         '#33',
         'key14list_of_color_tuples',
         '#34',
         '#35',
         'key15value_pairlist',
         '#36',
         '#37',
         'key16value_pairlist',
         '#38',
         '#39',
         'key17list_of_tuples',
         '#40',
         '#41',
         'RepeatedBlk1',
      ],
      msg=None
   )
   eq_(default_lconf_obj['key1value_pair'], 'NOT-DEFINED', msg=None)
   eq_(default_lconf_obj['key7value_pair'], -94599.5, msg=None)

   eq_(default_lconf_obj['key10value_mapping']['mapping10_key7_list'].column_names, ('name', 'b', 'c'), msg=None)
   eq_(default_lconf_obj['key11value_mapping']['mapping11_key2_mapping'].key_empty_replacementvalue, {}, msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_prepare_default_obj__ok0()
   test_lconf_prepare_default_obj__ok1()
   test_lconf_prepare_default_obj__ok2()
   test_lconf_prepare_default_obj__ok3()
   test_lconf_prepare_default_obj__ok4()
   test_lconf_prepare_default_obj__ok5()
   test_lconf_prepare_default_obj__ok6()
   test_lconf_prepare_default_obj__ok7()

   test_lconf_prepare_default_obj__baseexample_ok()

