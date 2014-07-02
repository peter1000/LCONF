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
   RdictFO2,
   RdictIO
)

SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import (
   lconf_emit,
   lconf_extract_one_section_by_name,
   lconf_prepare_and_parse_section,
   lconf_validate_file
)
from LCONF.Transform import (
   lconf_to_bool,
   lconf_to_datetime,
   lconf_to_float,
   lconf_to_int,
   lconf_to_number
)


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
   example_file = join(SCRIPT_PATH, 'example1_from_file_lconfspecification.lconf')
   # VALIDATE FILE
   lconf_validate_file(example_file)

   # Read the file content: all in one
   with open(example_file, 'r') as file_:
      # if one knows the name of the section one can do it like: which is faster to extract
      section_str = lconf_extract_one_section_by_name(file_.read(), 'BaseEXAMPLE')

      result1 = lconf_prepare_and_parse_section(section_str, example_template, validate=False)


      #print('\n=== result1: ', result1)
      # Accessing:  The Section-INFO
      print('\n\n=== result1: The Section ===')
      print('  result1.extra_data[l_section_name]: ', result1.extra_data['l_section_name'])
      print('  result1.extra_data[l_parsed]: ', result1.extra_data['l_parsed'])
      #

      print('  result1.key1value_pair: ', type(result1['key1value_pair']), result1['key1value_pair'])
      print('  result1.key2value_pair: ', type(result1['key2value_pair']), result1['key2value_pair'])
      print('  result1.key3value_pair: ', type(result1['key3value_pair']), result1['key3value_pair'])
      print('  result1.key4value_pair: ', type(result1['key4value_pair']), result1['key4value_pair'])
      print('  result1.key5value_pair: ', type(result1['key5value_pair']), result1['key5value_pair'])
      print('  result1.key6value_pair: ', type(result1['key6value_pair']), result1['key6value_pair'])
      print('  result1.key7value_pair: ', type(result1['key7value_pair']), result1['key7value_pair'])
      print('  result1.key8value_pair: ', type(result1['key8value_pair']), result1['key8value_pair'])
      print('  result1.key9value_pair: ', type(result1['key9value_pair']), result1['key9value_pair'])

      # Main `Key-Value-Mapping:ITEMS: using loop: but could be also accessed directly: e.g. result1['key10value_mapping']['mapping10_key1']
      # looping through the: Key-Value-Mapping
      print('  looping through the: Key-Value-Mapping:ITEMS:key10value_mapping: ')
      for this_key, this_value in result1['key10value_mapping'].yield_key_value_order():
         print('     this_key.{}: '.format(this_key), type(this_value), this_value)

      # Main `Key-Value-Mapping:ITEMS:  accessed directly
      print('  result1.key11value_mapping.mapping11_key1: ', type(result1['key11value_mapping']['mapping11_key1']), result1['key11value_mapping']['mapping11_key1'])
      print('  result1.key11value_mapping.mapping11_key2: ', type(result1['key11value_mapping']['mapping11_key2']), result1['key11value_mapping']['mapping11_key2'])

      # Main `Key-Value-List`
      # looping through the: Key-Value-List
      print('  looping through the: Key-Value-List:Values:key12list: ', type(result1['key12list']), result1['key12list'])
      for value in result1['key12list']:
         print('     key12list.value: ', type(value), value)

      # Main `Key-Value-List`
      # looping through the: Key-Value-List
      print('  looping through the: Key-Value-List:Values:key13value_pairlist: ', type(result1['key13value_pairlist']), result1['key13value_pairlist'])
      for value in result1['key13value_pairlist']:
         print('     key13value_pairlist.value: ', type(value), value)

      # Main `Key-Value-List`
      # looping through the: Key-Value-List
      print('  looping through the: Key-Value-List:Values:key14value_pairlist: ', type(result1['key14value_pairlist']), result1['key14value_pairlist'])
      for value in result1['key14value_pairlist']:
         print('     key14value_pairlist.value: ', type(value), value)

      # Repeated Mapping-Block Identifier: type: RdictIO
      print('\n  result1.RepeatedBlk1: ', type(result1['RepeatedBlk1']))
      # if the Mapping-Block: Name is known one can access the items directly like: result1['RepeatedBlk1']['BLK_OBJ0']['MyKey1mapping']
      print('     result1[RepeatedBlk][BLK_OBJ0][MyKey1mapping]: ', type(result1['RepeatedBlk1']['BLK_OBJ0']['MyKey1mapping']), result1['RepeatedBlk1']['BLK_OBJ0']['MyKey1mapping'])
      print('  looping through the: Mapping-Block-Names: ')

      for blk_name, block_obj in result1['RepeatedBlk1'].yield_key_value_order():
         print('     blk_name: ', type(blk_name), blk_name)

         # Block `Key-Value-Mapping:ITEMS:
         # looping through the: Key-Value-Mapping
         print('  looping through the: Key-Value-Mapping:ITEMS:MyKey1mapping: ', type(block_obj['MyKey1mapping']))
         for this_key, this_value in block_obj['MyKey1mapping'].yield_key_value_order():
            print('     this_key.{}: '.format(this_key), type(this_value), this_value)

         print('  block_obj[MyKey2]: ', type(block_obj['MyKey2']), block_obj['MyKey2'])
         print('  block_obj[MyKey3]: ', type(block_obj['MyKey3']), block_obj['MyKey3'])
         print('  block_obj[MyKey4]: ', type(block_obj['MyKey4']), block_obj['MyKey4'])

         # Block-Item `Key Value-List`
         # looping through the: Key-Value-List
         print('  looping through the: Block-Item `Key Value-List:MyKey5list: ', type(block_obj['MyKey5list']), block_obj['MyKey5list'])
         for value in block_obj['MyKey5list']:
            print('     block_obj.MyKey5list.value: ', type(value), value)

         # looping through the: Key-Value-List
         print('  looping through the: Block-Item `Key Value-List:MyKey6list: ', type(block_obj['MyKey6list']), block_obj['MyKey6list'])
         for value in block_obj['MyKey6list']:
            print('     block_obj.MyKey6list.value: ', type(value), value)

         # looping through the: Key-Value-List
         print('  looping through the: Block-Item `Key Value-List:MyKey7list: ', type(block_obj['MyKey7list']), block_obj['MyKey7list'])
         for value in block_obj['MyKey7list']:
            print('     block_obj.MyKey7list.value: ', type(value), value)

         print('  block_obj[MyKey8]: ', type(block_obj['MyKey8']), block_obj['MyKey8'])


      # IMPORTANT: because of type conversion the item: Main `key10value_mapping- mapping10_key6` and `RepeatedBlk1 - MyKey4` can not be simple dumped
      # so we convert it first into a correct string format `YYYY-MM-DD-hh:mm`.
      # NOTE this will change the: result1

      if result1['key10value_mapping']['mapping10_key6']:
         result1['key10value_mapping']['mapping10_key6'] = result1['key10value_mapping']['mapping10_key6'].strftime('%Y-%m-%d-%H:%M')
      # loop through all BLKs
      for blk_name, block_obj in result1['RepeatedBlk1'].yield_key_value_order():
         if block_obj['MyKey4']:
            block_obj['MyKey4'] = block_obj['MyKey4'].strftime('%Y-%m-%d-%H:%M')

      emit_result = lconf_emit(result1, onelinelists=True)
      print('\n\n===  ===  === emit_result: ===  ===  === \n\n', emit_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
