""" LCONF: Specification Examples: EXAMPLE 1: LCONF BASE EXAMPLE
"""
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from json import dumps as json_dumps
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path

# optional yaml for some example: needs pyyaml installed
try:
   # noinspection PyUnresolvedReferences
   from yaml import dump as yaml_dump

   has_yaml = True
except ImportError:
   has_yaml = False

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
   LCONF_DEFAULT,
   lconf_emit,
   lconf_emit_default_obj,
   lconf_parse_section_extract_by_name,
   lconf_prepare_and_parse_section,
   lconf_prepare_default_obj,
   lconf_to_native_type,
   lconf_to_ordered_native_type,
   lconf_validate_one_section_str,
)
from LCONF.transform import (
   lconf_to_bool,
   lconf_to_datetime,
   lconf_to_int,
   lconf_to_float,
   lconf_to_pathexpanduser,
)


# Main `Section-Template OBJ: type: Root
lconf_section__base_example_template_obj = Root([
   # Default Empty Line
   ('#1', ''),
   # Default Comment Line
   ('#2', '# Comment-Line: below: Main `Key :: Value Pair`'),
   ('key1value_pair', ''),
   ('#3', '# Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped'),
   ('key2value_pair', ''),
   ('#4', '# Comment-Line: Using a Transform Function'),
   ('key3value_pair', 0.0, lconf_to_float),
   ('key4value_pair', False, lconf_to_bool),
   ('key5value_pair', True, lconf_to_bool),
   ('key6value_pair', ''),
   ('key7value_pair', 0.0, lconf_to_float),
   ('key8value_pair', ''),
   ('key9value_pair', ''),

   # `Key-Value-Mapping: type: KVMap
   ('#5', '', None),
   ('#6', '# Comment-Line: below is a Main `Key-Value-Mapping`'),
   ('key10value_mapping', KVMap([
      ('#7', '# Comment-Line:  Key-Value-Mapping items: are `Key :: Value Pairs`'),
      ('mapping10_key1', ''),
      ('mapping10_key2', False, lconf_to_bool),
      ('mapping10_key3', 0, lconf_to_int),

      # `Key :: Value-List` or `Key-Value-List`: type: KVList: set default_is_oneline: True
      ('#8', ''),
      ('#9', '# Comment-Line:  Key-Value-Mapping item: `Key :: Value-List` or `Key-Value-List`'),
      ('mapping10_key4_list', KVList(True, [555, 9999]), lconf_to_int),

      # `Key :: Value-List` or `Key-Value-List`: type: KVList: set default_is_oneline: False
      ('#10', ''),
      ('#11', '# Comment-Line:  Key-Value-Mapping item: `Key :: Value-List` or `Key-Value-List`'),
      ('mapping10_key5_list', KVList(False, [
         555,
         9999
      ]), lconf_to_int),

      # `List-Of-Tuples`: type: ListOT: one transform function for all values
      ('#12', ''),
      ('#13', '# Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`'),
      ('mapping10_key6_list', ListOT(('x', 'y'), [
         (9999, 9999),
         (9999, 9999)
      ]), lconf_to_int),

      # `List-Of-Tuples`: type: ListOT: for each column a separate transform function
      ('#14', ''),
      ('#15', '# Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`'),
      ('mapping10_key7_list', ListOT(('name', 'b', 'c'), [
         ('something', 11, 1234),
         ('something2', 9999, 9999)
      ]), (None, lconf_to_float, lconf_to_int)),
   ])),

   # `Key-Value-Mapping: type: KVMap
   ('#16', ''),
   ('#17', '# Comment-Line: below is a Main `Key-Value-Mapping`'),
   ('key11value_mapping', KVMap([
      ('mapping11_key1', '', lconf_to_pathexpanduser),
      # `Key-Value-Mapping: type: KVMap
      ('#18', ''),
      ('#19', '# Comment-Line:  Key-Value-Mapping item: an other nested `Key-Value-Mapping`'),
      ('mapping11_key2_mapping', KVMap([
         ('#20', '# Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`'),
         ('mapping11_key2_nested_mapping_key1', '', lconf_to_datetime),

         # Repeated-Block-Identifier: type: BlkI: min_required_blocks: undefined (-1) max_required_blocks: 5
         # With DummyBlock: type: Blk
         ('#21', ''),
         ('#22', '# Comment-Line:  nested Key-Value-Mapping item: `Repeated-Block-Identifier`'),
         ('mapping11_key2_nested_mapping_key2_block_identifier', BlkI(-1, 5,
            Blk([
               ('#23', '# Comment-Line:  Block items: `Key :: Value Pairs`'),
               ('blk_item_red', 0, lconf_to_int),
               ('blk_item_green', 0, lconf_to_int),
               ('blk_item_blue', 0, lconf_to_int),
            ])
         )),

         ('#24', ''),
         ('#25', '# Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pairs`'),
         ('mapping11_key2_nested_mapping_key3', ''),

         ('#26', ''),
         ('#27', '# Comment-Line: nested Key-Value-Mapping item: `Key :: Value-List` or `Key-Value-List`'),
         ('mapping11_key2_nested_mapping_key4_list', KVList(True, ['Germany', 'France'])),
      ])),
   ])),

   ('#28', ''),
   ('#29', '# Comment-Line: below is a Main `Key :: Value-List` or `Key-Value-List`'),
   ('key12list', KVList(True, [])),

   ('#30', ''),
   ('#31', '# Comment-Line: below is a Main `Key :: Value-List` or `Key-Value-List`'),
   ('key13value_pairlist', KVList(False, [])),

   ('#32', ''),
   ('#33', '# Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'),
   ('key14list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), []),
   (None, lconf_to_int, lconf_to_int, lconf_to_int)),

   ('#34', ''),
   ('#35', '# Comment-Line: below is a Main `Key :: Value-List` or `Key-Value-List`'),
   ('key15value_pairlist', KVList(False, ['x', 'y', 'z'])),

   ('#36', ''),
   ('#37', '# Comment-Line: below is a Main `Key :: Value-List` or `Key-Value-List`'),
   ('key16value_pairlist', KVList(True, ['x', 'y', 'z'])),

   ('#38', ''),
   ('#39', '# Comment-Line: below is a Main `List-Of-Tuples` with 3 columns: |a|b|c|'),
   ('key17list_of_tuples', ListOT(('a', 'b', 'c'), [
      ('x', 'y', 'z'),
      ('x2', 'y2', 'z2')
   ])),

   # Repeated-Block-Identifier: type: BlkI: min_required_blocks: 2 max_required_blocks: 2
   # With DummyBlock: type: Blk
   ('#40', ''),
   ('#41', '# Comment-Line: below: `Repeated-Block-Identifier`'),
   ('RepeatedBlk1', BlkI(2, 5,
      Blk([

         # `Key-Value-Mapping: type: KVMap
         ('#42', '# Comment-Line: below Block-Item `Key-Value-Mapping` with all 4 defined items'),
         ('MyKey1_mapping', KVMap([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', 9999.999, lconf_to_float),
            ('blk_mapping_key3', False, lconf_to_bool),

            # `Key-Value-Mapping: type: KVMap
            ('#43', ''),
            ('#44', '# Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`'),
            ('blk_mapping_key4', KVMap([
               ('nested_mapping_key1', 'franz'),
               ('#45', ''),
               ('#46', '# Comment-Line: an other nested `Key :: Value-List` or `Key-Value-List`'),
               ('interests', KVList(True, ['a', 'b', 'c'])),

               # Repeated-Block-Identifier: type: BlkI
               ('#47', ''),
               ('#48', '# Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`'),
               ('Nested Repeated Block Identifier', BlkI(-1, -1,
                  Blk([
                     ('block-item_key1', 99999.0, lconf_to_float),
                     ('block-item_key2_list', KVList(True, []), lconf_to_bool),
                     ('block-item_key3_list', ListOT(('name', 'height', 'weight'), []),
                     (None, lconf_to_int, lconf_to_int)),
                  ])
               )),
            ])),
         ])),

         ('#49', ''),
         ('MyKey2', 99999.9, lconf_to_float),
         ('MyKey3', False, lconf_to_bool),
         ('MyKey4', 'GREAT LIFE'),

         ('#50', ''),
         ('MyKey5list', KVList(True, ['one item'])),
         ('MyKey6list', KVList(True, ['one item'])),

         ('#51', ''),
         ('MyKey7list', KVList(True, [False]), lconf_to_bool),
         ('MyKey8', ''),
      ])
   )),
])

lconf_section__base_example_lconf_section_raw_str = r'''___SECTION :: BaseEXAMPLE

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
# Comment-Line: Values can be most characters and also longer lines
key9value_pair :: different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ  翻訳する μεταφράζω

# Comment-Line: below is a Main `Key-Value-Mapping`
. key10value_mapping
   # Comment-Line:  Key-Value-Mapping items: `Key :: Value Pair`
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
   - mapping10_key7_list |name|b|c|
      Tom,     2.0, 3
      Peter,   2.4, 5

# Comment-Line: below is a Main `Key-Value-Mapping`
. key11value_mapping
   # Comment-Line:  Key-Value-Mapping item: `Key :: Value Pair`
   mapping11_key1 :: /home/examples/

   # Comment-Line:  Key-Value-Mapping item: an other nested `Key-Value-Mapping`
   . mapping11_key2_mapping
      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pair`
      mapping11_key2_nested_mapping_key1 :: 2014-05-08 13:39

      # Comment-Line:  nested Key-Value-Mapping item: `Repeated-Block-Identifier`
      * mapping11_key2_nested_mapping_key2_block_identifier

         # Comment-Line: `Block-Name1`
         sky_blue_blk_name1
            # Comment-Line:  Block items: `Key :: Value Pair`
            blk_item_red :: 135
            blk_item_green :: 206
            blk_item_blue :: 235

      # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pair`
      mapping11_key2_nested_mapping_key3 :: car

      # Comment-Line: nested Key-Value-Mapping item: `Key-Value-List`
      - mapping11_key2_nested_mapping_key4_list
         # Comment-Line: List item
         value_list_item1
         value_list_item2

# Comment-Line: below is a Main `Key-Value-List`
- key12list
   # Comment-Line: List item
   value_list_item1
   value_list_item2

# Comment-Line: below is a Main `Key :: Value-List`
- key13value_pairlist :: 123,8945,278

# Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
- key14list_of_color_tuples |Color Name|Red|Green|Blue|
   # Comment-Line: `List-Of-Tuples` item lines (rows)
   forestgreen,   34,   139,  34
   brick,         156,  102,  31

# Comment-Line: below is a Main `Key :: Value-List` with an empty list: overwriting any defaults
- key15value_pairlist ::

# Comment-Line: below is a Main `Key-Value-List` with an empty list: overwriting any defaults
- key16value_pairlist

# Comment-Line: below is a Main `List-Of-Tuples` with an empty list: overwriting any defaults
- key17list_of_tuples |a|b|c|


# Comment-Line: below: `Repeated-Block-Identifier`
#  this will loose the order of the `Repeated Block-Names` after parsing
#  but any library must implement an option to loop over it in order as defined in the section
* RepeatedBlk1
   # Comment-Line: BLK_OBJ1 (Block-Name) uses all 8 possible - defined items
   BLK_OBJ1

      # Comment-Line: below Block-Item `Key-Value-Mapping` with all 4 defined items
      . MyKey1_mapping
         blk_mapping_key1 :: some text
         blk_mapping_key2 :: 12345.99
         blk_mapping_key3 :: True

         # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
         . blk_mapping_key4
            nested_mapping_key1 :: franz
            # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
            - interests
               sport
               reading

            # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
            * Nested Repeated Block Identifier
               # Comment-Line:  keys do not have to be a single word: below a multi words Block-Name
               Nested Block Name1
                  block-item_key1 :: 12345.99
                  - block-item_key2_list :: False,True,True
                  # Comment-Line:  block-item_key3_list: `List-Of-Tuples`
                  - block-item_key3_list |name|height_cm|weight_kg|
                     # Comment-Line: |name|height_cm|weight_kg|
                     Tim,     178,     86
                     John,    166,   67

      MyKey2 :: 789.9
      MyKey3 :: True

      # Comment-Line:  empty `Key :: Value Pair`
      MyKey4 ::
      - MyKey5list :: test1,test2

      # Comment-Line: Block-Item `Key :: Value-List` with Empty List
      - MyKey6list ::

      # Comment-Line: Block-Item `Key :: Value-List`
      - MyKey7list :: True,False,False,True

      MyKey8 :: some text

   # Comment-Line: BLK_OBJ2 (Block-Name)
   BLK_OBJ2

      # Comment-Line: below Block-Item `Key-Value-Mapping` with all 4 defined items
      . MyKey1_mapping
         blk_mapping_key3 :: False

         # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
         . blk_mapping_key4
            nested_mapping_key1 :: julia
            # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
            - interests
               golf
               flowers

            # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
            * Nested Repeated Block Identifier
               # Comment-Line:  Block-Name: all values will use defaults
               Nested Block Name1
               # Comment-Line:  Block-Name: and defining an empty list: block-item_key2_list
               Nested Block Name2
                  - block-item_key2_list ::
                  # Comment-Line:  block-item_key3_list: `List-Of-Tuples`: to define an empty list: skip any item lines
                  - block-item_key3_list |name|height_cm|weight_kg|

      # Comment-Line: Block-Item `Key-Value-Lists`
      - MyKey7list
         True
         False
         True

   BLK_OBJ3
      # Comment-Line: below Block-Item empty `Key-Value-Mapping`: will use all defaults
      #     similar if it would not be defined at all
      . MyKey1_mapping

      # Comment-Line:  `Key :: Value Pairs`
      MyKey4 ::
      - MyKey5list :: test1,test2

   # Comment-Line: Repeated Block-Name: will be using all default values
   #    Note: nested Blocks are not having any default names: so the items are skipped
   BLK_OBJ4

___END'''


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   pass

   # EXAMPLE: ONLY VALIDATE
   lconf_validate_one_section_str(lconf_section__base_example_lconf_section_raw_str)

   # EXAMPLE: ONLY PREPARE DEFAULT OBJ
   lconf_default_obj = lconf_prepare_default_obj(lconf_section__base_example_template_obj, with_comments=False)
   print('\n\n============== EXAMPLE: ONLY PREPARE DEFAULT OBJ ==============\n')
   print(lconf_default_obj)

   # EXAMPLE: VALIDATE, PREPARE, PARSE:
   # validate a `LCONF-Section string` and prepare a default lconf obj from the template obj and parse the LCONF-Section
   print('\n\n============== EXAMPLE: VALIDATE, PREPARE, PARSE ==============\n')
   lconf_parse_obj = lconf_prepare_and_parse_section(
      lconf_section__base_example_lconf_section_raw_str,
      lconf_section__base_example_template_obj,
      with_comments=True,
      validate=True
   )
   print(lconf_parse_obj)

   # EXAMPLE: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: this is also useful to extract from files
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__base_example_lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__base_example_template_obj,
      with_comments=True,
      validate=True
   )
   print(
      '\n\n============== EXAMPLE: EXTRACT KNOWN SECTION, VALIDATE, PREPARE, PARSE: also for files ==============\n')
   print(lconf_parse_obj)

   # EXAMPLE: ACCESS The Section-INFO
   print('\n\n============== EXAMPLE: ACCESS The Section-INFO ==============\n')
   print('  lconf_parse_obj.key_order: ', lconf_parse_obj.key_order)
   print('  lconf_parse_obj.section_name: ', lconf_parse_obj.section_name)
   print('  lconf_parse_obj.is_parsed: ', lconf_parse_obj.is_parsed)
   print('  lconf_parse_obj.has_comments: ', lconf_parse_obj.has_comments)

   # EXAMPLE: EMIT DEFAULT OBJ
   lconf_section_emitted_default_obj_str = lconf_emit_default_obj(
      lconf_section__base_example_template_obj,
      'EMITTED BaseEXAMPLE',
      onelinelists=LCONF_DEFAULT,
      with_comments=True
   )
   print('\n\n============== EXAMPLE: EMIT DEFAULT OBJ ==============\n')
   print(lconf_section_emitted_default_obj_str)

   # EXAMPLE: EMIT PARSED LCONF OBJ
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__base_example_lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__base_example_template_obj,
      with_comments=True,
      validate=True
   )
   lconf_section_emitted_parsed_obj_str = lconf_emit(lconf_parse_obj, onelinelists=LCONF_DEFAULT)

   print('\n\n============== EXAMPLE: EMIT PARSED LCONF OBJ ==============\n')
   print(lconf_section_emitted_parsed_obj_str)

   # EXAMPLE: EMIT TO JSON
   lconf_parse_obj = lconf_parse_section_extract_by_name(
      lconf_section__base_example_lconf_section_raw_str,
      'BaseEXAMPLE',
      lconf_section__base_example_template_obj,
      with_comments=False,
      validate=True
   )
   result_ordered_native_type = lconf_to_ordered_native_type(lconf_parse_obj)
   # IMPORTANT: datetime.datetime(2014, 5, 8, 13, 39) is not JSON serializable
   result_ordered_native_type['key11value_mapping']['mapping11_key2_mapping'][
      'mapping11_key2_nested_mapping_key1'] = '2014-05-08 13:39:00'
   dump_json = json_dumps(result_ordered_native_type, indent=3)

   print('\n\n============== EXAMPLE: EMIT TO ORDERED JSON ==============\n')
   print(dump_json)

   # EXAMPLE: EMIT TO YAML
   if has_yaml:
      lconf_parse_obj = lconf_parse_section_extract_by_name(
         lconf_section__base_example_lconf_section_raw_str,
         'BaseEXAMPLE',
         lconf_section__base_example_template_obj,
         with_comments=False,
         validate=True
      )
      result_native_type = lconf_to_native_type(lconf_parse_obj)
      #  IMPORTANT: datetime.datetime(2014, 5, 8, 13, 39) is not JSON serializable
      result_native_type['key11value_mapping']['mapping11_key2_mapping'][
         'mapping11_key2_nested_mapping_key1'] = '2014-05-08 13:39:00'
      dump_yaml = yaml_dump(result_native_type, indent=3, allow_unicode=True)

      print('\n\n============== EXAMPLE: EMIT TO YAML ==============\n')
      print(dump_yaml)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   main()
