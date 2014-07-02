.. _README:

*************
LCONF: README
*************

**LCONF: L(ight) CONF(iguration): A simple human-readable data serialization format for dynamic configuration.**

.. contents::
   :depth: 3

HTML Documentation
==================

HTML documentation of the project is hosted at: `LCONF-HTML documentation <http://lconf.readthedocs.org/>`_


System Requirements
===================

:ref:`RequiredSoftware`   (in `docs/source/main_docs`)


Installation
------------

1. python packages might be available from pypi: to be installed with: pip/pip3

   `pip installing packages <http://pip.readthedocs.org/en/latest/user_guide.html#installing-packages>`_

2. or run the standard package installation:

   .. code-block:: sh

      $ python3 setup.py install

3. or use the top-level Makefile: to see all options run:

   .. code-block:: sh

      $ make

4. or add the folder to the python path: see **RandomNotes**   (in `info` folder)


Build the Documentation
-----------------------

MAIN plus API documentation in subfolder: `docs`

**To build: run the top-level Makefile**

.. code-block:: sh

   $ make docs

Resulting `html documentation` will be in:
   /docs/LCONF-DOCUMENTATION/html/index.html


Getting Started
===============

- Generate the documentation or read the .rst files

- Run any tests: in the `source` top-level (root) project folder execute:

   .. code-block:: sh

      $ make tests

- Check out any `Examples folder`, `SpeedCheck folder`, `Tests folder`

.. note:: check required/recommended software: in the `source` top-level (root) project folder execute:

   .. code-block:: sh

      $ make checksoftware


Main Info
=========

Implements the LCONF_Specification-5.0: for more info see the documentation


Main Features
-------------

.. note::

   if one loops through the keys of an LCONF-obj to access the values use the objects RDICT method:

      - yield_key_value_order(): to loop through all keys inclusive any `Default-Comment/Empty Lines`
      - yield_extra_key_value_order(): to loop through all keys exclusive any `Default-Comment/Empty Lines`


- extract one or multiple LCONF-Section from a raw str/file.read()
- Validate all LCONF-Sections in a raw string/file Validates/Checks for:
   - No Trailing Spaces
   - Most Indentation Errors: inclusive indent of Comment lines
   - if a line is a Key/Value separator line:
      - only one space before and one space after the double colon
         - for empty string values no space after the double colon
      - MISSING characters after <::>
      - WRONG CHAR/SPACES after <::>
      - WRONG CHAR/SPACES before <::>

- Command line tool: `lconf-validate`  to validate one or multiple files for all LCONF-sections
   e.g: run in the shell command in the `Example folder`

   this should raise an error on the second file: INDENTATION ERROR: LineNumber: <11>

   .. code-block:: sh

      $ lconf-validate example_to_validate0.lconf example_to_validate1.lconf

   .. note:: this works only if `lconf-validate` is in your path: otherwise specify the full path to `lconf-validate`

- parse one or multiple LCONF-Section from a raw str/file.read()

- supports: easy usage of Transform functions

   - built in `Transform` functions

      -  **lconf_to_bool**

         True, true >>> casted to python: `True`

         False, false >>> casted to python: `False`

      -  **lconf_to_int**

         integer numbers >>> casted to python: `int`

         must contain only digits

      - **lconf_to_float**

         floating point numbers >>> casted to python: `float`

         must contain only digits and exact 1 dot

      - **lconf_to_number**

         any number (int or float) >>> casted to python: `float`

         must contain only digits and maximum 1 dot

      - **lconf_to_pathexpanduser**

         file path strings >>> casted to python: `path.abspath(path.expanduser(path_string))`

         e.g. ~/.test/

      - **lconf_to_datetime**

         date/time string >>> casted to python: `datetime obj`

         must be in the format: 16 character long: `YYYY-MM-DD-hh:mm`

- emit a LCONF-section object with default settings

   - has support for output of `Default-Comment/Empty Lines`: new in LCONF_Specification-5.0

- emit a parsed LCONF-section object:

   - to LCONF text string

      - has support for output of `Default-Comment/Empty Lines`: new in LCONF_Specification-5.0

   - to JSON text string: this requires that only transform function which json format can handle are used

- emit/convert a `python dictionary` (inclusive some subclasses like RDICT) to a LCONF text string

   - supports only minimal nesting: see the function: lconf_dict_to_lconf


Code Examples
=============

for code examples see the files in folder: Examples


Code Usage - How To Implement
=============================

General Implementation Info
---------------------------

LCONF does require a predefined implemented `LCONF-Default-Template-Structure` - one can not >> `just parse` << a 'LCONF text source/file'

**DEFAULT-STRUCTURE-TEMPLATE**

uses two classes from the RDICT package:

- `MAIN (root) obj`: uses the RDICT **RdictFO2 class**
- `Any Key-Value-Mappings`: uses the RDICT **RdictFO2 class**
- `Any `BLOCK-NAME` 'dummy_blk': uses the RDICT **RdictFO2 class**
- `Any `BLOCK-IDENTIFIER`: uses the RDICT **RdictIO class**

.. note:: in the prepared `lconf obj` all **RdictFO2 class** are replaced with **RdictFO class**

   Reason: the prepared `lconf obj` needs to overwrite the values from the `LCONF-Section source/file`


**ITEM FORMAT**

.. code-block:: python

   ('KEY', DEFAULT-VALUE)


**ITEM FORMAT with Transform-Function**

.. code-block:: python

   ('KEY', (DEFAULT-VALUE, TRANSFORM-FUNCTION))


**ITEM FORMAT for Default-Comment Lines**

- key and value must start with an `one number sign` **#**

   - usually the keys are just incremented numbers to make them unique


.. code-block:: python

   ('#KEY', '# Comment')

   ('#1', '# Comment')


**ITEM FORMAT for Default-Empty Lines**


- key must start with an `one number sign` **#**

   - usually the keys are just incremented numbers to make them unique

- value must be an empty string

.. code-block:: python

   ('#KEY', '# Comment')

   ('#1', '')


Example: with explanation comments

.. code-block:: python

   example_template = RdictFO2([
      # key: `first`, DEFAULT-VALUE: `empty string`
      ('first', ''),
      # below is a Default-Empty Line and a Default-Comment Lines: both can be emitted
      ('#1', ''),
      ('#2', '# This is a Comment line which can be emitted'),
      # key: `age`, DEFAULT-VALUE: `0`, TRANSFORM-FUNCTION: `lconf_to_int`
      ('age', (0, lconf_to_int)),
      # key: `interests`, DEFAULT-VALUE: `empty list`
      ('interests', []),
   ])


Example LCONF
-------------

.. seealso:: in the Example folder: files: Example6aReadme.py to Example6eReadme.py

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


LCONF-Section DEFAULT-STRUCTURE-TEMPLATE
----------------------------------------

**write one DEFAULT-STRUCTURE-TEMPLATE:**


.. code-block:: python

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


Common Errors
-------------

- lconf_emit: if not a RDICT obj is passed as argument

   - AttributeError: 'dict' object has no attribute 'extra_data'

- lconf_emit: if not a parsed RDICT obj is passed as argument

   - KeyError: 'l_parsed'
   - or   `LCONF NOT PARSED ERROR`

- using frompickle: needs to load a parsed LCONF obj into: `RdictFO` and not `RdictFO2`


Getting Help
============

No help is provided. You may try to open a new `issue` at github but it is uncertain if anyone will look at it.

|
|

`LCONF` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
