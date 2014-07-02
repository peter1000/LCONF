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


example_lconf_section_str = r'''
some text outside



more text
___SECTION :: PERSON
age :: 39
* favorites
   BLK0
      color :: Blue
      food :: Spaghetti
      sport :: Soccer
first :: John
last :: Doe
registered :: true
salary :: 70000
sex :: M
___END

more text
___SECTION :: TEST
country :: Italy
* Cars
   Car0
      price  :: 1000

___END

any other text
'''


def main():
   lconf_validate_source(example_lconf_section_str)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
