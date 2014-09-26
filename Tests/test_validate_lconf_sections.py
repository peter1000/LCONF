""" tests validation of LCONF-Sections
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

from nose.tools import raises as nose_raises


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.main_code import (
   lconf_validate_file,
   lconf_validate_one_section_str,
   lconf_validate_source
)
from LCONF.utils import Err


def test_validate_file__ok0():
   """ Tests: test_validate_file__ok0
   """
   print('::: TEST: test_validate_file__ok0()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate0.lconf')
   lconf_validate_file(path_to_lconf_file)


def test_validate_file__multi_sections__ok1():
   """ Tests: test_validate_file__multi_sections__ok1
   """
   print('::: TEST: test_validate_file__multi_sections__ok1()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_multi_sections_1.lconf')
   lconf_validate_file(path_to_lconf_file)


@nose_raises(Err)
def test_validate_file__expect_failure1():
   """ Tests: test_validate_file__expect_failure1
   """
   print('::: TEST: test_validate_file__expect_failure1()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err1.lconf')
   lconf_validate_file(path_to_lconf_file)


@nose_raises(Err)
def test_validate_file__expect_failure2():
   """ Tests: test_validate_file__expect_failure2
   """
   print('::: TEST: test_validate_file__expect_failure2()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err2.lconf')
   lconf_validate_file(path_to_lconf_file)


@nose_raises(Err)
def test_validate_file__expect_failure3():
   """ Tests: test_validate_file__expect_failure3
   """
   print('::: TEST: test_validate_file__expect_failure3()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err3.lconf')
   lconf_validate_file(path_to_lconf_file)


@nose_raises(Err)
def test_validate_file__expect_failure4():
   """ Tests: test_validate_file__expect_failure4
   """
   print('::: TEST: test_validate_file__expect_failure4()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'example_to_validate_with_err4.lconf')
   lconf_validate_file(path_to_lconf_file)


@nose_raises(Err)
def test_validate_file__expect_failure5():
   """ Tests: test_validate_file__expect_failure5
   """
   print('::: TEST: test_validate_file__expect_failure5()')
   path_to_lconf_file = path_join(SCRIPT_PATH, 'notexisting.lconf')
   lconf_validate_file(path_to_lconf_file)


def test_lconf_validate_str__empty_lines_around_comments():
   """ Tests: test_lconf_validate_str__empty_lines_around_comments
   """
   print('::: TEST: test_lconf_validate_str__empty_lines_around_comments()')
   example_lconf_section_str1 = r'''___SECTION :: Example

# Comment-Line: below: Main `Key :: Value Pair`

key1value_pair :: value1


. mapping
   # Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
   1 :: 5



   # Comment1
   # Comment2

   2 :: s

___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__comments_indent__expect_failure1():
   """ Tests: test_lconf_validate_str__comments_indent__expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__comments_indent__expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example

# Comment-Line: below: Main `Key :: Value Pair`

key1value_pair :: value1


. mapping
   # Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
   1 :: 5

   # Comment1
    # Comment2

   2 :: s

___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__comments_indent__expect_failure2():
   """ Tests: test_lconf_validate_str__comments_indent__expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__comments_indent__expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example

   # Comment-Line: below: Main `Key :: Value Pair`

key1value_pair :: value1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__indent_expect_failure1():
   """ Tests: test_lconf_validate_str__indent_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__indent_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
key1value_pair :: value1
 key2value_pair ::

___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__indent_expect_failure2():
   """ Tests: test_lconf_validate_str__indent_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__indent_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example

# Comment-Line: below: Main `Key :: Value Pair`
key1value_pair :: value1
# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
key2value_pair ::
 - list
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__indent_expect_failure3():
   """ Tests: test_lconf_validate_str__indent_expect_failure3
   """
   print('::: TEST: test_lconf_validate_str__indent_expect_failure3()')
   example_lconf_section_str1 = r'''___SECTION :: Example
   key1value_pair :: value1
key2value_pair ::
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__indent_expect_failure4():
   """ Tests: test_lconf_validate_str__indent_expect_failure4
   """
   print('::: TEST: test_lconf_validate_str__indent_expect_failure4()')
   example_lconf_section_str1 = r'''___SECTION :: Example

# Comment-Line: below is a Main `Key-Value-Mapping`
. key11value_mapping
   # Comment-Line:  Key-Value-Mapping item: `Key :: Value Pairs`
   mapping11_key1 :: null

   # Comment-Line:  Key-Value-Mapping item: an other nested `Key-Value-Mapping`
   . mapping11_key2_mapping
      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`
      mapping11_key2_nested_mapping_key1 :: city

      # Comment-Line:  nested Key-Value-Mapping item: `Repeated-Block-Identifier`
      * mapping11_key2_nested_mapping_key2_block_identifier

         # Comment-Line: `Block-Name1`
         sky_blue_blk_name1
            # Comment-Line:  Block items: `Key :: Value Pairs`
            blk_item_red :: 135
            blk_item_green :: 206
            blk_item_blue :: 235

         # Comment-Line: `Block-Name2`
         lavender_blk_name2
            # Comment-Line:  Block items: `Key :: Value Pairs`
            blk_item_red :: 230
            blk_item_green :: 230
            blk_item_blue :: 250

      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`
      mapping11_key2_nested_mapping_key3 :: car

      # Comment-Line: nested Key-Value-Mapping item: `Key-Value-List`
      - mapping11_key2_nested_mapping_key4_list
         # Comment-Line: List item
         value_list_item1
         value_list_item2

 wrong1 ::
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__list_identifier_expect_failure1():
   """ Tests: test_lconf_validate_str__list_identifier_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__list_identifier_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
-  mylist ::
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__list_identifier_expect_failure2():
   """ Tests: test_lconf_validate_str__list_identifier_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__list_identifier_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example
-mylist ::
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__mapping_identifier_expect_failure1():
   """ Tests: test_lconf_validate_str__mapping_identifier_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__mapping_identifier_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
.  mapping
   key :: value
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__mapping_identifier_expect_failure2():
   """ Tests: test_lconf_validate_str__mapping_identifier_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__mapping_identifier_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example
.mapping
   key :: value
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__block_identifier_expect_failure1():
   """ Tests: test_lconf_validate_str__block_identifier_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__block_identifier_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
*  block
   person1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__block_identifier_expect_failure2():
   """ Tests: test_lconf_validate_str__block_identifier_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__block_identifier_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example
*block
   person1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__key_value_separator_expect_failure1():
   """ Tests: test_lconf_validate_str__key_value_separator_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__key_value_separator_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
key1 :: value1
key2  :: value2
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__key_value_separator_expect_failure2():
   """ Tests: test_lconf_validate_str__key_value_separator_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__key_value_separator_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: Example
key1 :: value1
key2 ::  value2
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__key_value_separator_expect_failure3():
   """ Tests: test_lconf_validate_str__key_value_separator_expect_failure3
   """
   print('::: TEST: test_lconf_validate_str__key_value_separator_expect_failure3()')
   example_lconf_section_str1 = r'''___SECTION :: Example
key1 :: value1
key2:: value2
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__key_value_separator_expect_failure4():
   """ Tests: test_lconf_validate_str__key_value_separator_expect_failure4
   """
   print('::: TEST: test_lconf_validate_str__key_value_separator_expect_failure4()')
   example_lconf_section_str1 = r'''___SECTION :: Example
key1 :: value1
key2 ::value2
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__firstline_key_value_separator_expect_failure1():
   """ Tests: test_lconf_validate_str__firstline_key_value_separator_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__firstline_key_value_separator_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION:: Example
key1 :: value1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__firstline_key_value_separator_expect_failure2():
   """ Tests: test_lconf_validate_str__firstline_key_value_separator_expect_failure2
   """
   print('::: TEST: test_lconf_validate_str__firstline_key_value_separator_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION ::  Example
key1 :: value1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__firstline_key_value_separator_expect_failure3():
   """ Tests: test_lconf_validate_str__firstline_key_value_separator_expect_failure3
   """
   print('::: TEST: test_lconf_validate_str__firstline_key_value_separator_expect_failure3()')
   example_lconf_section_str1 = r'''___SECTION : : Example
key1 :: value1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__lastline_expect_failure1():
   """ Tests: test_lconf_validate_str__lastline_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__lastline_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Example
- list
   1
   2
   ___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


def test_validate_source__multi_sections__ok1():
   """ Tests: test_validate_source__multi_sections__ok1
   """
   print('::: TEST: test_validate_source__multi_sections__ok1()')
   example_lconf_multiple_sections = r'''

Some text outside of any sections

___SECTION :: EXAMPLE 5 a
# Repeated-Block-Identifier
* categories
   # using `Block-Names`
   PHP
      test1_name :: One
      test1_score :: 90
      tests2_name :: Two
      tests2_score :: 96
   Node.js
      test1_name :: One
      test1_score :: 97
      tests2_name :: Two
      tests2_score :: 93
___END

more text

___SECTION :: EXAMPLE 5 b
# Repeated-Block-Identifier
* categories
   # using `Block-Names`
   PHP
      # Key-Value-Mapping
      . test1
         name :: One
         score :: 90
      . test2
         name :: Two
         score :: 96
   Node.js
      # Key-Value-Mapping
      . test1
         name :: One
         score :: 97
      . test2
         name :: Two
         score :: 93
___END

'''
   lconf_validate_source(example_lconf_multiple_sections)


@nose_raises(Err)
def test_lconf_validate_str__list_wrongitem_expect_failure1():
   """ Tests: test_lconf_validate_str__list_wrongitem_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__list_wrongitem_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
- list1
   1
   wrongkey :: value
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__list_wrongkeyvalueseparator_expect_failure1():
   """ Tests: test_lconf_validate_str__list_wrongkeyvalueseparator_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__list_wrongkeyvalueseparator_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
- list1 ::  1,2
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__listoftuples_wrongitem_expect_failure1():
   """ Tests: test_lconf_validate_str__listoftuples_wrongitem_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__listoftuples_wrongitem_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
- list_of_tuples4 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0,wrongkey :: value
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__listoftuples_wrongnumber_of_items_expect_failure1():
   """ Tests: test_lconf_validate_str__listoftuples_wrongnumber_of_items_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__listoftuples_wrongnumber_of_items_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
- list_of_tuples4 |a|b|c|
   100.0,200.0,300.0
   400.0,500.0
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__indent_too_much_expect_failure():
   """ Tests: test_lconf_validate_str__indent_too_much_expect_failure
   """
   print('::: TEST: test_lconf_validate_str__indent_too_much_expect_failure()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
. mapping
   - list
         3
         5
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@nose_raises(Err)
def test_lconf_validate_str__wrongblockname_expect_failure1():
   """ Tests: test_lconf_validate_str__wrongblockname_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__wrongblockname_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
* block1
   wrongblockname :: whatever
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


def test_lconf_validate_str__empty_mapping():
   """ Tests: test_lconf_validate_str__empty_mapping
   """
   print('::: TEST: test_lconf_validate_str__empty_mapping()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
. mapping
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


def test_lconf_validate_str__empty_block_identifier():
   """ Tests: test_lconf_validate_str__empty_block_identifier
   """
   print('::: TEST: test_lconf_validate_str__empty_block_identifier()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
* MyRepeating Block
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


def test_lconf_validate_str__empty_block_name():
   """ Tests: test_lconf_validate_str__empty_block_name
   """
   print('::: TEST: test_lconf_validate_str__empty_block_name()')
   example_lconf_section_str1 = r'''___SECTION :: Test Example1
* MyRepeating Block
   EmptyBlockName1
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


def test_lconf_validate_str__value_with_newline_chars():
   """ Tests: test_lconf_validate_str__empty_mapping_expect_failure1
   """
   print('::: TEST: test_lconf_validate_str__empty_mapping_expect_failure1()')

   example_lconf_section_str1 = r'''___SECTION :: Test Example1
key1 :: different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ  翻訳する μεταφράζω
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_validate_file__ok0()
   test_validate_file__multi_sections__ok1()
   test_validate_file__expect_failure1()
   test_validate_file__expect_failure2()
   test_validate_file__expect_failure3()
   test_validate_file__expect_failure4()
   test_validate_file__expect_failure5()

   test_lconf_validate_str__empty_lines_around_comments()
   test_lconf_validate_str__comments_indent__expect_failure1()
   test_lconf_validate_str__comments_indent__expect_failure2()

   test_lconf_validate_str__indent_expect_failure1()
   test_lconf_validate_str__indent_expect_failure2()
   test_lconf_validate_str__indent_expect_failure3()
   test_lconf_validate_str__indent_expect_failure4()

   test_lconf_validate_str__list_identifier_expect_failure1()
   test_lconf_validate_str__list_identifier_expect_failure2()

   test_lconf_validate_str__mapping_identifier_expect_failure1()
   test_lconf_validate_str__mapping_identifier_expect_failure2()

   test_lconf_validate_str__block_identifier_expect_failure1()
   test_lconf_validate_str__block_identifier_expect_failure2()

   test_lconf_validate_str__key_value_separator_expect_failure1()
   test_lconf_validate_str__key_value_separator_expect_failure2()
   test_lconf_validate_str__key_value_separator_expect_failure3()
   test_lconf_validate_str__key_value_separator_expect_failure4()

   test_lconf_validate_str__firstline_key_value_separator_expect_failure1()
   test_lconf_validate_str__firstline_key_value_separator_expect_failure2()
   test_lconf_validate_str__firstline_key_value_separator_expect_failure3()

   test_lconf_validate_str__lastline_expect_failure1()

   test_validate_source__multi_sections__ok1()

   test_lconf_validate_str__list_wrongitem_expect_failure1()
   test_lconf_validate_str__list_wrongkeyvalueseparator_expect_failure1()
   test_lconf_validate_str__listoftuples_wrongitem_expect_failure1()
   test_lconf_validate_str__listoftuples_wrongnumber_of_items_expect_failure1()

   test_lconf_validate_str__indent_too_much_expect_failure()

   test_lconf_validate_str__wrongblockname_expect_failure1()

   test_lconf_validate_str__empty_mapping()

   test_lconf_validate_str__empty_block_identifier()

   test_lconf_validate_str__empty_block_name()

   test_lconf_validate_str__value_with_newline_chars()
