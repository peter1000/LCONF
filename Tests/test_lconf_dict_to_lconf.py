""" tests lconf dict to lconf
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
   ok_,
   raises as nose_raises
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.main_code import (
   lconf_dict_to_lconf,
   lconf_validate_source,
   lconf_section_splitlines,
)
from LCONF.utils import Err


def test__parse_a_regular_dict_to_lconf1():
   """ Tests: test__parse_a_regular_dict_to_lconf1
   """
   print('::: TEST: test__parse_a_regular_dict_to_lconf1()')
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

   result_dict_to_lconf_str = lconf_dict_to_lconf(example_dict, 'PERMISSIONS', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_dict_to_lconf2():
   """ Tests: test__parse_a_regular_dict_to_lconf2
   """
   print('::: TEST: test__parse_a_regular_dict_to_lconf2()')
   example_dict = {
      '___SECTION': 'PERMISSIONS',
      'description': 'A trivial terminal emulator',
      'maintainer': 'Timothy Hobbs < (at)  dot cz>',
      'last_update_time': '2014_02_12_12:59',
      'dependency': 'libx11',
      'executable': '/usr/bin/xterm',
      'x11': [123.0, 123],
      'sound_card': False,
      'inherit_working_directory': None,
      '___END': None
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(example_dict, 'PERMISSIONS', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(example_dict, 'PERMISSIONS', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_nested_dict_to_lconf1():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf1
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf1()')

   nested_dict = {
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
         "test_mapping_key3": 'value',
         "test_mapping_key4": '',
      }
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'PERMISSIONS', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('- x11 :: 123.0,123' in section_lines, msg=None)
   ok_('   test_mapping_key1 ::' in section_lines, msg=None)
   ok_('   test_mapping_key3 ::' in section_lines, msg=None)
   ok_('   test_mapping_key4 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'PERMISSIONS', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('- x11' in section_lines, msg=None)
   ok_('   test_mapping_key1 ::' in section_lines, msg=None)
   ok_('   test_mapping_key3 ::' in section_lines, msg=None)
   ok_('   test_mapping_key4 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'PERMISSIONS', onelinelists=True, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('- x11 :: 123.0,123' in section_lines, msg=None)
   ok_('   test_mapping_key1 :: None' in section_lines, msg=None)
   ok_('   test_mapping_key3 ::' in section_lines, msg=None)
   ok_('   test_mapping_key4 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'PERMISSIONS', onelinelists=False, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('- x11' in section_lines, msg=None)
   ok_('   test_mapping_key1 :: None' in section_lines, msg=None)
   ok_('   test_mapping_key3 ::' in section_lines, msg=None)
   ok_('   test_mapping_key4 ::' in section_lines, msg=None)


def test__parse_a_regular_nested_dict_to_lconf2():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf2
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf2()')

   nested_dict = {
      "first": "John",
      "last": "Doe",
      "age": 39,
      "interests": [
         "Reading",
         "Mountain Biking",
         "Hacking"
      ],
      "registered": 'true',
      "salary": 70000,
      "sex": "M"
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 2', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 2', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_nested_dict_to_lconf3():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf3
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf3()')

   nested_dict = {
      "first": "John",
      "last": "Doe",
      "sex": "M",
      "age": 39,
      "salary": 70000,
      "favorites": {
         "food": "Spaghetti",
         "sport": "Soccer",
         "color": "Blue"
      },
      "registered": 'true'
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 3', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 3', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_nested_dict_to_lconf4():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf4
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf4()')

   nested_dict = {
      "registered_employees": 28594,
      "Employee": {
         "Person1": {
            "first": "John",
            "last": "Doe",
            "sex": "M",
            "age": "39",
            "past_salary": {
               "year2012": 45000,
               "year2013": 62000
            },
            "emails": [
               "<xaver@dot.com>",
               "<xaver23@yahoo.com>"
            ]
         }
      },
      "registered_customer": 28594,
      "accounting": [
         [
            "2010",
            38459845,
            15835945,
            3000945
         ],
         [
            "2011",
            38459845,
            15835945,
            3000945
         ],
         [
            "2012",
            28456849,
            4846123,
            2599901
         ],
         [
            "2013",
            38459845,
            15835945,
            3000945
         ]
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 4', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 4', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf5_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf5_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf5_expect_failure()')

   nested_dict = {
      "skills": [
         {
            "category": "PHP",
            "tests": [
               {
                  "score": 90,
                  "name": "One"
               },
               {
                  "score": 96,
                  "name": "Two"
               }
            ]
         },
         {
            "category": "Node.js",
            "tests": [
               {
                  "score": 97,
                  "name": "One"
               },
               {
                  "score": 93,
                  "name": "Two"
               }
            ]
         }
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 5', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf6_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf6_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf6_expect_failure()')

   nested_dict = {
      "skills": [
         {
            "category": "PHP",
            "tests": [
               {
                  "score": 90,
                  "name": "One"
               },
               {
                  "score": 96,
                  "name": "Two"
               }
            ]
         },
         {
            "category": "Node.js",
            "tests": [
               {
                  "score": 97,
                  "name": "One"
               },
               {
                  "score": 93,
                  "name": "Two"
               }
            ]
         }
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'Json EXAMPLE 5', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf7_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf7_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf7_expect_failure()')

   nested_dict = {
      "accounting": [
         [
            "2010",
            38459845,
            15835945,
            3000945
         ],
         [
            "2011",
            38459845,
            15835945,
            3000945
         ],
         [
            "2012",
            28456849,
            4846123,
            2599901
         ],
         [
            "2013",
            38459845,
            15835945,
            3000945
         ],
         {'wrong': '1'}
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf8_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf8_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf7_expect_failure()')

   nested_dict = {
      "accounting": [
         [
            "2010",
            38459845,
            15835945,
            3000945
         ],
         [
            "2011",
            38459845,
            15835945,
            3000945
         ],
         [
            "2012",
            28456849,
            4846123,
            2599901
         ],
         [
            "2013",
            38459845,
            15835945,
            3000945
         ],
         {'wrong': '1'}
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf9_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf9_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf9_expect_failure()')

   nested_dict = {
      "accounting": [
         [
            "2010",
            38459845,
            15835945,
            3000945
         ],
         [
            "2011",
            38459845,
            15835945,
            3000945
         ],
         [
            "2012",
            28456849,
            4846123,
            2599901
         ],
         [
            "2013",
            38459845,
         ]
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


@nose_raises(Err)
def test__parse_a_regular_nested_dict_to_lconf10_expect_failure():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf10_expect_failure
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf10_expect_failure()')

   nested_dict = {
      "accounting": [
         [
            "2010",
            38459845,
            15835945,
            3000945
         ],
         [
            "2011",
            38459845,
            15835945,
            3000945
         ],
         [
            "2012",
            28456849,
            4846123,
            2599901
         ],
         [
            "2013",
            38459845,
         ]
      ]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_nested_dict_to_lconf11():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf11
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf11()')

   nested_dict = {
      "empty_list": [],
      "normal_list": [1, 2, 3]
   }

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)


def test__parse_a_regular_nested_dict_to_lconf12():
   """ Tests: test__parse_a_regular_nested_dict_to_lconf12
   """
   print('::: TEST: test__parse_a_regular_nested_dict_to_lconf12()')

   nested_dict = {
      "accounting": {
         "nested": {
            "Inner": 'something'
         },
         "nested key": None,
         "nested key2": False,
         "nested key3": '',
         "nested list1": [],
         "nested list2": [1, 2, 3],
      },
      "key": None,
      "key2": False,
      "key3": '',
      "list1": [],
      "list2": [1, 2, 3]
   }
   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('   nested key ::' in section_lines, msg=None)
   ok_('   nested key2 :: False' in section_lines, msg=None)
   ok_('   nested key3 ::' in section_lines, msg=None)
   ok_('key ::' in section_lines, msg=None)
   ok_('key2 :: False' in section_lines, msg=None)
   ok_('key3 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('   nested key :: None' in section_lines, msg=None)
   ok_('   nested key2 :: False' in section_lines, msg=None)
   ok_('   nested key3 ::' in section_lines, msg=None)
   ok_('key :: None' in section_lines, msg=None)
   ok_('key2 :: False' in section_lines, msg=None)
   ok_('key3 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=True)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('   nested key ::' in section_lines, msg=None)
   ok_('   nested key2 :: False' in section_lines, msg=None)
   ok_('   nested key3 ::' in section_lines, msg=None)
   ok_('key ::' in section_lines, msg=None)
   ok_('key2 :: False' in section_lines, msg=None)
   ok_('key3 ::' in section_lines, msg=None)

   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=False, skip_none_value=False)
   lconf_validate_source(result_dict_to_lconf_str)
   section_lines, section_name = lconf_section_splitlines(result_dict_to_lconf_str, validate_first_line=False)
   ok_('   nested key :: None' in section_lines, msg=None)
   ok_('   nested key2 :: False' in section_lines, msg=None)
   ok_('   nested key3 ::' in section_lines, msg=None)
   ok_('key :: None' in section_lines, msg=None)
   ok_('key2 :: False' in section_lines, msg=None)
   ok_('key3 ::' in section_lines, msg=None)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test__parse_a_dict_to_lconf_wrong_list_itemtype_expect_failure():
   """ Tests: test__parse_a_dict_to_lconf_wrong_list_itemtype_expect_failure
   """
   print('::: TEST: test__parse_a_dict_to_lconf_wrong_list_itemtype_expect_failure()')

   nested_dict = {
      "skills": [
         {
            "category": "PHP",
            "tests": [
               {
                  "score": 90,
                  "name": "One"
               },
               {
                  "score": 96,
                  "name": "Two"
               }
            ]
         },
         {
            "category": "Node.js",
            "tests": [
               {
                  "score": 97,
                  "name": "One"
               },
               {
                  "score": 93,
                  "name": "Two"
               }
            ]
         }
      ]
   }
   result_dict_to_lconf_str = lconf_dict_to_lconf(nested_dict, 'example', onelinelists=True, skip_none_value=True)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test__parse_a_regular_dict_to_lconf1()
   test__parse_a_regular_dict_to_lconf2()

   test__parse_a_regular_nested_dict_to_lconf1()
   test__parse_a_regular_nested_dict_to_lconf2()
   test__parse_a_regular_nested_dict_to_lconf3()
   test__parse_a_regular_nested_dict_to_lconf4()

   test__parse_a_regular_nested_dict_to_lconf5_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf6_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf7_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf8_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf9_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf10_expect_failure()
   test__parse_a_regular_nested_dict_to_lconf11()

   test__parse_a_regular_nested_dict_to_lconf12()

   test__parse_a_dict_to_lconf_wrong_list_itemtype_expect_failure()
