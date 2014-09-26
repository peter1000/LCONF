""" tests extraction of LCONF-Sections
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

from LCONF.main_code import (
   lconf_extract_all_sections,
   lconf_extract_one_section_by_name,
   lconf_section_splitlines
)
from LCONF.utils import Err


def test_extract_lconf_multiple():
   """ Tests: test_extract_lconf_multiple
   """
   print('::: TEST: test_extract_lconf_multiple()')

   example_lconf_section_str1 = r'''
some text outside

more text

___SECTION :: EXAMPLE 1
first :: John
last :: Doe
sex :: M
age :: 39
salary :: 70000
# Comment-Line: `Key-Value-List`
- interests
   Reading
   Mountain Biking
   Hacking
registered :: True
___END

more text

___SECTION :: EXAMPLE 2
first :: Mary
last :: Lucia
sex :: W
___END

any other text
'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str1)
   len_all_sections = len(all_sections)
   eq_(len_all_sections, 2, msg=None)


@nose_raises(Err)
def test_extract_lconf_wrong_end_tag_in_section_expect_failure():
   """ Tests: test_extract_lconf_wrong_end_tag_in_section_expect_failure (missing start tag)
   """
   print('::: TEST: test_extract_lconf_wrong_end_tag_in_section_expect_failure()')

   example_lconf_section_str1 = r'''
some text outside

more text
___SECTION :: EXAMPLE 1
first :: John
last :: Doe
sex :: M
age :: 39
salary :: 70000
# Comment-Line: `Key-Value-List`
- interests
   Reading
   Mountain Biking
   Hacking
registered :: True
___END

more text
country :: Italy

 ____END

any other text
'''
   lconf_extract_all_sections(example_lconf_section_str1)


@nose_raises(Err)
def test_extract_lconf_wrong_start_tag_in_section_expect_failure():
   """ Tests: test_extract_lconf_wrong_start_tag_in_section_expect_failure (missing start tag)
   """
   print('::: TEST: test_extract_lconf_wrong_start_tag_in_section_expect_failure()')

   example_lconf_section_str1 = r'''
some text outside

more text

___SECTION :: EXAMPLE 1
first :: John
last :: Doe
sex :: M
age :: 39
salary :: 70000
# Comment-Line: `Key-Value-List`
- interests
   Reading
   Mountain Biking
   Hacking
registered :: True

more text

___SECTION :: EXAMPLE 2
first :: Mary
last :: Lucia
sex :: W
___END

any other text
'''
   lconf_extract_all_sections(example_lconf_section_str1)


def test_extract_lconf_section_splitlines1():
   """ Tests: extract LCONF Section and lconf_section_splitlines validate_first_line
   """
   print('::: TEST: test_extract_lconf_section_splitlines1()')
   example_lconf_section_str = r'''

any info text outside of a section



___SECTION :: Example

# Comment-Line: below: Main `Key :: Value Pair`
key1value_pair :: value1
# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
key2value_pair ::
key3value_pair ::
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ  翻訳する μεταφράζω


# Comment-Line: below is a Main `Key-Value-Mapping`
. key10value_mapping
   # Comment-Line:  Key-Value-Mapping items: are `Key :: Value Pairs`
   mapping10_key1 :: False
   mapping10_key2 :: true
   mapping10_key3 :: 123456

   # Comment-Line:  Key-Value-Mapping item: `Key :: Value-List`
   - mapping10_key4_list :: 1,2

   # Comment-Line:  Key-Value-Mapping item: `Key-Value-List`
   - mapping10_key5_list
      1
      2

   # Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`
   - mapping10_key6_list |x|y|
      1,3
      2,6

   # Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`
   - mapping10_key7_list |a|b|c|
      1,2.0,3
      2,4.0,6
___END

empty section next
___SECTION :: EMPTY_EXAMPLE
___END


empty section next
___SECTION :: MYSection
test :: No
___END
'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str)
   for section in all_sections:
      lconf_section_splitlines(section, validate_first_line=True)


@nose_raises(Err)
def test_extract_lconf_section_splitlines_expect_failure1():
   """ Tests: test_extract_lconf_section_splitlines_expect_failure1
   """
   print('::: TEST: test_extract_lconf_section_splitlines_expect_failure1()')
   example_lconf_section_str = r'''___SECTION ::  EXAMPLE
test :: No
___END
'''
   lconf_section_splitlines(example_lconf_section_str, validate_first_line=True)


@nose_raises(Err)
def test_extract_lconf_section_splitlines_expect_failure2():
   """ Tests: test_extract_lconf_section_splitlines_expect_failure2
   """
   print('::: TEST: test_extract_lconf_section_splitlines_expect_failure2()')
   example_lconf_section_str = r'''___SECTION ::BadSection
test :: No
___END
'''
   lconf_section_splitlines(example_lconf_section_str, validate_first_line=True)


@nose_raises(Err)
def test_lconf_extract_one_section_by_name_expect_failure1():
   """ Tests: test_lconf_extract_one_section_by_name_expect_failure1
   """
   print('::: TEST: test_lconf_extract_one_section_by_name_expect_failure1()')
   example_lconf_section_str = r'''___SECTION :: BASE_EXAMPLE
test :: No
___END
'''
   section_txt = lconf_extract_one_section_by_name(example_lconf_section_str, 'WrongSectionName')
   print(section_txt)


def test_lconf_extract_one_section_by_name_from_multi_section():
   """ Tests: test_lconf_extract_one_section_by_name_from_multi_section
   """
   print('::: TEST: test_lconf_extract_one_section_by_name_from_multi_section()')
   example_lconf_section_str = r'''some unrelated text

___SECTION :: BASE_EXAMPLE1
test :: No
___END

more unrelated text

___SECTION :: MySection
test :: No
___END

more unrelated text

___SECTION :: BASE_EXAMPLE2
test :: No
___END
'''
   section_txt = lconf_extract_one_section_by_name(example_lconf_section_str, 'MySection')
   print(section_txt)


# noinspection PyUnusedLocal
@nose_raises(ValueError)
def test_extract_lconf_missing_tags_expect_failure1():
   """ Tests: test_extract_lconf_missing_tags_expect_failure1
   """
   print('::: TEST: test_extract_lconf_missing_tags_expect_failure1()')

   example_lconf_section_str1 = r'''
___END'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str1)


# noinspection PyUnusedLocal
@nose_raises(ValueError)
def test_extract_lconf_missing_tags_expect_failure2():
   """ Tests: test_extract_lconf_missing_tags_expect_failure2
   """
   print('::: TEST: test_extract_lconf_missing_tags_expect_failure2()')

   example_lconf_section_str1 = r'''
___SECTION :: Test Example1'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str1)


# noinspection PyUnusedLocal
@nose_raises(ValueError)
def test_extract_lconf_missing_tags_expect_failure3():
   """ Tests: test_extract_lconf_missing_tags_expect_failure3
   """
   print('::: TEST: test_extract_lconf_missing_tags_expect_failure3()')

   example_lconf_section_str1 = r'''
missing both tags'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str1)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_extract_lconf_multiple()
   test_extract_lconf_wrong_end_tag_in_section_expect_failure()
   test_extract_lconf_wrong_start_tag_in_section_expect_failure()

   test_extract_lconf_section_splitlines1()
   test_extract_lconf_section_splitlines_expect_failure1()
   test_extract_lconf_section_splitlines_expect_failure2()

   test_lconf_extract_one_section_by_name_expect_failure1()
   test_lconf_extract_one_section_by_name_from_multi_section()

   test_extract_lconf_missing_tags_expect_failure1()
   test_extract_lconf_missing_tags_expect_failure2()
   test_extract_lconf_missing_tags_expect_failure3()
