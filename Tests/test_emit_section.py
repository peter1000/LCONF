""" tests test emit section
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
   eq_,
   raises as nose_raises
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.lconf_structure_classes import (
   KVList,
   Root,
   ListOT,
)
from LCONF.main_code import (
   LCONF_DEFAULT,
   LCONF_NO,
   LCONF_YES,
   lconf_emit,
   lconf_prepare_default_obj,
   lconf_parse_section_extract_by_name,
)
from LCONF.transform import (
   lconf_to_int,
   lconf_to_float,
)
from LCONF.utils import Err

# noinspection PyUnresolvedReferences
from base_examples import (
   get_lconf_section__base_example_template_obj,
   get_lconf_section__base_example_lconf_section_raw_str,
)


def test_lconf_emit_ok0():
   """ Tests: test_lconf_emit_ok0
   """
   print('::: TEST: test_lconf_emit_ok0()')

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
# Comment-Line: `Key-Value-List`
- interests :: soccer,tennis
# Comment-Line: `Key :: Value Pair`
registered :: False
___END'''

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(lconf_section_raw_str, emit_result, msg=None)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   eq_(lconf_obj, reparsed_lconf_obj, msg=None)
   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(lconf_section_raw_str, re_emit_result, msg=None)


def test_lconf_emit_ok1():
   """ Tests: test_lconf_emit_ok1
   """
   print('::: TEST: test_lconf_emit_ok1()')

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

   lconf_section_raw_str = r'''___SECTION :: Test Example1

# Comment-Line: `Key :: Value Pair`
first :: Joe
last :: Smith
sex ::
age :: 18
salary :: 12500
# Comment-Line: `Key-Value-List`
- interests :: soccer,tennis
# Comment-Line: `Key :: Value Pair`
registered :: False
___END'''

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(lconf_section_raw_str, emit_result, msg=None)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   eq_(lconf_obj, reparsed_lconf_obj, msg=None)
   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(lconf_section_raw_str, re_emit_result, msg=None)


def test_lconf_emit_ok2():
   """ Tests: test_lconf_emit_ok2
   """
   print('::: TEST: test_lconf_emit_ok2()')

   lconf_section__template_obj = Root([
      # Default Empty Line
      ('#1', ''),
      # Default Comment Line
      ('#2', '# Comment-Line: `Key :: Value Pair`'),
      ('first', ''),
      ('last', ''),
      ('sex', '', None, 'NOT-DEFINED'),
      ('age', '', None, 25),
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
sex ::
age ::
salary :: 12500
# Comment-Line: `Key-Value-List`
- interests :: soccer,tennis
# Comment-Line: `Key :: Value Pair`
registered :: False
___END'''

   check_str = '''___SECTION :: Test Example1

# Comment-Line: `Key :: Value Pair`
first :: Joe
last :: Smith
sex :: NOT-DEFINED
age :: 25
salary :: 12500
# Comment-Line: `Key-Value-List`
- interests :: soccer,tennis
# Comment-Line: `Key :: Value Pair`
registered :: False
___END'''

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=False)
   eq_(check_str, emit_result, msg=None)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'Test Example1',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=False)
   eq_(check_str, re_emit_result, msg=None)


def test_lconf_emit_ok3():
   """ Tests: test_lconf_emit_ok3
   """
   print('::: TEST: test_lconf_emit_ok3()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


def test_lconf_emit_ok4():
   """ Tests: test_lconf_emit_ok4
   """
   print('::: TEST: test_lconf_emit_ok4()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


def test_lconf_emit_ok5():
   """ Tests: test_lconf_emit_ok5
   """
   print('::: TEST: test_lconf_emit_ok5()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


def test_lconf_emit_ok6():
   """ Tests: test_lconf_emit_ok6
   """
   print('::: TEST: test_lconf_emit_ok6()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


def test_lconf_emit_ok7():
   """ Tests: test_lconf_emit_ok7
   """
   print('::: TEST: test_lconf_emit_ok7()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


def test_lconf_emit_ok8():
   """ Tests: test_lconf_emit_ok8
   """
   print('::: TEST: test_lconf_emit_ok8()')

   lconf_section__template_obj = get_lconf_section__base_example_template_obj()
   lconf_section_raw_str = get_lconf_section__base_example_lconf_section_raw_str()

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)
   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'BaseEXAMPLE',
      lconf_section__template_obj,
      with_comments=False,
      validate=True
   )

   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


# noinspection PyUnusedLocal
def test_lconf_emit_ok9():
   """ Tests: test_lconf_emit_ok9
   """
   print('::: TEST: test_lconf_emit_ok9()')

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

      ('#4', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples4', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ])),

      ('#5', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples5', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ], column_replace_missing=('-1.0', '-1.0', '-1.0'))),

      ('#6', '# Comment-Line: using one transform function for all'),
      ('list_of_tuples6', ListOT(('a', 'b', 'c'), [
         ('1.0', '2.0', '3.0'),
         ('44.0', '55.0', '66.0')
      ], column_replace_missing=('-1.0', '-1.0', '-1.0')), (lconf_to_float, lconf_to_float, lconf_to_float)),
   ])

   lconf_section_raw_str = r'''___SECTION :: TestExample
# Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|
- list_of_color_tuples |Color Name|Red|Green|Blue|
   forestgreen,34,139,34
   brick,156,102,31
# Comment-Line: below is a Main `List-Of-Tuples` with 3 columns: |a|b|c|
- list_of_tuples2 |a|b|c|
   100,200,300
   400,500,600
# Comment-Line: using one transform function for all
- list_of_tuples3 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0,600.0
# Comment-Line: using one transform function for all
- list_of_tuples4 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0,600.0
# Comment-Line: using one transform function for all
- list_of_tuples5 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0
# Comment-Line: using one transform function for all
- list_of_tuples6 |a|b|c|
   100.0,,300.0
   400.0,500.0,600.0
___END'''

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_DEFAULT)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   eq_(lconf_obj, reparsed_lconf_obj, msg=None)
   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   eq_(lconf_obj, reparsed_lconf_obj, msg=None)
   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_NO, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)

   lconf_obj = lconf_parse_section_extract_by_name(
      lconf_section_raw_str,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   emit_result = lconf_emit(lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)

   reparsed_lconf_obj = lconf_parse_section_extract_by_name(
      emit_result,
      'TestExample',
      lconf_section__template_obj,
      with_comments=True,
      validate=True
   )

   eq_(lconf_obj, reparsed_lconf_obj, msg=None)
   re_emit_result = lconf_emit(reparsed_lconf_obj, onelinelists=LCONF_YES, empty_key_value_pair=True)
   eq_(emit_result, re_emit_result, msg=None)


@nose_raises(Err)
def test_lconf_emit_expect_failure1():
   """ Tests: test_lconf_emit_expect_failure1
   """
   print('::: TEST: test_lconf_emit_expect_failure1()')

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
# Comment-Line: `Key-Value-List`
- interests :: soccer,tennis
# Comment-Line: `Key :: Value Pair`
registered :: False
___END'''

   default_lconf_obj = lconf_prepare_default_obj(lconf_section__template_obj, with_comments=False)

   emit_result = lconf_emit(default_lconf_obj, onelinelists=LCONF_DEFAULT, empty_key_value_pair=True)
   eq_(lconf_section_raw_str, emit_result, msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_emit_ok0()
   test_lconf_emit_ok1()
   test_lconf_emit_ok2()
   test_lconf_emit_ok3()
   test_lconf_emit_ok4()
   test_lconf_emit_ok5()
   test_lconf_emit_ok6()
   test_lconf_emit_ok7()
   test_lconf_emit_ok8()

   test_lconf_emit_ok9()

   test_lconf_emit_expect_failure1()



