.. image:: _static/LCONFMain350_220.png
   :align: center


.. _LCONF_specification:

.. index:: LCONF; specification

========================
LCONF: Specification 6.0
========================
`LCONF` is a light - human-friendly, simple readable data serialization format for dynamic configuration.


.. rst-class:: emphasize-children

.. index:: Specification; specification

Specification
=============


.. index:: Specification; indentation

Indentation
-----------

**LCONF Indentation** is exact 3 spaces per level


.. index:: Specification; lconf-default-template-structure

.. _lconf_default_template_structure:

LCONF-Default-Template-Structure
--------------------------------

LCONF does require a predefined implemented `LCONF-Default-Template-Structure`.

   REASON:

   LCONF is based on the idea of defaults and order which must be implemented previously - parsing a 'LCONF text source/file'
   will only overwrites such defaults with the user set values

Depending on the library and coding language such `LCONF-Default-Template-Structure` can be implemented in different ways but
must have some common features:

#. should be quite easily to implement
#. must support options for easily defining value transformation: :ref:`Value Transformation <value-transformation>`
#. must support option to define: default comment lines, default empty lines which can be emitted/dumped:
   `Default-Comment/Empty Lines`_
#. must support option to define: order and default values of all LCONF items, keys, values, blocks ect..:
   :ref:`Order <order>`, :ref:`Default Values <default-values>`, `Default-Comment/Empty Lines`_


.. index:: Specification; default-comment/default empty lines

Default-Comment/Empty Lines
---------------------------
The `LCONF-Default-Template-Structure` can define `Default-Comment/Empty Lines` which can be emitted/dumped.

.. warning::

   - before the `Block-Name` (dummy_blk) there may be no `Default-Comment/Empty Lines`

   - within default list items there may be also no `Default-Comment/Empty Lines`

   .. note::
      This does not apply to the 'LCONF text source/file' as such Comments are always skipped when the source text gets
      parsed.


Strings
-------
`LCONF` uses **mainly one native type: strings**. Unlike many other formats: `LCONF` does not use quotation for strings.

Additionally it supports:

- empty string values: for `Key :: Value Pairs` and empty `Key :: Value-Lists` are supported:
   where the value is left out and the last space after the double colon is skipped

   .. warning::   LCONF does not at all support trailing spaces

- optional casting to different data types


.. index:: Specification; comment-line identifier

Comment-Line Identifier
-----------------------
`one number sign` is used as `Comment-Line Identifier`: **"# Comment-Line more info"**

If the first none space character in a line is **#** the line is considered a Comment-Line

Comment-Line must have the indentation level of the following line (disregarding empty lines)
User defined comment lines (LCONF source) are always skipped when the `LCONF source` is parsed.

.. lconf-example:: LCONF with `Comment-Line`

   .. code-block:: lconf

      ___SECTION :: SectionName

      # Comment-Line: must have the indentation level of the following line (disregarding empty lines)
      first :: Tim
      last :: Doe
      age :: 39
      ___END

.. seealso:: related `Default-Comment/Empty Lines`_ which are implemented in the code's `LCONF-Default-Template-Structure`


.. index:: Specification; key :: value separator

.. _key_value_separator:

Key :: Value Separator
----------------------
`one space, double colons, one space` is used as a: `Key Value Separator`: **"Key Name :: Value"**

   **Exception for empty string values:** the last space is skipped so that there is no trailing space.


.. index:: Specification; key :: value pair

Key :: Value Pair
-----------------
Uses the `Key :: Value Separator`_

Each `value` is always interpreted as a: `single string`

   - to transform it use **one** `Value Transformation` function

Empty `Key :: Value Pair`: for empty values the last space of the `Key :: Value Separator`_ is skipped

.. warning:: Empty values with `transformation-function` are returned as empty strings


.. lconf-example::

   LCONF with `Key :: Value Pair`

   .. code-block:: lconf

      ___SECTION :: SectionName
      Color :: Blue
      mykey :: a long sentence ...
      ___END

   LCONF with empty `Key :: Value Pair`

   .. code-block:: lconf

      ___SECTION :: SectionName
      MyEmptyKeyValuePair ::
      ___END



.. index:: Specification; lists


Lists
-----
There are 3 sub types of lists and all of them use the `List Identifier`_ and support empty lists.

For an empty list only define the `List Identifier line` without any items / item lines.

- This will overwrite any default values

- To keep all default values do not define the `List` at all


.. index:: Specification; list identifier

.. _list_identifier:

List Identifier
~~~~~~~~~~~~~~~
`minus, one space` is used as `List Identifier` for all `3 sub types of lists`: **"- List Identifier Name"**


.. lconf-example:: LCONF with `List Identifiers` for all 3 sub types of lists

   .. code-block:: lconf

      ___SECTION :: SectionName

      # Key :: Value-List: one line
      - Names :: Tim,Sandra,Max

      # Key-Value-List: multi line with indentation
      - Names
         Tim
         Sandra
         Max

      # List-Of-Tuples: multi line with indentation
      - Colors RGB |Color Name|Red|Green|Blue|
         forestgreen,34,139,34
         brick,156,102,31
      ___END


.. index:: Specification; key :: value-list

Key :: Value-List
~~~~~~~~~~~~~~~~~
Ordered collection of items: oneline list

Uses the `List Identifier`_ and  also the `Key :: Value Separator`_ and as value a collection of ordered items separated by
`comma` **,**

.. important:: spaces are not stripped

Each `list item` is always interpreted as a: `single string` within a list obj.

- This implies that list items can not be an other list or dict.

- to transform it use **one** `Value Transformation` function which is applied to each item in the list


.. lconf-example::

   LCONF `Key :: Value-List`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - Names :: Tim,Sandra,Max
      ___END

   LCONF empty `Key :: Value-List`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - MyEmptyList ::
      ___END


.. index:: Specification; key-value-list

Key-Value-List
~~~~~~~~~~~~~~
Ordered collection of items: multiline list

Uses the `List Identifier`_ and the value lines (list items) uses one indentation level (3 additional spaces).

Basically the same as `Key :: Value-List`_ just uses a different notation for readability and is mostly useful for longer
lists (or when the items are long e.g. sentences).

Each `list item` line is always interpreted as a: `single string` within a list obj.

   - This implies that list items can not be an other list or dict.

   - to transform it use **one** `Value Transformation` function


.. lconf-example::

   LCONF `Key-Value-List`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - Names
         Tim
         Sandra
         Max
         Frank
      ___END

   LCONF empty `Key-Value-List`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - Names
      ___END


.. warning::  `Key-Value-List Identifier` lines may NOT end with an `pipe sign (vertical bar)` **|**

   WRONG LCONF `Key-Value-List`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - My List |
         VALUE list item1
         VALUE list item2
      ___END


.. tip::

      LCONF `Key-Value-List` can have comma separated lines

      .. code-block:: lconf

         ___SECTION :: SectionName
         - list_
            534,45
            0,1,2,3
         ___END

   - This is neither a multidimensional `List-Of-Tuples` because there was no last char: `pipe sign` **|**

   The list item: *534,45* or *0,1,2,3* are a normal string lines (item lines of an: `Key-Value-List`)
   e.g. one could use a transformation function to simulate a kind of list within a list with different number of
   values (in case `List-Of-Tuples` can not fit the purpose)

      - splitting it be comma


.. index:: Specification; list-of-tuples

List-Of-Tuples
~~~~~~~~~~~~~~
Ordered collection of items: multi-line list of multiple values

Uses the `List Identifier`_ and additionally adds at the end a `space` followed by column names

The Value lines (tuple item rows) use **one** additional indentation level (3 additional spaces).

- all item lines must have the same number of values (as defined in the column names)

`List-Of-Tuples` are useful for multidimensional lists or tables e.g. csv data.


- Column Names are embraced and separated by `pipe sign (vertical bar)` and must be unique
- `List-Of-Tuples` item lines: Values are separated by `comma` **,**

   .. important:: spaces around values are stripped


.. lconf-example::

   LCONF `List-Of-Tuples` with 3 expected items (columns) per line (row)

   .. code-block:: lconf

      ___SECTION :: SectionName
      - My List of lists |X|Y|Z|
         value1, value2, value3
         value1, value2, value3
      ___END

   LCONF empty `List-Of-Tuples`

   .. code-block:: lconf

      ___SECTION :: SectionName
      - My empty List of lists |X|Y|Z|
      ___END


List-Of-Tuples can have empty (missing) values: `Empty/Missing Values` are returned as empty strings or if defined per column
replacement values. `Replacement-Values` must be implemented in the `LCONF-Default-Template-Structure`_.

   .. important:: Defined `Empty/Missing Replacement-Values` must be defined as **strings** as they run also through any
      transformation functions

.. lconf-example::

   LCONF `List-Of-Tuples` with `Empty/Missing Values` which will be returned as empty strings or with a `Replacement-Values`
   if implemented in the `LCONF-Default-Template-Structure`_

   .. code-block:: lconf

      ___SECTION :: SectionName
      - My List of lists |X|Y|Z|
         # COMMENT: the 2. item is empty or missing
         value1,       , value3
         value1, value2, value3
         # COMMENT: all items are empty or missing: the indentation level must be kept
         ,             ,
         # COMMENT: spaces are not important
         ,,
      ___END


Each single `item value` is always interpreted as a: `single string` within a tuple obj.

   - This implies that items in any of the tuples (rows) can not be an other list or dict.


   - have **one** `transformation function` which will be applied to each single item in each tuple

   - or have **for each `column` a separate** `transformation function` which will be applied to each line (row)

      in the example above this would be 3 `transformation functions`: X,Y,Z Columns

.. warning::

   - Empty values with `transformation-function` are returned as empty strings

   - Any `Replacement-Value` runs also through the transformation-function like any normally set value and is returned


.. index:: Specification; key-value-mapping

.. _key_value_mapping_identifier:

Key-Value-Mapping
-----------------
`dot, one space`  is used as `Key-Value-Mapping Identifier`: **". Key-Value-Mapping Identifier Name"**

A collection of items depending on the implementation this can be ordered or unordered

.. note:: any LCONF library must implement an option to loop over it in order as defined in a
   `LCONF-Template-Default-Structure`

Mapping items use **one** additional indentation level (3 additional spaces).
   Each `mapping item` can be any of can be any of the :ref:`Four Main Structures <Four_Main_Structures>`

An Empty `Key-Value-Mapping Identifier` is permitted: which will use all default values as implemented by a
`LCONF-Template-Default-Structure`. It is basically the same as if one does not define it at all.

   - use it as a placeholder: e.g. if one wants previous comment lines


.. lconf-example::

   LCONF `Key-Value-Mapping`

   .. code-block:: lconf

      ___SECTION :: SectionName
      . Mapping KEY
         mapping_item1_key :: mapping_item1_value
         - mapping_item2_key list
            my list item 1
         . mapping_item3_key nested key-value-mapping
            inner_mapping_item1_key :: inner_mapping_item1_value

         * mapping_item1_key Nested_BLK_Identifier
            Tim_Blk_Name
      ___END


   LCONF empty `Key-Value-Mapping`

   .. code-block:: lconf

      ___SECTION :: SectionName
      . Mapping KEY
         mapping_item1_key :: mapping_item1_value
         - mapping_item2_key list
            my list item 1
         # Comment: below a permitted empty `Key-Value-Mapping Identifier` which will use all default values
         . mapping_item3_key nested key-value-mapping

         * mapping_item1_key Nested_BLK_Identifier
            Tim_Blk_Name
      ___END

`Key-Value-Mapping` lines can not have any `transformation function`

   - but each item can (depending on the item)


.. important::  Do get all default values for each item key

      do not define the `Key-Value-Mapping` in the LCONF

      OR define only the `Key-Value-Mapping Identifier line` in the LCONF which is permitted too


.. index:: Specification; repeated-block

Repeated-Block
--------------
Repeated Blocks allows to configure any number of such blocks within the ‘LCONF text source/file’.

`Repeated-Block-Identifier` and `Block-Name` lines can not have any `transformation function`

   - but each block item of a `Block-Name` can (depending on the item)

Any number of Block-Names can be defined: this can also be limited in a `LCONF-Template-Default-Structure`

`Repeated Blocks` have two options to predefine: 

   - NUMBER_MIN_REQUIRED_BLOCKS in a `LCONF-Template-Default-Structure`
   
      - 0 or greater
      
      - to not define it: set it to -1
      
   - NUMBER_MAX_ALLOWED_BLOCKS in a `LCONF-Template-Default-Structure`
      
      - 1 or greater
      
      - to not define it: set it to -1 

Block item can be any of the :ref:`Four Main Structures <Four_Main_Structures>`.


.. _repeated_block_identifier:

Repeated-Block-Identifier
~~~~~~~~~~~~~~~~~~~~~~~~~
`asterisk, one space` is used as `Repeated-Block-Identifier`: **"* Repeated-Block-Identifier Name"**

An Empty `Repeated Block Identifier` is permitted: but without a `Block-Name` it does nothing

   - use it as a placeholder: e.g. if one wants previous comment lines

`Repeated-Block-Identifier` lines can not have any `transformation function`


.. lconf-example::

   LCONF `Repeated-Block`

   .. code-block:: lconf

      ___SECTION :: SectionName
      * Color_BLK_Identifier
         Sky Blue_Blk-Name
            blk_item_red :: 135
            blk_item_green :: 206
            blk_item_blue :: 235
      ___END

   LCONF empty `Repeated-Block`  only define the `Repeated Block Identifier` line:  it does nothing

   .. code-block:: lconf

      ___SECTION :: SectionName
      * Color_BLK_Identifier
      ___END


Block-Names
~~~~~~~~~~~
Each Block is named: `Block-Names` use **one** additional indentation level (3 additional spaces) from the
`Repeated-Block-Identifier`.

Any number of Block-Names can be defined: this can also be limited in a `LCONF-Template-Default-Structure`.

- `Repeated Blocks` have two options to predefine: NUMBER_MIN_REQUIRED_BLOCKS, NUMBER_MAX_ALLOWED_BLOCKS

.. todo:: change NUMBER_MAX_ALLOWED_BLOCKS to NUMBER_MAX_ALLOWED_BLOCKS

.. note:: if a `Block-Name` is defined without any items at all: it is still valid using all defaults

   LCONF `Repeated-Block` with an empty `Block-Name` which will using all defaults implemented in a
   `LCONF-Template-Default-Structure`

   .. code-block:: lconf

      ___SECTION :: SectionName
      * Color_BLK_Identifier
         Sky Blue_Blk-Name
      ___END


Block-Name Items
~~~~~~~~~~~~~~~~
`Block-Name Items` use **one** additional indentation level (3 additional spaces) from the `Block-Name`.

Each `Block-Name Item` can be any of the :ref:`Four Main Structures <Four_Main_Structures>`.


`Block-Name Items` lines can have `transformation function/s` (depending on the item type)


.. index:: Specification; section start/end tags

Section Start/End Tags
----------------------
`___SECTION`, `___END` are reserved for the purpose of `SECTION START/END TAGS`.

.. lconf-example:: LCONF `Section Start/End TAGS-Block` LCONF-Section called: MyExample

   .. code-block:: lconf

      ___SECTION :: MyExample
      ___END


.. warning:: Section Start/End TAGS are forbidden in any form except for the defined purpose.

Section Start TAG
~~~~~~~~~~~~~~~~~
`three underlines, capital SECTION`

This is followed by a `Key :: Value Separator`_ and the Section Name which is required: it can not be an empty string value.

It must always be without indentation.

Section End TAG
~~~~~~~~~~~~~~~
`three underlines, capital END`

It must always be without indentation.


.. index:: Specification; restrictions, Restrictions; restrictions, LCONF; restrictions

Restrictions
------------

**A library does not have to validate these restrictions: validation is optional.**

Restrictions Summary
~~~~~~~~~~~~~~~~~~~~

- GENERAL RESERVED: `___SECTION`, `___END`, `::`

- FIRST NONE WHITE character of a line RESERVED:

   - `* asterisk` Except for `Repeated-Block-Identifier`

   - `- minus` Except for all kind of `Lists-Identifier`

   - `. dot` Except for all kind of `Key-Value-Mapping`

   - `# number sign` Except for Comment lines

- LAST character of a line RESERVED:

   -  `Key-Value-List Identifier` lines may NOT end with an `pipe sign (vertical bar)` **|**

   - `List-Of-Tuples Identifier` lines: must end with a `pipe sign (vertical bar)` **|**

      `List-Of-Tuples Identifier` can not contain any `pipe sign (vertical bar)` except for the purpose of separating
      `column names`


- Item types in lists:

   - `Key-Value-List` and `Key :: Value-List`: may be only basic types: not another list, tuple, dict ect..

      .. tip::

            LCONF `Key-Value-List` can have comma separated lines

            .. code-block:: lconf

               ___SECTION :: SectionName
               - list_
                  534,45
                  0,1,2,3
               ___END

         - This is neither a multidimensional `List-Of-Tuples` because there was no last char: `pipe sign` **|**

         The list item: *534,45* or *0,1,2,3* are a normal string lines (item lines of an: `Key-Value-List`)
         e.g. one could use a transformation function to simulate a kind of list within a list with different number of
         values (in case `List-Of-Tuples` can not fit the purpose)

            - splitting it be comma

   - `List-Of-Tuples`: can contain tuples with the same number of items as column-names specified. (empty items are allowed)

      - items within the tuples: may be only basic types: not another list, tuple, dict ect..


.. index:: Restrictions; section start/end tag

Restrictions: Section Start/End Tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Section Start/End Tag are forbidden in any form except for the defined purpose. `Section Start/End Tags`_


.. index:: Restrictions; unique names

.. _restrictions_unique_names:

Restrictions: Unique names
~~~~~~~~~~~~~~~~~~~~~~~~~~

- all `Main Keys` and `Repeated-Block-Identifiers`: must be unique

- `withing a `Key-Value-Mapping`: the keys must be unique

- `within a `List-Of-Tuples`: the column names must be unique

- `Block-Names`: must be unique within one `Repeated-Block-Identifier`

- `Block-Keys`: must be unique within one `Block`


.. index:: Restrictions; item types in lists

.. _restrictions_item_types_in_lists:

Restrictions: Item Types in Lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Key-Value-List` and `Key :: Value-List`: may be only basic types: not another list, tuple, dict ect..

   .. note::

      LCONF `Key-Value-List` can have comma separated lines

      .. code-block:: lconf

         - list_
            0,1,2,3

      - This is neither a multidimensional `List-Of-Tuples` because there was no last char: `pipe sign` **|**
      - It is also not a oneline `Key :: Value-List`

      The list item: *0,1,2,3* is a normal string line (item line of an: `Key-Value-List`)
      e.g. one could use a transformation function to simulate a kind of list within a list.

         - splitting it be comma


      **WRONG** LCONF `Key-Value-List` can have as items only basic types

         .. code-block:: lconf

            - mylist
               item1
               # wrong to have a nested list within a list
               - another_list ::


- `List-Of-Tuples`: may only contain tuples (row lines) with the same number of items as column-names specified.

   - items within the tuples: may be only basic types: not another list, tuple, dict ect.. (empty items are supported)


.. index:: Restrictions; restrictions (No Trailing Spaces)

Restrictions: No Trailing Spaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Lines may not have any trailing spaces


.. index:: Restrictions; comments

Restrictions: Comments
~~~~~~~~~~~~~~~~~~~~~~
Comment lines **#** within a `LCONF-Section` are required to have the indentation of the next none empty line.


.. index:: Restrictions; default-comment/empty lines

Restrictions: Default-Comment/Empty Lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- before `Block-Names` (dummy_blk) there may be no `Default-Comment/Empty Lines`_ within the code of the
   `LCONF-Default-Template-Structure`_.

- within `Lists` (between default list items) there may be no `Default-Comment/Empty Lines`_ within the code of the
   `LCONF-Default-Template-Structure`_.


|
|

`LCONF` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
