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
   lconf_parse_section_pickled,
   lconf_prepare_default_obj_pickled
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

example_lconf_section_str2 = r'''___SECTION :: PERSON2
first :: Peter
last :: Bond
age :: 12
interests :: [Boxing,Reading,Cooking]
registered :: false
salary :: 1
sex :: M
___END
'''

example_lconf_section_str3 = r'''___SECTION :: PERSON3
first :: Rosalie
last :: Herold
age :: 58
interests :: [Cooking,Movie]
registered :: True
salary :: 15894
sex :: F
___END
'''

example_template = RdictFO2([
   ('first', ''),
   ('last', ''),
   ('age', (0, lconf_to_int)),
   ('interests', []),
   ('registered', (False, lconf_to_bool)),
   ('salary', (0, lconf_to_int)),
   ('sex', ''),
])


def main():
   lconf_default_obj_pickled = lconf_prepare_default_obj_pickled(example_template)
   result1 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str1, example_template)
   result2 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str2, example_template)
   result3 = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_str3, example_template)

   print('\n=== result1: ', result1)
   print('  result1.extra_data[l_section_name]: ', result1.extra_data['l_section_name'])
   print('  result1.extra_data[l_parsed]: ', result1.extra_data['l_parsed'])
   print('  result1.first: ', type(result1['first']), result1['first'])
   print('  result1.last: ', type(result1['last']), result1['last'])
   print('  result1.age: ', type(result1['age']), result1['age'])
   print('  result1.interests: ', type(result1['interests']), result1['interests'])
   print('  result1.registered: ', type(result1['registered']), result1['registered'])
   print('  result1.salary: ', type(result1['salary']), result1['salary'])
   print('  result1.sex: ', type(result1['sex']), result1['sex'])

   print('\n=== result2: ', result2)
   print('  result2.extra_data[l_section_name]: ', result2.extra_data['l_section_name'])
   print('  result2.extra_data[l_parsed]: ', result2.extra_data['l_parsed'])
   print('  result2.first: ', type(result2['first']), result2['first'])
   print('  result2.last: ', type(result2['last']), result2['last'])
   print('  result2.age: ', type(result2['age']), result2['age'])
   print('  result2.interests: ', type(result2['interests']), result2['interests'])
   print('  result2.registered: ', type(result2['registered']), result2['registered'])
   print('  result2.salary: ', type(result2['salary']), result2['salary'])
   print('  result2.sex: ', type(result2['sex']), result2['sex'])

   print('\n=== result3: ', result3)
   print('  result3.extra_data[l_section_name]: ', result3.extra_data['l_section_name'])
   print('  result3.extra_data[l_parsed]: ', result3.extra_data['l_parsed'])
   print('  result3.first: ', type(result3['first']), result3['first'])
   print('  result3.last: ', type(result3['last']), result3['last'])
   print('  result3.age: ', type(result3['age']), result3['age'])
   print('  result3.interests: ', type(result3['interests']), result3['interests'])
   print('  result3.registered: ', type(result3['registered']), result3['registered'])
   print('  result3.salary: ', type(result3['salary']), result3['salary'])
   print('  result3.sex: ', type(result3['sex']), result3['sex'])


   # ======= OR in a loop ======= #
   print('\n\n ======= OR in a loop ======= \n\n')
   lconf_default_obj_pickled = lconf_prepare_default_obj_pickled(example_template)
   for example_lconf_section_string in [example_lconf_section_str1, example_lconf_section_str2, example_lconf_section_str3]:
      result = lconf_parse_section_pickled(lconf_default_obj_pickled, example_lconf_section_string, example_template)

      print('\n=== result: ', result)
      print('  result.extra_data[l_section_name]: ', result.extra_data['l_section_name'])
      print('  result.extra_data[l_parsed]: ', result.extra_data['l_parsed'])
      # loop through the result in order
      for key, value in result.yield_key_value_order():
         print('  result.{}: '.format(key), type(value), value)

      emit_result = lconf_emit(result1, onelinelists=True)
      print('\n\n===  ===  === emit_result: ===  ===  === \n\n', emit_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
