""" Example: parse_lconf_json1.py
"""
from collections import OrderedDict
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from json import (
   loads as json_loads
)
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path


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
)

from LCONF.main_code import (
   lconf_prepare_and_parse_section
)


example_template_no_cast = Root([
   ('key1value_pair', ''),
   ('key2value_pair', ''),
   ('key3value_pair', ''),
   ('key4value_pair', ''),
   ('key5value_pair', ''),
   ('key6value_pair', ''),
   ('key7value_pair', ''),
   ('key8value_pair', ''),
   ('key9value_pair', ''),

   # Main `Key-Value-Mapping:
   ('key10value_mapping', KVMap([
      ('mapping10_key1', ''),
      ('mapping10_key2', ''),
      ('mapping10_key3', ''),
      ('mapping10_key4', ''),
      ('mapping10_key5', ''),
      ('mapping10_key6', ''),
   ])),

   # Main `Key-Value-Mapping:
   ('key11value_mapping', KVMap([
      ('mapping11_key1', ''),
      ('mapping11_key2', ''),
   ])),

   ('key12list', KVList(True, [])),
   ('key13value_pairlist', KVList(False, [])),
   ('key14value_pairlist', KVList(False, ['1', '2', '3'])),


   # Repeated Mapping-Block Identifier:
   ('RepeatedBlk1', BlkI(2, 5,
      Blk([
         # Block-Item `Key-Value-Mapping`
         ('MyKey1mapping', KVMap([
            ('blk_mapping_key1', ''),
            ('blk_mapping_key2', ''),
            ('blk_mapping_key3', ''),
         ])),

         ('MyKey2', ''),
         ('MyKey3', ''),
         ('MyKey4', ''),
         ('MyKey5list', KVList(True, [])),
         ('MyKey6list', KVList(False, ['1', '2', '3'])),
         ('MyKey7list', KVList(False, [])),
         ('MyKey8', ''),
      ])
   ))
])

example_lconf_section_str_no_comments = r'''___SECTION :: Example
key1value_pair :: value1
key2value_pair ::
key3value_pair :: 1234
key4value_pair :: True
key5value_pair :: False
key6value_pair :: None
key7value_pair :: 1456.984
key8value_pair :: true
key9value_pair :: false
. key10value_mapping
   mapping10_key1 :: null
   mapping10_key2 :: true
   mapping10_key3 :: 123456
   mapping10_key4 :: False
   mapping10_key5 :: None
   mapping10_key6 :: 0001-01-01-00:00
. key11value_mapping
   mapping11_key1 :: null
   mapping11_key2 :: ''
- key12list :: value_list_item1,value_list_item2
- key13value_pairlist
   123
   8945
   278
- key14value_pairlist
* RepeatedBlk1
   BLK_OBJ0
      . MyKey1mapping
         blk_mapping_key1 :: some text
         blk_mapping_key2 :: 12345.99
         blk_mapping_key3 :: True
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-08-13:45
      - MyKey5list :: test1,test2
      - MyKey6list
      - MyKey7list
         True
         False
         False
         True
      MyKey8 :: some text
   BLK_OBJ1
      . MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 999.0
      MyKey3 ::
      MyKey4 :: 1970-01-01 00:00:00
      - MyKey5list ::
      - MyKey6list
         1
         2
         3
      - MyKey7list
      MyKey8 ::
   BLK_OBJ2
      . MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 89456.456
      MyKey3 :: True
      MyKey4 :: 1982-02-26-12:15
      - MyKey5list ::
      - MyKey6list
         1
         2
         3
      - MyKey7list
         True
         False
         False
         True
      MyKey8 ::
   BLK_OBJ3
      . MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 188.0
         blk_mapping_key3 :: False
      MyKey2 :: 789.9
      MyKey3 :: True
      MyKey4 :: 2014-05-12-01:52
      - MyKey5list :: dog,cat
      - MyKey6list
         1
         2
         3
      - MyKey7list
      MyKey8 :: just a test
   BLK_OBJ4
      . MyKey1mapping
         blk_mapping_key1 ::
         blk_mapping_key2 :: 0.0
         blk_mapping_key3 :: False
      MyKey2 :: 0.0
      MyKey3 ::
      MyKey4 :: 1970-01-01 00:00:00
      - MyKey5list ::
      - MyKey6list
         1
         2
         3
      - MyKey7list
      MyKey8 ::
___END'''

example_json_str = '''
{
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
}
'''


# noinspection PyUnusedLocal
def do_parse__lconf():
   parsed_lconf = lconf_prepare_and_parse_section(
      example_lconf_section_str_no_comments,
      example_template_no_cast
   )
   # print(parsed_lconf)


# noinspection PyUnusedLocal
def do_parse__json_ordered():
   parsed_json = json_loads(example_json_str, object_pairs_hook=OrderedDict)
   # print(parsed_json)


# noinspection PyUnusedLocal
def do_parse__json():
   parsed_json = json_loads(example_json_str)
   # print(parsed_json)


# do_parse__lconf()
# do_parse__json_ordered()
# do_parse__json()
