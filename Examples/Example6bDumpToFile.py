""" Example implementation: of the documentation: docs/source/main_docs/README.rst: 'Code Usage - How To Implement'
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
   RdictIO,
   RdictFO2
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


example_lconf_section_str = r'''___SECTION :: INFO
# Comment-Line: below: Main `Key :: Value Pair`
registered_employees :: 28594
# Comment-Line: below: `Repeated Mapping-Block Identifier`
* Employee
   # Comment-Line: below: `Block-Name`
   Person1
      # Comment-Line: below: Block-Item `Key :: Value Pair`
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      # Comment-Line: below: Block-Item `Key-Value-Mapping`
      past_salary
         # Comment-Line: Block  Key-Value-Mapping items: are `Key :: Value Pairs`
         year2012 :: 45000
         year2013 :: 62000
      # Comment-Line: below: Block-Item `Key-Value-List`
      emails
         <xaver@dot.com>
         <xaver23@yahoo.com>
# Comment-Line: below: Main `Key :: Value Pair`
registered_customer :: 28594
# Comment-Line: below: `Repeated List-Block Identifier`
* CompanyProfit
   # Comment-Line: below: Block-Name
   Year2012
      # Comment-Line: Repeated Block Items:
      GrossSales :: 38459845
      NetSales :: 15835945
      GrossProfit :: 3000945
   # Comment-Line: below: Block-Name
   Year2013
      # Comment-Line: Repeated Block Items:
      GrossSales :: 41459256
      NetSales :: 18635001
      GrossProfit :: 2900725
___END
'''

example_template = RdictFO2([
   ('#1', '# Comment-Line: below: Main `Key :: Value Pair`'),
   ('registered_employees', (0, lconf_to_int)),
   ('#2', ''),
   ('#2a', '# Comment-Line: below: `Repeated Mapping-Block Identifier`: type RdictIO'),
   ('Employee', RdictIO([
      ('#3', '# Comment-Line: Repeated Block-Name: default dummy: must be named: dummy_blk: type: RdictFO2'),
      ('dummy_blk', RdictFO2([
         ('#4', '# Comment-Line: below: Block-Item `Key :: Value Pair'),
         ('first', ''),
         ('last', ''),
         ('sex', ''),
         ('age', (0, lconf_to_int)),
         ('#5', '# Comment-Line: below: Block-Item `Key-Value-Mapping` type: RdictFO2'),
         ('past_salary', RdictFO2([
            ('#6', '# Comment-Line: Block  Key-Value-Mapping items: are `Key :: Value Pairs`'),
            ('year2012', (0, lconf_to_int)),
            ('year2013', (0, lconf_to_int)),
         ])),
         ('#7', '# Comment-Line: below: Block-Item `Key-Value-List`'),
         ('emails', []),
      ])),
   ])),
   ('#8', '# Comment-Line: below: Main `Key :: Value Pair`'),
   ('registered_customer', (0, lconf_to_int)),
   ('#9', ''),
   ('#9a', '# Comment-Line: below: `Repeated Mapping-Block Identifier`: type RdictIO'),
   ('CompanyProfit', RdictIO([
      ('#10', '# Comment-Line: Repeated Block-Name: default dummy: must be named: dummy_blk: type: RdictFO2'),
      ('dummy_blk', RdictFO2([
         ('#11', '# Comment-Line: Repeated Block Items'),
         ('GrossSales', (0, lconf_to_int)),
         ('NetSales', (0, lconf_to_int)),
         ('GrossProfit', (0, lconf_to_int)),
      ])),
   ])),
])


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   # Prepare: a default lconf obj from the template obj and parse the LCONF-Section string
   lconf__obj = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   #print('\n=== lconf__obj: ', lconf__obj)

   # EMIT PARSED  and dump it to file
   with open('example6b_dumptofile_readme.lconf', 'w') as file_:
      file_.write('\n\n======== WITH `Default-Comment/Empty Lines` ========\n\n')
      result_emit = lconf_emit(lconf__obj, onelinelists=True, with_comments=True)
      file_.write(result_emit)

      file_.write('\n\n======== WITHOUT `Default-Comment/Empty Lines` ========\n\n')
      result_emit = lconf_emit(lconf__obj, onelinelists=True, with_comments=False)
      file_.write(result_emit)
      
      
   print('\n\n======== Finished dumping to file: file content: ========\n\n')

   with open('example6b_dumptofile_readme.lconf', 'r') as file_:
      print(file_.read())


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
