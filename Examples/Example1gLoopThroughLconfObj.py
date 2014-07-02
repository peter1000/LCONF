""" Example implementation: of the documentation: docs/source/main_docs/LCONF_Specification-4.1.rst: 'EXAMPLE 1'
"""
from datetime import datetime
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


from RDICT.MainCode import (
   RdictFO,
   RdictFO2,
   RdictIO
)

SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import lconf_prepare_and_parse_section
from LCONF.Transform import (
   lconf_to_bool,
   lconf_to_datetime,
   lconf_to_float,
   lconf_to_int,
   lconf_to_number
)


example_lconf_section_str = r'''___SECTION :: BaseEXAMPLE

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
      MyKey7list :: [True,False,False,True]
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


# Main `Section-Template OBJ: type: RdictFO2
example_template = RdictFO2([
   ('key1value_pair', ''),
   ('key2value_pair', ''),
   ('key3value_pair', (0.0, lconf_to_number)),
   ('key4value_pair', (False, lconf_to_bool)),
   ('key5value_pair', (False, lconf_to_bool)),
   ('key6value_pair', ''),
   ('key7value_pair', (0.0, lconf_to_float)),
   ('key8value_pair', (False, lconf_to_bool)),
   ('key9value_pair', (False, lconf_to_bool)),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('key10value_mapping', RdictFO2([
      ('mapping10_key1', ''),
      ('mapping10_key2', False),
      ('mapping10_key3', (0, lconf_to_int)),
      ('mapping10_key4', (False, lconf_to_bool)),
      ('mapping10_key5', ''),
      ('mapping10_key6', (datetime.utcfromtimestamp(0), lconf_to_datetime)),
   ])),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('key11value_mapping', RdictFO2([
      ('mapping11_key1', ''),
      ('mapping11_key2', False),
   ])),

   ('key12list', []),
   ('key13value_pairlist', ([], lconf_to_int)),
   ('key14value_pairlist', [1, 2, 3]),


   # Repeated Mapping-Block Identifier: type: RdictIO
   ('RepeatedBlk1', RdictIO([
      # Repeated Block-Name: default dummy: must be named: `dummy_blk`: type: RdictFO2
      ('dummy_blk', RdictFO2([

         # Block-Item `Key-Value-Mapping`: type: RdictFO2
         ('MyKey1mapping', RdictFO2([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', (0.0, lconf_to_float)),
            ('blk_mapping_key3', (False, lconf_to_bool)),
         ])),

         ('MyKey2', (0.0, lconf_to_float)),
         ('MyKey3', ''),
         ('MyKey4', (datetime.utcfromtimestamp(0), lconf_to_datetime)),
         ('MyKey5list', []),
         ('MyKey6list', [1, 2, 3]),
         ('MyKey7list', ([], lconf_to_bool)),
         ('MyKey8', ''),
      ])),
   ])),
])


def main():
   # Prepare: a default lconf obj from the template obj and parse the LCONF-Section string
   result1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=False)
   #print('\n=== result1: ', result1)

   # Accessing:  The Section-INFO
   print('\n\n=== result1: The Section ===')
   print('  result1.extra_data[l_section_name]: ', result1.extra_data['l_section_name'])
   print('  result1.extra_data[l_parsed]: ', result1.extra_data['l_parsed'])
   #
   print('\n\n=== result1: LOOP THROUGH PARSED LCONF OBJ ===')
   for main_key, main_value in result1.yield_key_value_order():
      # Main Lists
      if isinstance(main_value, list):
         print('\nMain Lists:main_key: ', main_key)
         for main_list_item in main_value:
            print('   main_list_item: ', main_list_item)
      # Main Mappings
      elif isinstance(main_value, RdictFO):
         print('\nMain Mappings:main_key: ', main_key)
         for main_mapping_key, main_mapping_value in main_value.yield_key_value_order():
            print('   main_mapping_key: ', main_mapping_key, ' main_mapping_value: ', main_mapping_value)
      # Main: BLOCK Identifier
      elif isinstance(main_value, RdictIO):
         print('\nMain: BLOCK Identifier:main_key: ', main_key)
         for blk_name, blk_obj in main_value.yield_key_value_order():
            print('\n   BLK-Name:blk_name: ', blk_name)
            # BLOCK:  Items
            for blk_key, blk_value in blk_obj.yield_key_value_order():
               # BLOCK Lists
               if isinstance(blk_value, list):
                  print('\n      BLK Lists:main_key: ', blk_key)
                  for blk_list_item in blk_value:
                     print('           blk_list_item: ', blk_list_item)
               # BLOCK Mappings
               elif isinstance(blk_value, RdictFO):
                  print('\n      BLK Mappings:blk_key: ', blk_key)
                  for blk_mapping_key, blk_mapping_value in blk_value.yield_key_value_order():
                     print('           blk_mapping_key: ', blk_mapping_key, ' blk_mapping_value: ', blk_mapping_value)
               # BLOCK Key::value
               else:
                  print('\n      BLK Key::value:blk_key: ', blk_key, ' blk_value: ', blk_value)
      # Main Key::value
      else:
         print('\nMain Key::value:main_key: ', main_key, ' main_value: ', main_value)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
