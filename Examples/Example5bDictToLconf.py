""" Example implementation
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


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import lconf_dict_to_lconf


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


def main():

   result_dict_to_lconf = lconf_dict_to_lconf(example_nested_dict, 'PERMISSIONS', onelinelists=False, skip_none_value=True)
   print('\n=== result_dict_to_lconf: onelinelists=True  sort_first_dict_keys=False\n{}'.format(result_dict_to_lconf))


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
