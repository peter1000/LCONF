.. image:: _static/LCONFMain350_220.png
   :align: center


.. _LCONF_specification:

.. index:: LCONF; specification abstract (overview)

=============================
LCONF: Specification Abstract
=============================

`LCONF` is a light - human-friendly, simple readable data serialization format for dynamic configuration.

- in many situations `LCONF` is a suitable replacement for `YAML <http://www.yaml.org/>`_
- `LCONF` can be used to replace `JSON <http://json.org/>`_ in many cases

.. note:: LCONF_Specification-7.0

   `LCONF Specification 7.0` should be backwards compatible with version 6.0

   - adds support for setting: optional `Empty-KeyValuePair-ReplacementValues` in the

      :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>`

      - for instance: a integer value is expected but one wants for empty `LCONF Key :: Value Pairs` to return -1 or whatever


Designed around
===============

- READABILITY
- NAMED SECTIONS
- FOUR MAIN STRUCTURES
- VALUE TRANSFORMATION
- ORDER
- DEFAULT VALUES
- PRETTY EMITTING/DUMPING

   - inclusive Default Comments


Readability
===========

- Sections
- Lines
- Indentation
- Strings
- # Comments
- # Default-Comment/Empty Lines
- Only a few special Identifier Tags


Named Sections
==============
Named Sections allow for extended text/info/explanations before or after a `Section` without the need of **#** Comment tags.

Multiple LCONF-Sections can be within one *LCONF text source or file*


.. index:: Specification; four main structures

.. _Four_Main_Structures:

Four Main Structures
====================

Key :: Value Pairs
------------------

   .. code-block:: text

      my name key :: assigned value

Lists
-----
There are 3 sub types of lists:

*Key :: Value-Lists*: oneline lists

   .. code-block:: text

      - name list :: Tim,Joe,Peter

*Key-Value-Lists*: multiline lists: values with indentation: basically just an different way to write/read it

   .. code-block:: text

      - name list
         Tim
         Joe
         Peter

*List-Of-Tuples*: multiline list of tuples: values with indentation

   - each tuple must have at least 2 values
   - all tuples must have the same number of items as columns defined

   .. code-block:: text

      - list of RGB colors |Color Name|Red|Green|Blue|
         forestgreen,   34,   139,  34
         brick,         156,  102,  31

Key-Value-Mappings
------------------
Items with indentation: each item can be any of the `Four Main Structures`_

.. code-block:: text

   . my mapping key
      key :: value
      - name list :: Tim,Joe,Peter

Repeated Blocks
---------------
Block item can be any of the `Four Main Structures`_

*Repeated Blocks* allows to configure any number of such blocks within the 'LCONF text source/file'.


.. index:: Specification; value transformation

.. _value-transformation:

Value Transformation
====================
LCONF implements the idea of easy item value transformation.
Any Item-Value must be easily transformable using customary hook functions or some other ways to achieve such: depending
on the library language. Such are implemented in the `LCONF-Default-Template-Structure`.

Value Transformation is mostly used for type transformation (type casting) because:
   `basic LCONF is on purpose only text/string based`

- of course such `transformation` function could do also any other complex transformation

Within the `LCONF-Default-Template-Structure` transformation functions can only be applied to:
   `Key :: Value Pairs`: each one can have a separate `transformation function`

      .. important:: Empty values with `transformation-function` are returned as empty strings

      .. seealso:: EXCEPTION: **Empty-KeyValuePair-ReplacementValues**

         :ref:`Empty Key :: Value Pairs`<empty_key_value_pairs>`

   `Key :: Value-Lists` and `Key-Value-Lists`: can have only one `transformation function` which will be applied to each item
   in the list

   `List-Of-Tuples`:

      - can have one `transformation function` which will be applied to each item in each tuple of the list

      - or can have for each value (column) a separate `transformation function` which will be applied to each line (row)

      .. warning:: Empty values with `transformation-function` are returned as empty strings


.. _order:

Order
=====
LCONF is ordered

.. important::

   Any order will always be based on the `LCONF-Default-Template-Structure` and not on the `LCONF text source/file`

   EXCEPTIONS:

      - the order of `Block-Names` of (Repeated-Block-Identifiers):
         will be always as in the 'LCONF text source/file' (as they are not previously known)

      - the order of `Lists items`:
         will be always as in the 'LCONF text source/file' (as they are not previously known)


.. index:: Specification; default values, Specification; lconf-default-template-structure

.. _default-values:

Default Values
==============
LCONF is based on the idea of a: predefined `LCONF-Default-Template-Structure`.

- This gives it order, default values and one knows what to expect.

- helps to emit/dump in proper order based on the structure

   - inclusive any `Default-Comment/Empty Lines`
   - Any LCONF library **must** implement an option to emit/dump any `Repeated Block`
     with an optional 'dummy-blk' with default values.

- the only thing which is not pre-known are:

   - the user set values
   - the number of items in lists
   - the number of Block-Names in `Repeated Blocks`

      but `Repeated Blocks` have an option to predefine: NUMBER_MIN_REQUIRED_BLOCKS, NUMBER_MAX_ALLOWED_BLOCKS

- Because all structures must be previously implemented within the code (`LCONF-Template-Default-Structure`)
   any library which implements the `LCONF: human-friendly, simple readable data serialization format` should give some
   thoughts as how do write such `LCONF-Template-Default-Structure` in a simple form

- parsing a LCONF-Section (string/file) will just overwrite any default values
   So the simplest LCONF is only a START/END TAG:
      which will be parsed to all implemented defaults as nothing gets overwritten
      There won't be any Repeated Blocks because there are no default Block-Names set.

   .. lconf-example::

      .. code-block:: lconf

         ___SECTION :: DefaultLCONF
         ___END


.. note:: To get `Default-Values` do not define the item in the 'LCONF text source/file'

   - **EXCEPTIONS:**

      - for `Repeated Blocks`: to get the `Default-Values` for a whole Block: only define the Block-Identifier and the
        Block-Name without any items


Pretty Emitting/Dumping
=======================
LCONF actively supports `pretty` printing (emitting/dumping).

- By design there is a strict predefined outline of indentation, structure ect..
- For list items there are 2 option implemented:

   - oneline lists: empty lists or usually used for lists with few items
   - multiline lists with item indentation: usually used for lists with more items

      - List-Of-Tuples: are always multiline lists

- # `Default-Comment/Empty Lines`

   - unlike many other formats LCONF design has full support for emitting/dumping of `Default-Comment/Empty Lines`

      * such must be implemented in the `LCONF-Template-Default-Structure`

   .. warning:: LCONF does not support parsing **#** Comment lines from the 'LCONF text source/file'

      - Such are skipped by design


.. index:: Specification; relation to json - yaml

Relation To Json - Yaml
=======================

.. important:: REPLACEMENT

   - in many situations **LCONF** is a suitable replacement for `YAML <http://www.yaml.org/>`_
   - **LCONF** can be used to replace `JSON <http://json.org/>`_ in many cases


Any base LCONF (string representation) without transformation can be dumped as a valid json obj (array) which is also a valid
yaml.

BUT not every json array/object or yaml might be represented as a valid `LCONF-Section`

- e.g. LCONF does not support list to have nested dictionary items or other lists

.. note::

   - LCONF does require a predefined implemented `LCONF-Default-Template-Structure`

      - one can not >> `just parse` << a 'LCONF text source/file'

   - LCONF has some additional features e.g.:

      - there is an option to loop over all keys in order as implemented by the: `LCONF-Default-Template-Structure`

      - support for output of `Default-Comment/Empty Lines`

   - LCONF supports customary transform functions: json/yaml may not be able to handle the `type` of such transformation

      - but the base LCONF (string representation) should be ok
