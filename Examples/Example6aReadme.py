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
from pickle import (
   dumps as pdumps,
   loads as ploads
)
from sys import path as syspath

from RDICT.MainCode import (
   RdictFO,
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
   lconf_emit_default_obj,
   lconf_prepare_and_parse_section,
   lconf_validate_source
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
   # EMIT DEFAULT
   result_emit_default_obj = lconf_emit_default_obj(example_template, 'Example Default', onelinelists=True, emit_dummy_blks=True)
   print('\n=== result_emit_default_obj: ', result_emit_default_obj)


   # Optional: Validate the LCONF-Section string
   lconf_validate_source(example_lconf_section_str)


   # Prepare: a default lconf obj from the template obj and parse the LCONF-Section string
   lconf__obj = lconf_prepare_and_parse_section(example_lconf_section_str, example_template, validate=True)
   #print('\n=== lconf__obj: ', lconf__obj)


   # See if this LCONF obj was parsed or only created with default settings
   print('\n  lconf__obj.extra_data[l_parsed]: ', lconf__obj.extra_data['l_parsed'])
   # Accessing:  The Section-Name
   print('\n  lconf__obj.extra_data[l_section_name]: ', lconf__obj.extra_data['l_section_name'])
   # Accessing:  The Section-key_order
   print('\n=== lconf__obj.key_order: ', lconf__obj.key_order)


   # Try to pickle it
   pdump_result = pdumps(lconf__obj, protocol=4)
   print('\n pdump_result: ', pdump_result)
   ploads_result = ploads(pdump_result)
   print('\n ploads_result: ', ploads_result)


   # Try topickle/ frompickle
   topickle_result = lconf__obj.topickle()
   print('\n topickle_result: ', topickle_result)
   ploads_result = RdictFO.frompickle(topickle_result)
   print('\n ploads_result: ', ploads_result)


   # ACCESS/PRINT:parsed lconf obj
   print('\n\n ==== access/print parsed lconf obj ==== \n\n')
   print('  lconf__obj.registered_employees: type: <{}>  val: <{}>'.format(type(lconf__obj['registered_employees']), lconf__obj['registered_employees']))
   # Mapping-Block Identifier
   print('  lconf__obj.Employee: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']), lconf__obj['Employee']))
   # if the Mapping-Block: Name is known one can access the items like
   print('  lconf__obj.Employee.Person1: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']), lconf__obj['Employee']['Person1']))

   # Mapping-Block-Item:
   print('     lconf__obj.Employee.Person1.first: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['first']), lconf__obj['Employee']['Person1']['first']))
   print('     lconf__obj.Employee.Person1.last: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['last']), lconf__obj['Employee']['Person1']['last']))
   print('     lconf__obj.Employee.Person1.sex: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['sex']), lconf__obj['Employee']['Person1']['sex']))
   print('     lconf__obj.Employee.Person1.age: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['age']), lconf__obj['Employee']['Person1']['age']))
   # Mapping-Block-Item: Key-Value-Mapping
   print('     lconf__obj.Employee.Person1.past_salary: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['past_salary']), lconf__obj['Employee']['Person1']['past_salary']))
   print('     lconf__obj.Employee.Person1.past_salary.year2012: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['past_salary']['year2012']), lconf__obj['Employee']['Person1']['past_salary']['year2012']))
   print('     lconf__obj.Employee.Person1.past_salary.year2013: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['past_salary']['year2013']), lconf__obj['Employee']['Person1']['past_salary']['year2013']))

   # Mapping-Block-Item: Key-Value-Lists
   print('     lconf__obj.Employee.Person1.emails: type: <{}>  val: <{}>'.format(type(lconf__obj['Employee']['Person1']['emails']), lconf__obj['Employee']['Person1']['emails']))
   #
   print('     lconf__obj.registered_customer: type: <{}>  val: <{}>'.format(type(lconf__obj['registered_customer']), lconf__obj['registered_customer']))
   # Mapping-Block Identifier
   print('  lconf__obj.CompanyProfit: type: <{}>  val: <{}>'.format(type(lconf__obj['CompanyProfit']), lconf__obj['CompanyProfit']))
   # if the Mapping-Block: Name is known one can access the items like
   print('  lconf__obj.CompanyProfit.Year2012: type: <{}>  val: <{}>'.format(type(lconf__obj['CompanyProfit']['Year2012']), lconf__obj['CompanyProfit']['Year2012']))

   # Mapping-Block-Item: loop through the items
   for blk_name, blk_obj in lconf__obj['CompanyProfit'].yield_key_value_order():
      print('     lconf__obj.CompanyProfit.blk_name: type: <{}>  val: <{}>'.format(type(blk_name), blk_name))

      # Block-Item:
      print('        blk_obj.GrossSales: type: <{}>  val: <{}>'.format(type(blk_obj['GrossSales']), blk_obj['GrossSales']))
      print('        blk_obj.NetSales: type: <{}>  val: <{}>'.format(type(blk_obj['NetSales']), blk_obj['NetSales']))
      print('        blk_obj.GrossProfit: type: <{}>  val: <{}>'.format(type(blk_obj['GrossProfit']), blk_obj['GrossProfit']))


   # EMIT PARSED
   result_emit = lconf_emit(lconf__obj, onelinelists=True, with_comments=True)
   print('\n\n=== result_emit: ', result_emit)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
