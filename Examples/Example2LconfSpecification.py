""" Example implementation: of the documentation: docs/source/main_docs/LCONF_Specification-4.1.rst: 'EXAMPLE 2 (JSON - LCONF)'
                                                                                                      using the: LCONF Key-Value-List
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
   lconf_prepare_and_parse_section
)
from LCONF.Transform import (lconf_to_bool, lconf_to_int)


example_lconf_section_str = r'''___SECTION :: PERSON
first :: John
last :: Doe
age :: 39
# Key-Value-List
interests
   Reading
   Mountain Biking
   Hacking
registered :: true
salary :: 70000
sex :: M
___END
'''

example_template = RdictFO2([
   ('first', ''),
   ('last', ''),
   ('age', (0, lconf_to_int)),
   # Key-Value-List: using as default an empty list
   ('interests', []),
   ('registered', (False, lconf_to_bool)),
   ('salary', (0, lconf_to_int)),
   ('sex', ''),
])


def main():
   # Prepare: a default lconf obj from the template obj and parse the LCONF-Section string
   result1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=False)
   #print('\n=== result1: ', result1)

   print('  result1.extra_data[l_section_name]: ', result1.extra_data['l_section_name'])
   print('  result1.extra_data[l_parsed]: ', result1.extra_data['l_parsed'])
   print('  result1.first: ', type(result1['first']), result1['first'])
   print('  result1.last: ', type(result1['last']), result1['last'])
   print('  result1.age: ', type(result1['age']), result1['age'])
   print('  result1.interests: ', type(result1['interests']), result1['interests'])
   # looping through the: Key-Value-List
   for this_value in result1['interests']:
      print('     this_value: ', type(this_value), this_value)
   print('  result1.registered: ', type(result1['registered']), result1['registered'])
   print('  result1.salary: ', type(result1['salary']), result1['salary'])
   print('  result1.sex: ', type(result1['sex']), result1['sex'])

   emit_result = lconf_emit(result1, onelinelists=True)
   print('\n\n===  ===  === emit_result: ===  ===  === \n\n', emit_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
