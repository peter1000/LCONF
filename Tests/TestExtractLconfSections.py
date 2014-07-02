""" tests extraction of LCONF-Sections
"""
from inspect import (
   getfile,
   currentframe
)
from os.path import (
   abspath,
   dirname,
   join
)
from sys import path as syspath

from nose import tools


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import (
   lconf_extract_all_sections,
   lconf_extract_one_section_by_name,
   lconf_section_splitlines
)
from LCONF.ProjectErr import Err


def test_extract_lconf_multiple():
   """ Tests: extraction of multiple LCONF-Sections
   """
   print('::: TEST: test_extract_lconf_multiple()')

   example_lconf_section_str1 = r'''
some text outside

more text
___SECTION :: PERSON
age :: 39
- favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
registered :: true
salary :: 70000
sex :: M
___END

more text

___SECTION :: TEST
country :: Italy
- Cars
   Car0
      price :: 1000

___END

any other text
'''
   all_sections = lconf_extract_all_sections(example_lconf_section_str1)
   len_all_sections = len(all_sections)
   tools.eq_(len_all_sections, 2, msg='Expected 2 extracted LCONF-sections found: <{}>'.format(len_all_sections))


@tools.raises(Err)
def test_extract_lconf_wrong_end_tag_in_section_expect_failure():
   """ Tests: extract LCONF wrong END-TAG in Section (expect failure)
   """
   print('::: TEST: test_extract_lconf_wrong_end_tag_in_section_expect_failure()')

   example_lconf_section_str1 = r'''
some text outside



more text
___SECTION :: PERSON
age :: 39
- favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
registered :: true
salary :: 70000
sex :: M
___END

more text
 :: TEST
country :: Italy
- Cars
   Car0
      price :: 1000

 ____END

any other text
'''
   lconf_extract_all_sections(example_lconf_section_str1)


@tools.raises(Err)
def test_extract_lconf_wrong_start_tag_in_section_expect_failure():
   """ Tests: extract LCONF wrong START-TAG in Section (expect failure)
   """
   print('::: TEST: test_extract_lconf_wrong_start_tag_in_section_expect_failure()')

   example_lconf_section_str1 = r'''
some text outside



more text
___SECTION :: PERSON
age :: 39
- favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
registered :: true
salary :: 70000
sex :: M
___SECTION

more text
 :: TEST
country :: Italy
- Cars
   Car0
      price :: 1000

 ____END

any other text
'''
   lconf_extract_all_sections(example_lconf_section_str1)


def test_extract_lconf_section_splitlines1():
   """ Tests: extract LCONF Section and lconf_section_splitlines validate_first_line
   """
   print('::: TEST: test_extract_lconf_section_splitlines1()')
   example_lconf_section_str = r'''

any info text outside of a section


___SECTION :: BASE_EXAMPLE

key1value_pair :: value1
# Comment-Line: below is a Key :: Value Pair with an empty string value
key2value_pair ::
key3value_pair :: 1234
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: false
key10value_pair :: []

# Comment-Line: below is a Key-Value-List using indentation
key11list
   # Comment:  List item
   value_list_item1
   value_list_item2

# Comment-Line: below is a Key-Value-List using key/value pair separator
key12value_pairlist :: [value_list_item1,value_list_item2]
key13value_pairlist :: []

# Comment: Repeated List-Block Identifier: this will keep the order of the `Repeated Block-Names` after parsing
- RepeatedBlk1

   # Comment: Repeated Block-Name
   BLK_OBJ1
      # Comment: Repeated Block-Key: is a Key :: Value Pair with an empty string value
      BLK_key1 ::
      BLK_key2 :: 789
      BLK_key3 :: True
      BLK_key4 :: False
      BLK_key5list
         # Comment: Repeated List-Block Item
         BLK_value_list_item1
         BLK_value_list_item2
      BLK_key6list :: [1,2,3]
      BLK_key7list :: []
   # Comment: Repeated Block-Name
   BLK_OBJ2
      BLK_key1 :: None
      BLK_key2 :: 9856
      BLK_key3 :: true
      BLK_key4 :: false
      BLK_key5list
         # Comment: Repeated List-Block Item
         BLK_value_list_item1
         BLK_value_list_item2
      BLK_key6list :: [4566,987]
      BLK_key7list :: []

# Comment: Repeated Mapping-Block Identifier: this will loose the order of the `Repeated Block-Names` after parsing
* RepeatedBlk2
   # Comment: Repeated Block-Name
   BLK_OBJ1
      # Comment: Repeated Block-Key: is a Key :: Value Pair with an empty string value
      MyKey1 ::
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: True
      MyKey5list
         # Comment: Repeated List-Block Item
         BLK_value_list_item1
         BLK_value_list_item2
      MyKey6list :: [8]
      MyKey7list :: []
   # Comment: Repeated Block-Name
   BLK_OBJ2
      MyKey1 :: []
      MyKey2 :: 123456.99
      MyKey3 :: False
      MyKey4 :: []
      MyKey5list
         # Comment: Repeated List-Block Item
         BLK_value_list_item1
         BLK_value_list_item2
      # Comment: Repeated List-Block Item: one line
      MyKey6list :: [1258,684,456]
      MyKey7list :: []

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


@tools.raises(Err)
def test_extract_lconf_section_splitlines_expect_failure1():
   """ Tests: lconf_section_splitlines validate_first_line <TOO MANY SPACES around :: >   (expect failure)
   """
   print('::: TEST: test_extract_lconf_section_splitlines_expect_failure1()')
   example_lconf_section_str = r'''___SECTION ::  BASE_EXAMPLE
test :: No
___END
'''
   lconf_section_splitlines(example_lconf_section_str, validate_first_line=True)


@tools.raises(Err)
def test_extract_lconf_section_splitlines_expect_failure2():
   """ Tests: lconf_section_splitlines validate_first_line <FIRST LINE ERROR: Must start with ___SECTION :: >   (expect failure)
   """
   print('::: TEST: test_extract_lconf_section_splitlines_expect_failure2()')
   example_lconf_section_str = r'''___SECTION ::BadSection
test :: No
___END
'''
   lconf_section_splitlines(example_lconf_section_str, validate_first_line=True)


@tools.raises(Err)
def test_lconf_extract_one_section_by_name_expect_failure1():
   """ Tests: test_lconf_extract_one_section_by_name_expect_failure1  (expect failure)
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


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
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
