""" SpeedCheckParse
"""
from collections import OrderedDict
from inspect import (
   getfile,
   currentframe
)
from json import (
   loads as jloads
)
from os.path import (
   abspath,
   dirname,
   join
)
import sys
from sys import path as syspath

try:
   from SpeedIT.BenchmarkIT import speedit_func_benchmark_list
except ImportError as err:
   sys.exit('Example SpeedTest: Can not run example. This example needs the package <SpeedIT> to be installed: <{}>'.format(err))

from RDICT.MainCode import (
   RdictIO,
   RdictFO2
)


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import (
   lconf_parse_section_pickled,
   lconf_prepare_and_parse_section,
   lconf_prepare_default_obj_pickled
)


# Main `Section-Template OBJ: type: RdictFO2
example_template_no_cast = RdictFO2([
   ('key1value_pair', ''),
   ('key2value_pair', ''),
   ('key3value_pair', ''),
   ('key4value_pair', ''),
   ('key5value_pair', ''),
   ('key6value_pair', ''),
   ('key7value_pair', ''),
   ('key8value_pair', ''),
   ('key9value_pair', ''),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('key10value_mapping', RdictFO2([
      ('mapping10_key1', ''),
      ('mapping10_key2', ''),
      ('mapping10_key3', 0),
      ('mapping10_key4', ''),
      ('mapping10_key5', ''),
      ('mapping10_key6', ''),
   ])),

   # Main `Key-Value-Mapping: type: RdictFO2
   ('key11value_mapping', RdictFO2([
      ('mapping11_key1', ''),
      ('mapping11_key2', ''),
   ])),

   ('key12list', []),
   ('key13value_pairlist', []),
   ('key14value_pairlist', ['1', '2', '3']),


   # Repeated Mapping-Block Identifier: type: RdictIO
   ('RepeatedBlk1', RdictIO([
      # Repeated Block-Name: default dummy: must be named: `dummy_blk`: type: RdictFO2
      ('dummy_blk', RdictFO2([

         # Block-Item `Key-Value-Mapping`: type: RdictFO2
         ('MyKey1mapping', RdictFO2([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', ''),
            ('blk_mapping_key3', ''),
         ])),

         ('MyKey2', ''),
         ('MyKey3', ''),
         ('MyKey4', ''),
         ('MyKey5list', []),
         ('MyKey6list', ['1', '2', '3']),
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

example_json_section_str = '''{
   "key1value_pair": "value1",
   "key2value_pair": "",
   "key3value_pair": "1234",
   "key4value_pair": "True",
   "key5value_pair": "False",
   "key6value_pair": "None",
   "key7value_pair": "1456.984",
   "key8value_pair": "true",
   "key9value_pair": "false",
   "key10value_mapping": {
      "mapping10_key1": "null",
      "mapping10_key2": "true",
      "mapping10_key3": "123456",
      "mapping10_key4": "False",
      "mapping10_key5": "None",
      "mapping10_key6": "0001-01-01-00:00"
   },
   "key11value_mapping": {
      "mapping11_key1": "null",
      "mapping11_key2": "''"
   },
   "key12list": [
      "value_list_item1",
      "value_list_item2"
   ],
   "key13value_pairlist": [
      "123",
      "8945",
      "278"
   ],
   "key14value_pairlist": [],
   "RepeatedBlk1": {
      "BLK_OBJ0": {
         "MyKey1mapping": {
            "blk_mapping_key1": "some text",
            "blk_mapping_key2": "12345.99",
            "blk_mapping_key3": "True"
         },
         "MyKey2": "789.9",
         "MyKey3": "True",
         "MyKey4": "2014-05-08-13:45",
         "MyKey5list": [
            "test1",
            "test2"
         ],
         "MyKey6list": [],
         "MyKey7list": [
            "True",
            "False",
            "False",
            "True"
         ],
         "MyKey8": "some text"
      },
      "BLK_OBJ1": {
         "MyKey1mapping": {
            "blk_mapping_key1": "",
            "blk_mapping_key2": "0.0",
            "blk_mapping_key3": "False"
         },
         "MyKey2": "999.0",
         "MyKey3": "",
         "MyKey4": "1970-01-01 00:00:00",
         "MyKey5list": [],
         "MyKey6list": [
            "1",
            "2",
            "3"
         ],
         "MyKey7list": [],
         "MyKey8": ""
      },
      "BLK_OBJ2": {
         "MyKey1mapping": {
            "blk_mapping_key1": "",
            "blk_mapping_key2": "0.0",
            "blk_mapping_key3": "False"
         },
         "MyKey2": "89456.456",
         "MyKey3": "True",
         "MyKey4": "1982-02-26-12:15",
         "MyKey5list": [],
         "MyKey6list": [
            "1",
            "2",
            "3"
         ],
         "MyKey7list": [
            "True",
            "False",
            "False",
            "True"
         ],
         "MyKey8": ""
      },
      "BLK_OBJ3": {
         "MyKey1mapping": {
            "blk_mapping_key1": "",
            "blk_mapping_key2": "188.0",
            "blk_mapping_key3": "False"
         },
         "MyKey2": "789.9",
         "MyKey3": "True",
         "MyKey4": "2014-05-12-01:52",
         "MyKey5list": [
            "dog",
            "cat"
         ],
         "MyKey6list": [
            "1",
            "2",
            "3"
         ],
         "MyKey7list": [],
         "MyKey8": "just a test"
      },
      "BLK_OBJ4": {
         "MyKey1mapping": {
            "blk_mapping_key1": "",
            "blk_mapping_key2": "0.0",
            "blk_mapping_key3": "False"
         },
         "MyKey2": "0.0",
         "MyKey3": "",
         "MyKey4": "1970-01-01 00:00:00",
         "MyKey5list": [],
         "MyKey6list": [
            "1",
            "2",
            "3"
         ],
         "MyKey7list": [],
         "MyKey8": ""
      }
   }
}'''


parsed_lconf = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast, validate=True)
parsed_json = jloads(example_json_section_str)
parsed_ordered_json = jloads(example_json_section_str, object_pairs_hook=OrderedDict)


def parse__lconf():
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_prepare_and_parse_section(example_lconf_section_str_no_comments, example_template_no_cast)
   #print(parsed_lconf)


def parse__lconf_pickled():
   lconf_default_obj_pickled = lconf_prepare_default_obj_pickled(example_template_no_cast)

   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   parsed_lconf1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str_no_comments, example_template_no_cast)
   #print(parsed_lconf)


def parse__json():
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   parsed_json1 = jloads(example_json_section_str)
   #print(parsed_json)


def parse__json_ordereddict():
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   parsed_ordered_json1 = jloads(example_json_section_str, object_pairs_hook=OrderedDict)
   #print(parsed_ordered_json)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():

   func_dict = {
      'lconf_prepare_and_parse_section': (parse__lconf, [], {}),
      'lconf_parse_section_pickled': (parse__lconf_pickled, [], {}),
      'parse__json not ordered': (parse__json, [], {}),
      'parse__json ordereddict': (parse__json_ordereddict, [], {}),
   }

   setup_line_list = [
      'from collections import OrderedDict',
      'from json import dumps as jdumps, loads as jloads',
      'from LCONF.MainCode import lconf_emit, lconf_parse_section_pickled, lconf_prepare_and_parse_section, lconf_prepare_default_obj_pickled',
      'from __main__ import example_lconf_section_str_no_comments, example_template_no_cast, example_json_section_str'
   ]

   check_run_sec = 1
   with open('result_output/SpeedCheckParse.txt', 'w') as file_:
      file_.write('\n\n SpeedCheckParse.py output\n\n')
      for count in range(3):
         file_.write('\n'.join(speedit_func_benchmark_list(func_dict, setup_line_list, run_sec=check_run_sec, out_put_in_sec=False, use_func_name=False)))
         file_.write('\n\n')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
