""" tests LCONF parse - emit
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

from nose import tools

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


from LCONF.MainCode import (
   lconf_dict_to_lconf,
   lconf_emit,
   lconf_emit_default_obj,
   lconf_parse_section_lines,
   lconf_parse_section,
   lconf_parse_section_extract_by_name,
   lconf_prepare_and_parse_section,
   lconf_prepare_and_parse_section_lines,
   lconf_prepare_default_obj,
   lconf_remove_comments,
   lconf_validate_source,
)
from LCONF.Transform import (
   lconf_to_bool,
   lconf_to_float,
   lconf_to_int,
   lconf_to_number
)
from LCONF.ProjectErr import Err


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
      # Comment-Line: below an default Block-Item `Key-Value-Mapping`
      MyKey3 :: True

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
   ('#1', ''),
   ('#2', '# Default Comment: Some key value pairs'),
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
   ('#3', ''),
   ('#4', '# Default Comment: Main Key-Value-Mapping'),
   ('key10value_mapping', RdictFO2([
      ('mapping10_key1', ''),
      ('mapping10_key2', False),
      ('#5', '# Default Comment: Main mapping10_key3'),
      ('mapping10_key3', (0, lconf_to_int)),
      ('mapping10_key4', (False, lconf_to_bool)),
      ('mapping10_key5', ''),
      ('mapping10_key6', datetime.utcfromtimestamp(0)),
   ])),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('#6', ''),
   ('key11value_mapping', RdictFO2([
      ('mapping11_key1', ''),
      ('mapping11_key2', False),
   ])),

   ('key12list', []),
   ('key13value_pairlist', ([], lconf_to_int)),
   ('key14value_pairlist', [1, 2, 3]),

   # Repeated Mapping-Block Identifier: type: RdictIO
   ('#7', '# Default Comment: Repeated Mapping-Block Identifier'),
   ('RepeatedBlk1', RdictIO([
      # Repeated Block-Name: default dummy: must be named: `dummy_blk`: type: RdictFO2
      ('dummy_blk', RdictFO2([

         # Block-Item `Key-Value-Mapping`: type: RdictFO2
         ('#8', ''),
         ('#9', '# Default Comment: Block-Item `Key-Value-Mapping'),
         ('MyKey1mapping', RdictFO2([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', (0.0, lconf_to_float)),
            ('#10', '# Default Comment: blk_mapping_key3'),
            ('blk_mapping_key3', (False, lconf_to_bool)),
         ])),

         ('MyKey2', (0.0, lconf_to_float)),
         ('MyKey3', ''),
         ('MyKey4', datetime.utcfromtimestamp(0)),
         ('MyKey5list', []),
         ('MyKey6list', [1, 2, 3]),
         ('MyKey7list', ([], lconf_to_bool)),
         ('MyKey8', ''),
      ])),
   ])),
])



# Main `Section-Template OBJ: type: RdictFO2
example_template_no_cast = RdictFO2([
   ('#1', ''),
   ('#2', '# Default Comment: Some key value pairs'),
   ('key1value_pair', ''),
   ('key2value_pair', ''),
   ('key3value_pair', 0.0),
   ('key4value_pair', False),
   ('key5value_pair', False),
   ('key6value_pair', ''),
   ('key7value_pair', 0.0),
   ('key8value_pair', False),
   ('key9value_pair', False),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('#3', ''),
   ('#4', '# Default Comment: Main Key-Value-Mapping'),
   ('key10value_mapping', RdictFO2([
      ('mapping10_key1', ''),
      ('mapping10_key2', False),
      ('#5', '# Default Comment: Main mapping10_key3'),
      ('mapping10_key3', (0, lconf_to_int)),
      ('mapping10_key4', False),
      ('mapping10_key5', ''),
      ('mapping10_key6', datetime.utcfromtimestamp(0)),
   ])),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('#6', ''),
   ('key11value_mapping', RdictFO2([
      ('mapping11_key1', ''),
      ('mapping11_key2', False),
   ])),

   ('key12list', []),
   ('key13value_pairlist', ([], lconf_to_int)),
   ('key14value_pairlist', [1, 2, 3]),

   # Repeated Mapping-Block Identifier: type: RdictIO
   ('#7', '# Default Comment: Repeated Mapping-Block Identifier'),
   ('RepeatedBlk1', RdictIO([
      # Repeated Block-Name: default dummy: must be named: `dummy_blk`: type: RdictFO2
      ('dummy_blk', RdictFO2([

         # Block-Item `Key-Value-Mapping`: type: RdictFO2
         ('#8', ''),
         ('#9', '# Default Comment: Block-Item `Key-Value-Mapping'),
         ('MyKey1mapping', RdictFO2([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', 0.0),
            ('#10', '# Default Comment: blk_mapping_key3'),
            ('blk_mapping_key3', False),
         ])),

         ('MyKey2', 0.0),
         ('MyKey3', ''),
         ('MyKey4', datetime.utcfromtimestamp(0)),
         ('MyKey5list', []),
         ('MyKey6list', [1, 2, 3]),
         ('MyKey7list', []),
         ('MyKey8', ''),
      ])),
   ])),
])


example_lconf_section_str_no_comments = r'''___SECTION :: BaseEXAMPLE
key1value_pair :: value1
key2value_pair ::
key3value_pair :: 1234
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: false
key10value_mapping
   mapping10_key1 :: null
   mapping10_key2 :: true
   mapping10_key3 :: 123456
   mapping10_key4 :: False
   mapping10_key5 :: None
   mapping10_key6 :: 0001-01-01-00:00
key11value_mapping
   mapping11_key1 :: null
   mapping11_key2 :: ''
key12list :: [value_list_item1,value_list_item2]
key13value_pairlist :: [123,8945,278]
key14value_pairlist :: []
* RepeatedBlk1
   BLK_OBJ0
      MyKey1mapping
         blk_mapping_key1 :: some text
         blk_mapping_key2 :: 12345.99
         blk_mapping_key3 :: True
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-08-13:45
      MyKey5list :: [test1,test2]
      MyKey6list :: []
      MyKey7list :: [True,False,False,True]
      MyKey8 :: some text
   BLK_OBJ1
      MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 999.0
      MyKey3 ::
      MyKey4 :: 1970-01-01 00:00:00
      MyKey5list :: []
      MyKey6list :: [1,2,3]
      MyKey7list :: []
      MyKey8 ::
   BLK_OBJ2
      MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 89456.456
      MyKey3 :: True
      MyKey4 :: 1982-02-26-12:15
      MyKey5list :: []
      MyKey6list :: [1,2,3]
      MyKey7list :: [True,False,False,True]
      MyKey8 ::
   BLK_OBJ3
      MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 188.0
         blk_mapping_key3 :: False
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-12-01:52
      MyKey5list :: [dog,cat]
      MyKey6list :: [1,2,3]
      MyKey7list :: []
      MyKey8 :: just a test
   BLK_OBJ4
      MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 0.0
      MyKey3 ::
      MyKey4 :: 1970-01-01 00:00:00
      MyKey5list :: []
      MyKey6list :: [1,2,3]
      MyKey7list :: []
      MyKey8 ::
___END'''


def test_parse_section_access_each_attribute():
   """ Tests: parse section access items
   """
   print('::: TEST: test_parse_section_access_each_attribute()')
   lconf_validate_source(example_lconf_section_str)

   result = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   for main_key, main_value in result.yield_key_value_order():
      # Main Lists
      if isinstance(main_value, list):
         for main_list_item in main_value:
            pass
      # Main Mappings
      elif isinstance(main_value, RdictFO):
         for main_mapping_key, main_mapping_value in main_value.yield_key_value_order():
            pass
      # Main: BLOCK Identifier
      elif isinstance(main_value, RdictIO):
         for blk_name, blk_obj in main_value.yield_key_value_order():
            # BLOCK:  Items
            for blk_key, blk_value in blk_obj.yield_key_value_order():
               # BLOCK Lists
               if isinstance(blk_value, list):
                  for blk_list_item in blk_value:
                     pass
               # BLOCK Mappings
               elif isinstance(blk_value, RdictFO):
                  for blk_mapping_key, blk_mapping_value in blk_value.yield_key_value_order():
                     pass


@tools.raises(KeyError)
def test_parse_section_access_none_existing_key__expect_failure():
   """ Tests: test_parse_section_access_none_existing_key__expect_failure: parse section access a none existing key:  <KeyError>  (expect failure)
   """
   print('::: TEST: test_parse_section_access_none_existing_key__expect_failure()')
   lconf_validate_source(example_lconf_section_str)

   lconf_obj = lconf_prepare_default_obj(example_template)
   result = lconf_parse_section(lconf_obj, example_lconf_section_str, example_template)

   dummy_result = result['key6value_pair23']


@tools.raises(KeyError)
def test_parse_section_wrong_key__expect_failure():
   """ Tests: parse section with a wrong key:  <AttributeError>  (expect failure)
   """
   print('::: TEST: test_parse_section_wrong_slot_item()')
   example_lconf_str = r'''___SECTION :: BASE_EXAMPLE
key1value_pair_wrong :: value1
___END
'''
   lconf_validate_source(example_lconf_str)
   result = lconf_prepare_and_parse_section(example_lconf_str, example_template, validate=True)


@tools.raises(KeyError)
def test_parse_section_wrong_blk_identifier__expect_failure():
   """ Tests: parse section with a wrong Block Identifier:  <KeyError:>  (expect failure)
   """
   print('::: TEST: test_parse_section_wrong_blk_identifier__expect_failure()')
   example_lconf_str = r'''___SECTION :: BASE_EXAMPLE
* RepeatedBlkWrong
___END
'''
   lconf_validate_source(example_lconf_str)

   lconf_obj = lconf_prepare_default_obj(example_template)
   result = lconf_parse_section(lconf_obj, example_lconf_str, example_template)


@tools.raises(KeyError)
def test_parse_section_wrong_blk_key__expect_failure():
   """ Tests: parse section with a wrong Block-Key:  <KeyError:>  (expect failure)
   """
   print('::: TEST: test_parse_section_wrong_blk_key__expect_failure()')
   example_lconf_str = r'''___SECTION :: BASE_EXAMPLE
* RepeatedBlk1
   # Comment: Repeated Block-Name
   BLK_OBJ1
      # Comment: Repeated Block-Key: is a Key :: Value Pair with an empty string value
      MyKeyWrong :: So What
___END
'''
   lconf_validate_source(example_lconf_str)
   result = lconf_prepare_and_parse_section(example_lconf_str, example_template, validate=False)


def test__parse_emit1():
   """ Tests: parse section and compares the output of the emit 1 loaded Section
   """
   print('::: TEST: test__parse_emit1()')
   lconf_obj = lconf_prepare_default_obj(example_template_no_cast)
   section_lines = example_lconf_section_str_no_comments.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   # Parse parse_section_lines
   result_parse = lconf_parse_section_lines(lconf_obj, section_lines, section_name, example_template_no_cast)

   result_emit = lconf_emit(result_parse, onelinelists=True, with_comments=False)
   tools.eq_(example_lconf_section_str_no_comments, result_emit, msg=None)


def test__parse_emit2():
   """ Tests: parse section emit and reparse/emit onelinelists=True with_comments=False)
   """
   print('::: TEST: test__parse_emit2()')
   section_lines = example_lconf_section_str_no_comments.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   result_parse1 = lconf_prepare_and_parse_section_lines(section_lines, section_name, example_template_no_cast)

   result_emit1 = lconf_emit(result_parse1, onelinelists=True, with_comments=False)

   lconf_obj2 = lconf_prepare_default_obj(example_template_no_cast)
   result_parse2 = lconf_parse_section(lconf_obj2, result_emit1, example_template_no_cast)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=False)

   tools.eq_(result_emit1, result_emit2, msg=None)


def test__parse_emit2b():
   """ Tests: test__parse_emit2b: parse section emit and reparse/emit onelinelists=True with_comments=True)
   """
   print('::: TEST: test__parse_emit2b()')
   section_lines = example_lconf_section_str_no_comments.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   result_parse1 = lconf_prepare_and_parse_section_lines(section_lines, section_name, example_template_no_cast)

   result_emit1 = lconf_emit(result_parse1, onelinelists=True, with_comments=True)

   lconf_obj2 = lconf_prepare_default_obj(example_template_no_cast)
   result_parse2 = lconf_parse_section(lconf_obj2, result_emit1, example_template_no_cast)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=True)

   tools.eq_(result_emit1, result_emit2, msg=None)


def test__parse_emit3():
   """ Tests: parse section emit and reparse/emit onelinelists=False with_comments=False)
   """
   print('::: TEST: test__parse_emit3()')
   section_lines = example_lconf_section_str_no_comments.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   result_parse1 = lconf_prepare_and_parse_section_lines(section_lines, section_name, example_template_no_cast)

   result_emit1 = lconf_emit(result_parse1, onelinelists=False, with_comments=False)

   lconf_obj2 = lconf_prepare_default_obj(example_template_no_cast)
   result_parse2 = lconf_parse_section(lconf_obj2, result_emit1, example_template_no_cast)
   result_emit3 = lconf_emit(result_parse2, onelinelists=False, with_comments=False)

   tools.eq_(result_emit1, result_emit3, msg=None)


def test__parse_emit3b():
   """ Tests: test__parse_emit3b: parse section emit and reparse/emit onelinelists=False with_comments=True)
   """
   print('::: TEST: test__parse_emit3b()')
   section_lines = example_lconf_section_str_no_comments.splitlines()
   not_needed_start_tag, section_name = section_lines[0].split(' :: ', 1)
   result_parse1 = lconf_prepare_and_parse_section_lines(section_lines, section_name, example_template_no_cast)

   result_emit1 = lconf_emit(result_parse1, onelinelists=False, with_comments=True)

   lconf_obj2 = lconf_prepare_default_obj(example_template_no_cast)
   result_parse2 = lconf_parse_section(lconf_obj2, result_emit1, example_template_no_cast)
   result_emit3 = lconf_emit(result_parse2, onelinelists=False, with_comments=True)

   tools.eq_(result_emit1, result_emit3, msg=None)


def test__parse_emit4():
   """ Tests: CAST parse section emit and reparse/emit onelinelists=True  with_comments=True
   """
   print('::: TEST: test__parse_emit4()')
   lconf_validate_source(example_lconf_section_str)
   result_parse1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit1 = lconf_emit(result_parse1, onelinelists=True, with_comments=True)
   result_parse2 = lconf_prepare_and_parse_section(result_emit1, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=True)
   tools.eq_(result_emit1, result_emit2, msg=None)


def test__parse_emit4b():
   """ Tests: test__parse_emit4b: CAST parse section emit and reparse/emit onelinelists=True  with_comments=False
   """
   print('::: TEST: test__parse_emit4b()')
   lconf_validate_source(example_lconf_section_str)
   result_parse1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit1 = lconf_emit(result_parse1, onelinelists=True, with_comments=False)
   result_parse2 = lconf_prepare_and_parse_section(result_emit1, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=False)
   tools.eq_(result_emit1, result_emit2, msg=None)


def test__parse_emit5():
   """ Tests: CAST parse section emit and reparse/emit onelinelists=False  with_comments=True
   """
   print('::: TEST: test__parse_emit5()')
   lconf_validate_source(example_lconf_section_str)
   result_parse1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit1 = lconf_emit(result_parse1, onelinelists=False, with_comments=True)
   result_parse2 = lconf_prepare_and_parse_section(result_emit1, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=False, with_comments=True)
   tools.eq_(result_emit1, result_emit2, msg=None)


def test__parse_emit5b():
   """ Tests: test__parse_emit5b: CAST parse section emit and reparse/emit onelinelists=False  with_comments=False
   """
   print('::: TEST: test__parse_emit5b()')
   lconf_validate_source(example_lconf_section_str)
   result_parse1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit1 = lconf_emit(result_parse1, onelinelists=False, with_comments=False)
   result_parse2 = lconf_prepare_and_parse_section(result_emit1, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=False, with_comments=False)
   tools.eq_(result_emit1, result_emit2, msg=None)


def test__emit_none_parsed_lconf_obj_reparse():
   """ Tests: test__emit_none_parsed_lconf_obj_reparse: mit LCONF OBJ defaults section and reparse/emit onelinelists=True with_comments=True
   """
   print('::: TEST: test__emit_none_parsed_lconf_obj_reparse()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=True, emit_dummy_blks=True, with_comments=True)
   result_parse2 = lconf_prepare_and_parse_section(result_emit_none_parsed_lconf_obj, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=True)
   tools.eq_(result_emit_none_parsed_lconf_obj, result_emit2, msg=None)


def test__emit_none_parsed_lconf_obj_reparse2():
   """ Tests: test__emit_none_parsed_lconf_obj_reparse2 emit LCONF OBJ defaults section and reparse/emit onelinelists=False with_comments=True
   """
   print('::: TEST: test__emit_none_parsed_lconf_obj_reparse2()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=False, emit_dummy_blks=True, with_comments=True)
   result_parse2 = lconf_prepare_and_parse_section(result_emit_none_parsed_lconf_obj, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=False, with_comments=True)
   tools.eq_(result_emit_none_parsed_lconf_obj, result_emit2, msg=None)


def test__emit_none_parsed_lconf_obj_reparse3():
   """ Tests: test__emit_none_parsed_lconf_obj_reparse3 emit LCONF OBJ defaults section and reparse/emit onelinelists=True with_comments=False
   """
   print('::: TEST: test__emit_none_parsed_lconf_obj_reparse3()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=True, emit_dummy_blks=True, with_comments=False)
   result_parse2 = lconf_prepare_and_parse_section(result_emit_none_parsed_lconf_obj, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=True, with_comments=False)
   tools.eq_(result_emit_none_parsed_lconf_obj, result_emit2, msg=None)


def test__emit_none_parsed_lconf_obj_reparse4():
   """ Tests: test__emit_none_parsed_lconf_obj_reparse4 emit LCONF OBJ defaults section and reparse/emit onelinelists=False with_comments=False
   """
   print('::: TEST: test__emit_none_parsed_lconf_obj_reparse4()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=False, emit_dummy_blks=True, with_comments=False)
   result_parse2 = lconf_prepare_and_parse_section(result_emit_none_parsed_lconf_obj, example_template, validate=True)
   result_emit2 = lconf_emit(result_parse2, onelinelists=False, with_comments=False)
   tools.eq_(result_emit_none_parsed_lconf_obj, result_emit2, msg=None)


def test_parse_get_value1():
   """ Tests: parse section access value
   """
   print('::: TEST: test_parse_get_value1()')
   example_lconf = r'''___SECTION :: BASE_EXAMPLE
key8value_pair :: true
* RepeatedBlk1
   BLK_OBJ1
      MyKey2 :: [12345,9842.5]
___END
'''
   lconf_validate_source(example_lconf)
   result = lconf_prepare_and_parse_section(example_lconf, example_template_no_cast)
   tools.ok_(isinstance(result['key8value_pair'], str), msg='Expected: key8value_pair: true str')
   tools.ok_(isinstance(result['RepeatedBlk1']['BLK_OBJ1']['MyKey2'][0], str), msg='Expected: MyKey2 list item 1: 12345 isinstance str')
   tools.ok_(isinstance(result['RepeatedBlk1']['BLK_OBJ1']['MyKey2'][1], str), msg='Expected: MyKey2 list item 2: 9842.5 isinstance str')


def test_parse_get_value2():
   """ Tests: CAST parse section access value
   """
   print('::: TEST: test_parse_get_value2()')
   example_lconf = r'''___SECTION :: BASE_EXAMPLE
key8value_pair :: true
* RepeatedBlk1
   BLK_OBJ1
      MyKey2 :: [12345.0,9842.5]
___END
'''
   result = lconf_prepare_and_parse_section(example_lconf, example_template, validate=True)
   tools.ok_(isinstance(result['key8value_pair'], bool), msg='Expected: CAST to bool key8value_pair: true isinstance bool')
   tools.ok_(isinstance(result['RepeatedBlk1']['BLK_OBJ1']['MyKey2'][0], float), msg='Expected: CAST to number MyKey2 list item 1: 12345 isinstance float')
   tools.ok_(isinstance(result['RepeatedBlk1']['BLK_OBJ1']['MyKey2'][1], float), msg='Expected: CAST to number MyKey2 list item 1: 12345 isinstance float')


def test__parse_a_dict():
   """ Tests: just parses a dicts using: lconf_dict_to_lconf()
   """
   print('::: TEST: test__parse_a_dict()')
   example_dict = {
      'description': 'A trivial terminal emulator',
      'maintainer': 'Timothy Hobbs < (at)  dot cz>',
      'last_update_time': '2014_02_12_12:59',
      'dependency': 'libx11',
      'executable': '/usr/bin/xterm',
      'x11': [123.0, 123],
      'sound_card': False,
      'inherit_working_directory': None
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(example_dict, 'PERMISSIONS', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_dict2():
   """ Tests: just parses a little nested dict using: lconf_dict_to_lconf()
   """
   print('::: TEST: test__parse_a_dic2t()')
   example_nested_dict = {
      "description": "A trivial terminal emulator",
      "maintainer": "Timothy Hobbs < (at)  dot cz>",
      "last_update_time": "2014_02_12_12:59",
      "dependency": "libx11",
      "executable": "/usr/bin/xterm",
      "x11": [
         123.0,
         123
      ],
      "sound_card": False,
      "inherit_working_directory": None,
      "allow_network_access": True,
      "test_mapping": {
         "test_mapping_key1": None,
         "test_mapping_key2": 234,
      }
   }


   result_dict_to_lconf_str = lconf_dict_to_lconf(example_nested_dict, 'PERMISSIONS', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__check_indent_for_emit_with_comments1():
   """ Tests: test__check_indent_for_emit_with_comments1
   """
   print('::: TEST: test__check_indent_for_emit_with_comments1()')
   result_parse = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit = lconf_emit(result_parse, onelinelists=True, with_comments=True)

   lconf_validate_source(result_emit)


def test__check_indent_for_emit_with_comments2():
   """ Tests: test__check_indent_for_emit_with_comments2
   """
   print('::: TEST: test__check_indent_for_emit_with_comments2()')
   result_parse = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   result_emit = lconf_emit(result_parse, onelinelists=False, with_comments=True)

   lconf_validate_source(result_emit)


def test__check_indent_for_emit_with_comments3():
   """ Tests: test__check_indent_for_emit_with_comments3
   """
   print('::: TEST: test__check_indent_for_emit_with_comments3()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=True, emit_dummy_blks=True, with_comments=True)
   lconf_validate_source(result_emit_none_parsed_lconf_obj)


def test__check_indent_for_emit_with_comments4():
   """ Tests: test__check_indent_for_emit_with_comments4
   """
   print('::: TEST: test__check_indent_for_emit_with_comments4()')
   result_emit_none_parsed_lconf_obj = lconf_emit_default_obj(example_template, 'TestSection', onelinelists=False, emit_dummy_blks=True, with_comments=True)
   lconf_validate_source(result_emit_none_parsed_lconf_obj)


@tools.raises(AssertionError)
def test__check_lconf_remove_comments():
   """ Tests: test__check_lconf_remove_comments
   """
   print('::: TEST: test__check_lconf_remove_comments()')
   lconf__obj = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   if '#2' not in lconf__obj:
      # this is not the error we expect
      raise Err('test__check_lconf_remove_comments', '`#2` should be found after parsing the section')
   lconf__obj__no_comments = lconf_remove_comments(lconf__obj)
   tools.ok_('#2' in lconf__obj__no_comments, msg='Expected: AssertionError: for key `#2` after lconf_remove_comments')


@tools.raises(Err)
def test__parse_section_extract_by_name__expect_failure():
   """ Tests: test__parse_section_extract_by_name__expect_failure
   """
   print('::: TEST: test__parse_section_extract_by_name__expect_failure()')
   lconf__obj = lconf_parse_section_extract_by_name(example_lconf_section_str, 'WrongSectionName', example_template, validate=True)


def test__parse_section_extract_by_name():
   """ Tests: test__parse_section_extract_by_name
   """
   print('::: TEST: test__parse_section_extract_by_name()')
   result_parse1 = lconf_parse_section_extract_by_name(example_lconf_section_str, 'BaseEXAMPLE', example_template, validate=False)

   tools.eq_(result_parse1.extra_data['l_section_name'], 'BaseEXAMPLE', msg=None)

   # do some additional checks
   result_emit1 = lconf_emit(result_parse1, onelinelists=False, with_comments=True)

   lconf_obj2 = lconf_prepare_default_obj(example_template_no_cast)
   result_parse2 = lconf_parse_section(lconf_obj2, result_emit1, example_template_no_cast)
   result_emit3 = lconf_emit(result_parse2, onelinelists=False, with_comments=True)

   tools.eq_(result_emit1, result_emit3, msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':

   test_parse_section_access_each_attribute()
   test_parse_section_access_none_existing_key__expect_failure()
   test_parse_section_wrong_key__expect_failure()
   test_parse_section_wrong_blk_identifier__expect_failure()
   test_parse_section_wrong_blk_key__expect_failure()

   test__parse_emit1()
   test__parse_emit2()
   test__parse_emit2b()
   test__parse_emit3()
   test__parse_emit3b()
   test__parse_emit4()
   test__parse_emit4b()
   test__parse_emit5()
   test__parse_emit5b()
   test__emit_none_parsed_lconf_obj_reparse()
   test__emit_none_parsed_lconf_obj_reparse2()
   test__emit_none_parsed_lconf_obj_reparse3()
   test__emit_none_parsed_lconf_obj_reparse4()

   test_parse_get_value1()
   test_parse_get_value2()

   test__parse_a_dict()
   test__parse_a_dict2()

   test__check_indent_for_emit_with_comments1()
   test__check_indent_for_emit_with_comments2()
   test__check_indent_for_emit_with_comments3()
   test__check_indent_for_emit_with_comments4()

   test__check_lconf_remove_comments()

   test__parse_section_extract_by_name__expect_failure()
   test__parse_section_extract_by_name()
