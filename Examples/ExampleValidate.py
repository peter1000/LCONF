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


from LCONF.MainCode import lconf_validate_source


example_lconf_section_str = r'''___SECTION :: BASE_EXAMPLE

key1value_pair :: value1
# Comment line: below is a key value pair with an empty string value
key2value_pair ::

# Comment line: below is a key value list using indentation
key3list
   # Comment:  List item
   value_list_item1
   value_list_item2

# Comment line: below is a key value list using key/value pair separator
key4value_pairlist :: [value_list_item1,value_list_item2]

# Comment: Repeated BLK identifier
* RepeatedBlk
___SECTION
   # Comment: Repeated Block Name
   BLK_OBJ1
      # Comment: Repeated Block KEY: is a key value pair with an empty string value
      BLK_key1 ::
      BLK_key2list
         # Comment: Repeated Block List item
         BLK_value_list_item1
         BLK_value_list_item2

   # Comment: Repeated Block Name
   BLK_OBJ2
      BLK_key1 :: BLK_value1
___END
'''


def main():

   lconf_validate_source(example_lconf_section_str)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
