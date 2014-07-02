""" Example implementation: of the documentation: docs/source/main_docs/LCONF_Specification-4.1.rst: 'EXAMPLE 4 (JSON - LCONF)'
                                                                                                      using the: LCONF Repeated Mapping-Block
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
   lconf_prepare_and_parse_section
)
from LCONF.Transform import lconf_to_int


example_lconf_section_str = r'''___SECTION :: SKILLS
# Repeated Mapping-Block
* categories
   PHP
      test1_name :: One
      test1_score :: 90
      tests2_name :: Two
      tests2_score :: 96
   Node.js
      test1_name :: One
      test1_score :: 97
      tests2_name :: Two
      tests2_score :: 93
___END
'''


example_template = RdictFO2([
   # Repeated Mapping-Block: type: RdictIO
   ('categories', RdictIO([
      # Comment-Line: Repeated Block-Name: default dummy: must be named: dummy_blk: type: RdictFO2
      ('dummy_blk', RdictFO2([
         ('test1_name', ''),
         ('test1_score', (0, lconf_to_int)),
         ('tests2_name', ''),
         ('tests2_score', (0, lconf_to_int)),
      ])),
   ])),
])


def main():
   # Prepare: a default lconf obj from the template obj and parse the LCONF-Section string
   result1 = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   #print('\n=== result1: ', result1)

   # Accessing:  The Section-INFO
   print('  result1.extra_data[l_section_name]: ', result1.extra_data['l_section_name'])
   print('  result1.extra_data[l_parsed]: ', result1.extra_data['l_parsed'])
   # Mapping-Block Identifier
   print('  result1.categories: ', type(result1['categories']), result1['categories'])

   # if the Mapping-Block: Name is known one can access the items directly
   print('  result1.categories.PHP.test1_name: ', type(result1['categories']['PHP']['test1_name']), result1['categories']['PHP']['test1_name'])
   # looping through the Block-Names:
   for blk_name, blk_obj in result1['categories'].yield_key_value_order():
      # Block-Name:
      print('     blk_name: ', type(blk_name), blk_name)

      # Mapping-Block-Item:
      print('        blk_obj: ', type(blk_obj), blk_obj)
      # looping through the Mapping-Block-Items:
      for item_key, item_value in blk_obj.yield_key_value_order():
         print('     this_key.{}: '.format(item_key), type(item_value), item_value)

   emit_result = lconf_emit(result1, onelinelists=True)
   print('\n\n===  ===  === emit_result: ===  ===  === \n\n', emit_result)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
