""" tests validation of LCONF-Sections
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
   lconf_validate_file,
   lconf_validate_one_section_str,
   lconf_validate_source
)
from LCONF.ProjectErr import Err


@tools.raises(Err)
def test_lconf_validate_one_section_str_expect_failure1():
   """ Tests: test_lconf_validate_one_section_str_expect_failure1
   """
   print('::: TEST: test_lconf_validate_one_section_str_expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
 first :: John
last :: Doe
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@tools.raises(Err)
def test_lconf_validate_one_section_str_expect_failure2():
   """ Tests: test_lconf_validate_one_section_str_expect_failure2
   """
   print('::: TEST: test_lconf_validate_one_section_str_expect_failure2()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
 ___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@tools.raises(Err)
def test_lconf_validate_one_section_str_expect_failure3():
   """ Tests: test_lconf_validate_one_section_str_expect_failure3
   """
   print('::: TEST: test_lconf_validate_one_section_str_expect_failure3()')
   example_lconf_section_str1 = r''' ___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
___END
'''
   lconf_validate_one_section_str(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation0():
   """ Tests: test_validate_expect_failure__wrong_indentation0: MAIN `BLOCK`: Expected: <3>, <6> or <9> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation0()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
 first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation1():
   """ Tests: test_validate_expect_failure__wrong_indentation1: No previous: `MAIN Block`, `MAIN Key-Value-List` or `MAIN Key-Value-Mapping` (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation1()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
 age :: 39
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation2():
   """ Tests: test_validate_expect_failure__wrong_indentation2: <INDENTATION ERROR>  MAIN `BLOCK`: Expected: <3>, <6> or <9> spaces (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation2()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
     color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation3():
   """ Tests: test_validate_expect_failure__wrong_indentation3: MAIN `Key-Value-List`: Expected: <3> spaces: (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation3()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
   food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation4():
   """ Tests: test_validate_expect_failure__wrong_indentation4: INDENTATION LEVEL JUMP ERROR (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation4()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
      BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation5():
   """ Tests: test_validate_expect_failure__wrong_indentation5: MAIN `Key-Value-List`: Expected: <3> spaces (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation5()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
cars
   ford
   porsche
    bmw
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport
         Soccer
         Tennis
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_indentation6():
   """ Tests: test_validate_expect_failure__wrong_indentation6: MAIN `BLOCK`: Expected: <3>, <6> or <9> spaces (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_indentation6()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
cars
   ford
   porsche
   bmw
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport
         Soccer
          Tennis
first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator1():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator1: <MISSING SPACES before> (expect failure)

   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator1()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age:: 39
car :: bmw
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator2():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator2: <WRONG CHAR/SPACES before> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator2()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age  :: 39
car :: bmw
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator3():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator3: <WRONG SPACES after> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator3()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age ::  39
car :: bmw
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator4():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator4: <EXPECTED: EMPTY STRING or a space after> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator4()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age ::39
car :: bmw
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator5():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator5: wrong Key/Value Pair Separator 6 <TOO MANY SPACES around> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator5()')
   example_lconf_section_str1 = r'''___SECTION ::  PERSON
age :: 39
car :: bmw
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator6():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator6: BLK <MISSING SPACES before> (expect failure)

   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator6()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color:: Blue
      food :: Spaghetti
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator7():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator7: <WRONG CHAR/SPACES before> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator7()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color  :: Blue
      food :: Spaghetti
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator8():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator8: BLK <EXPECTED: EMPTY STRING or a space after> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator8()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color ::Blue
      food :: Spaghetti
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_key_value_separator9():
   """ Tests: test_validate_expect_failure__wrong_key_value_separator9: -> BLK <WRONG SPACES after> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_key_value_separator9()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color ::  Blue
      food :: Spaghetti
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__blk_identifier():
   """ Tests: test_validate_expect_failure__blk_identifier: BLK Identifier 1 <BLOCK IDENTIFIER NAME ERROR> (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__blk_identifier()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39
*  favorites
   BLK0
      color ::  Blue
      food :: Spaghetti
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_file__expect_failure():
   """ Tests: test_validate_file__expect_failure: BLK Identifier 1 <BLOCK IDENTIFIER NAME ERROR> (expect failure)
   """
   print('::: TEST: test_validate_file__expect_failure()')
   path_to_lconf_file = join(SCRIPT_PATH, 'example_to_validate1.lconf')
   lconf_validate_file(path_to_lconf_file)


def test_validate_file__ok():
   """ Tests: test_validate_file__ok
   """
   print('::: TEST: test_validate_file__ok()')
   path_to_lconf_file = join(SCRIPT_PATH, 'example_to_validate0.lconf')
   lconf_validate_file(path_to_lconf_file)


@tools.raises(Err)
def test_validate_expect_failure__wrong_commentline_indentation__expect_failure0():
   """ Tests: test_validate_expect_failure__wrong_commentline_indentation__expect_failure0: MAIN (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_commentline_indentation__expect_failure0()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39

* favorites
# Comment line 1
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
 first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


@tools.raises(Err)
def test_validate_expect_failure__wrong_commentline_indentation__expect_failure1():
   """ Tests: test_validate_expect_failure__wrong_commentline_indentation__expect_failure1: `BLOCK` (expect failure)
   """
   print('::: TEST: test_validate_expect_failure__wrong_commentline_indentation__expect_failure1()')
   example_lconf_section_str1 = r'''___SECTION :: PERSON
age :: 39

* favorites
   BLK0
   # Comment line 1
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
 first :: John
last :: Doe
___END
'''
   lconf_validate_source(example_lconf_section_str1)


def test_validate_empty_lines_after_key_value_mapping_or_list():
   """ Tests: test_validate_empty_lines_after_key_value_mapping_or_list
   """
   print('::: TEST: test_validate_empty_lines_after_key_value_mapping_or_list()')
   example_lconf_section_str1 = example_lconf_section_str = r'''___SECTION :: BaseEXAMPLE

# Comment-Line: below: Main `Key :: Value Pair`
key1value_pair :: value1
# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
key2value_pair ::
key3value_pair :: 1234
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: false

# Comment-Line: below is a Main `Key-Value-Mapping`
key10value_mapping





   # Comment-Line:  Key-Value-Mapping items: are `Key :: Value Pairs`
   mapping10_key1 :: null
   mapping10_key2 :: true
   mapping10_key3 :: 123456


   mapping10_key4 :: False
   mapping10_key5 :: None
   mapping10_key6 :: 0001-01-01-00:00

# Comment-Line: below is a Main `Key-Value-Mapping` with an empty value
#  the implementation supports: mapping11_key1, mapping11_key2
key11value_mapping




   # Comment line1 to test `Key-Value-Mapping` recognition
   # Comment line2 to test `Key-Value-Mapping` recognition
   mapping11_key1 :: null


   mapping11_key2 :: ''

# Comment-Line: below is a Main `Key-Value-List`
key12list



   # Comment-Line: List item
   value_list_item1


   value_list_item2

# Comment-Line: below is a Main `Key :: Value-List`
key13value_pairlist :: [123,8945,278]

# Comment-Line: below is a Main `Key :: Value-Lists` with an empty list: overwriting any defaults
key14value_pairlist :: []

# Comment-Line: below: `Repeated Mapping-Block Identifier`
#  this will loose the order of the `Repeated Block-Names` after parsing
#  but any library must implement an option to loop over it in order as defined in the section
* RepeatedBlk1



   # Comment-Line: BLK_OBJ0 uses all 8 possible - defined items
   BLK_OBJ0



      # Comment-Line: below Block-Item `Key-Value-Mapping` with all 3 defined items
      MyKey1mapping



         # Comment-Line: below Block `Key-Value-Mapping-Item` blk_mapping_key1
         blk_mapping_key1 :: some text


         blk_mapping_key2 :: 12345.99
         blk_mapping_key3 :: True
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-08-13:45
      MyKey5list :: [test1,test2]


      # Comment-Line: Block-Item `Key :: Value-List` with Empty List
      MyKey6list :: []
      # Comment-Line: Block-Item `Key :: Value-List`
      MyKey7list :: [True,False,False,True]
      MyKey8 :: some text
   # Comment-Line: BLK_OBJ1 does only use a subset of the defined items:
   # all others will be set to default values as implemented
   BLK_OBJ1
      # Comment-Line: overwrites only 1 Main Key: MyKey2. All other items are default values
      MyKey2 :: 999.0

   BLK_OBJ2
      # Comment-Line: below Block-Item `Key-Value-Mapping` with only one defined item of 3: the rest gets default values
      MyKey1mapping
         blk_mapping_key3 :: False
      MyKey2 :: 89456.456
      MyKey3 :: True
      MyKey4 :: 1982-02-26-12:15
      # Comment-Line: Block-Item `Key :: Value-List`
      MyKey7list

         True
         False
         # Comment-Line: test
         False
         True

   BLK_OBJ3
      MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 188.0
         blk_mapping_key3 :: False
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-12-01:52
      MyKey5list :: [dog,cat]
      MyKey8 :: just a test
   # Comment-Line: Repeated Block-Name: will be using all default values
   BLK_OBJ4

___END
'''
   lconf_validate_source(example_lconf_section_str1)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_validate_expect_failure__wrong_indentation0()
   test_validate_expect_failure__wrong_indentation1()
   test_validate_expect_failure__wrong_indentation2()
   test_validate_expect_failure__wrong_indentation3()
   test_validate_expect_failure__wrong_indentation4()
   test_validate_expect_failure__wrong_indentation5()
   test_validate_expect_failure__wrong_indentation6()

   test_validate_expect_failure__wrong_key_value_separator1()
   test_validate_expect_failure__wrong_key_value_separator2()
   test_validate_expect_failure__wrong_key_value_separator3()
   test_validate_expect_failure__wrong_key_value_separator4()
   test_validate_expect_failure__wrong_key_value_separator5()
   test_validate_expect_failure__wrong_key_value_separator6()
   test_validate_expect_failure__wrong_key_value_separator7()
   test_validate_expect_failure__wrong_key_value_separator8()
   test_validate_expect_failure__wrong_key_value_separator9()

   test_validate_expect_failure__blk_identifier()

   test_validate_file__expect_failure()
   test_validate_file__ok()

   test_validate_expect_failure__wrong_commentline_indentation__expect_failure0()
   test_validate_expect_failure__wrong_commentline_indentation__expect_failure1()

   test_lconf_validate_one_section_str_expect_failure1()
   test_lconf_validate_one_section_str_expect_failure2()
   test_lconf_validate_one_section_str_expect_failure3()

   test_validate_empty_lines_after_key_value_mapping_or_list()

