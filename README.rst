.. _LongDescription:

******************
LCONF: Description
******************

.. rubric:: LCONF:
.. rubric:: L(ight) CONF(iguration): A simple human-readable data serialization format for dynamic configuration.

.. contents::
   :depth: 3


HTML Documentation
==================

HTML documentation of the project is hosted at: `LCONF-HTML documentation <http://lconf.readthedocs.org/>`_

Or `Package Documentation <http://pythonhosted.org//LCONF/>`_


Main Info
=========

Implements the LCONF_Specification-5.0: for more info see the documentation


Relation To Json - Yaml
-----------------------

Any base LCONF (string representation) without transformation can be dumped as a valid json obj (array) which is also a valid yaml

BUT not every json array/object or yaml can be represented as a valid `LCONF-Section`

.. note::

   - LCONF does not support deep nesting - but only predefined nesting and has some additional features e.g.:

      - there is an option to loop over all keys in order as implemented by the: `LCONF-Default-Template-Structure`

      - support for output of `Default-Comment/Empty Lines`

   - LCONF does require a predefined implemented `LCONF-Default-Template-Structure` - one can not >> `just parse` << a 'LCONF text source/file'

   - LCONF supports customary transform functions per item: json may not be able to keep the `type` and will represent it as an `string type`

      - but the base LCONF (string representation) will be ok


Example LCONF
=============

see also: in the Example folder: files: Example6aReadme.py to Example6eReadme.py

.. code-block:: python

   ___SECTION :: INFO
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


Projects using LCONF
====================

Known `projects` which make use of: **LCONF**


`DOCK <https://github.com/peter1000/DOCK>`_  (A `docker` linux desktop with permission configuration.)

`HealthNutritionPlanner <https://github.com/peter1000/HealthNutritionPlanner>`_  (Plan: weight loss, healthy diets, meals.)

|
|

`LCONF` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
