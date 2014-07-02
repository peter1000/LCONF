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

from RDICT.MainCode import RdictFO2


SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.MainCode import (
   lconf_emit,
   lconf_parse_section,
   lconf_prepare_default_obj
)
from LCONF.Transform import (lconf_to_bool, lconf_to_int)


example_lconf_section_str1 = r'''___SECTION :: PERSON1
first :: John
last :: Doe
age :: 39
interests :: [Reading,Mountain Biking,Hacking]
registered :: true
salary :: 70000
sex :: M
___END
'''


example_template = RdictFO2([
   ('#1', 'This is a Comment Line'),
   ('first', ''),
   ('last', ''),
   ('age', (0, lconf_to_int)),
   ('interests', []),
   ('registered', (False, lconf_to_bool)),
   ('salary', (0, lconf_to_int)),
   ('sex', ''),
])


def main():
   lconf_default_obj = lconf_prepare_default_obj(example_template)
   print('  lconf_default_obj.extra_data[l_section_name]: ', lconf_default_obj.extra_data['l_section_name'])
   print('  lconf_default_obj.extra_data[l_parsed]: ', lconf_default_obj.extra_data['l_parsed'])

   lconf_parse_section(lconf_default_obj, example_lconf_section_str1, example_template)

   print('\n=== lconf_default_obj: ', lconf_default_obj)
   print('  lconf_default_obj.extra_data[l_section_name]: ', lconf_default_obj.extra_data['l_section_name'])
   print('  lconf_default_obj.extra_data[l_parsed]: ', lconf_default_obj.extra_data['l_parsed'])
   print('  lconf_default_obj.first: ', type(lconf_default_obj['first']), lconf_default_obj['first'])
   print('  lconf_default_obj.last: ', type(lconf_default_obj['last']), lconf_default_obj['last'])
   print('  lconf_default_obj.age: ', type(lconf_default_obj['age']), lconf_default_obj['age'])
   print('  lconf_default_obj.interests: ', type(lconf_default_obj['interests']), lconf_default_obj['interests'])
   # looping through the: Key :: Value-Lists
   for this_value in lconf_default_obj['interests']:
      print('     this_value: ', type(this_value), this_value)
   print('  lconf_default_obj.registered: ', type(lconf_default_obj['registered']), lconf_default_obj['registered'])
   print('  lconf_default_obj.salary: ', type(lconf_default_obj['salary']), lconf_default_obj['salary'])
   print('  lconf_default_obj.sex: ', type(lconf_default_obj['sex']), lconf_default_obj['sex'])

   emit_result = lconf_emit(lconf_default_obj, onelinelists=True)
   print('\n\n===  ===  === emit_result: ===  ===  === \n\n', emit_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
