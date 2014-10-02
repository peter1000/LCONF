""" tests emit default lconf obj
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

from nose.tools import (
   eq_
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.lconf_structure_classes import (
   KVList,
   KVMap,
   Root,
)
from LCONF.main_code import (
   LCONF_DEFAULT,
   LCONF_NO,
   LCONF_YES,
   lconf_emit_default_obj,
   lconf_section_splitlines,
   lconf_validate_one_section_str,
)
from LCONF.transform import (
   lconf_to_int,
   lconf_to_float,
)

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from base_examples import get_lconf_section__base_example_template_obj


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def test_lconf_emit_default_obj__ok0():
   """ Tests: test_lconf_emit_default_obj__ok0
   """
   print('::: TEST: test_lconf_emit_default_obj__ok0()')

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
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   eq_(section_lines[0], '___SECTION :: Test Example1', msg=None)
   # empty comment line
   eq_(section_lines[1], '', msg=None)
   eq_(section_lines[8], '# Comment-Line: `Key-Value-List`', msg=None)
   eq_(section_lines[9], '- interests ::', msg=None)
   eq_(section_lines[12], '___END', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)

   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_NO,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_YES,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=False
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_NO,
      with_comments=False
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_YES,
      with_comments=False
   )


def test_lconf_emit_default_obj__ok1():
   """ Tests: test_lconf_emit_default_obj__ok1
   """
   print('::: TEST: test_lconf_emit_default_obj__ok1()')

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
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=False
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   eq_(section_lines[0], '___SECTION :: Test Example1', msg=None)
   # empty multi line list: `Key :: Value-List`
   eq_(section_lines[6], '- interests ::', msg=None)
   eq_(section_lines[8], '___END', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def test_lconf_emit_default_obj__ok2():
   """ Tests: test_lconf_emit_default_obj__ok2
   """
   print('::: TEST: test_lconf_emit_default_obj__ok2()')

   lconf_section__template_obj = Root([
      ('first', ''),
      ('last', ''),
      ('sex', ''),
      ('age', ''),
      ('salary', ''),
      ('interests', KVList(False, [])),
      ('registered', ''),
   ])
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=False
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   eq_(section_lines[0], '___SECTION :: Test Example1', msg=None)
   # empty multi line list: `Key-Value-List`
   eq_(section_lines[6], '- interests', msg=None)
   eq_(section_lines[8], '___END', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)

   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_NO,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_YES,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_NO,
      with_comments=False
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_YES,
      with_comments=False
   )


def test_lconf_emit_default_obj__ok3():
   """ Tests: test_lconf_emit_default_obj__ok3
   """
   print('::: TEST: test_lconf_emit_default_obj__ok3()')

   lconf_section__template_obj = Root([
      ('first', 'Paul'),
      ('last', 'Smith'),
      ('sex', 'm'),
      ('age', '39', lconf_to_int),
      ('salary', '7000', lconf_to_float),
      ('interests', KVList(False, ['golf', 'reading', 'investments'])),
      ('registered', 'true'),
   ])
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Test Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=False
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)
   eq_(section_lines[0], '___SECTION :: Test Example1', msg=None)
   eq_(section_lines[4], 'age :: 39', msg=None)
   eq_(section_lines[6], '- interests', msg=None)
   eq_(section_lines[7], '   golf', msg=None)
   eq_(section_lines[10], 'registered :: true', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)


def test_lconf_emit_default_obj__ok4():
   """ Tests: test_lconf_emit_default_obj__ok4
   """
   print('::: TEST: test_lconf_emit_default_obj__ok4()')

   lconf_section__template_obj = Root([
      ('interests', KVList(False, ['golf', 'reading', 'investments'])),
   ])
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_YES,
      with_comments=False
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   eq_(section_lines[1], '- interests :: golf,reading,investments', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)


def test_lconf_emit_default_obj__ok5():
   """ Tests: test_lconf_emit_default_obj__ok5
   """
   print('::: TEST: test_lconf_emit_default_obj__ok5()')

   lconf_section__template_obj = Root([
      ('interests', KVList(True, ['golf', 'reading', 'investments'])),
   ])
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_NO,
      with_comments=False
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   eq_(section_lines[1], '- interests', msg=None)
   eq_(section_lines[2], '   golf', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)


def test_lconf_emit_default_obj__ok6():
   """ Tests: test_lconf_emit_default_obj__ok6
   """
   print('::: TEST: test_lconf_emit_default_obj__ok6()')

   lconf_section__template_obj = Root([
      ('keyvalue_mapping', KVMap([
         ('#1', '# Comment-Line:  Key-Value-Mapping items: `Key :: Value Pairs`'),
         ('mapping_key1', 'Some long sentence'),
      ])),
   ])
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_NO,
      with_comments=True
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   eq_(section_lines[1], '. keyvalue_mapping', msg=None)
   eq_(section_lines[3], '   mapping_key1 :: Some long sentence', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def test_lconf_emit_default_obj__ok7():
   """ Tests: test_lconf_emit_default_obj__ok7
   """
   print('::: TEST: test_lconf_emit_default_obj__ok7()')

   # Main `Section-Template OBJ: type: Root
   lconf_section__template_obj = get_lconf_section__base_example_template_obj()

   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=True)
   eq_(section_lines[23], '   - mapping10_key4_list :: 555,9999', msg=None)
   eq_(section_lines[97], '            nested_mapping_key1 :: franz', msg=None)
   eq_(section_lines[107], '                  - block-item_key3_list |name|height|weight|', msg=None)

   lconf_validate_one_section_str(lconf_section_raw_str)

   section_lines, section_name = lconf_section_splitlines(lconf_section_raw_str, validate_first_line=False)

   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_NO,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_YES,
      with_comments=True
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_DEFAULT,
      with_comments=False
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_NO,
      with_comments=False
   )
   lconf_section_raw_str = lconf_emit_default_obj(
      lconf_section__template_obj,
      'Example1',
      onelinelists=LCONF_YES,
      with_comments=False
   )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_emit_default_obj__ok0()
   test_lconf_emit_default_obj__ok1()
   test_lconf_emit_default_obj__ok2()
   test_lconf_emit_default_obj__ok3()
   test_lconf_emit_default_obj__ok4()
   test_lconf_emit_default_obj__ok5()

   test_lconf_emit_default_obj__ok6()

   test_lconf_emit_default_obj__ok7()
