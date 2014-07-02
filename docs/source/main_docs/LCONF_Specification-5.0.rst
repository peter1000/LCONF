.. _LCONF_specification:

********************************************
LCONF: L(ight) CONF(iguration) Specification
********************************************

**LCONF: L(ight) CONF(iguration): A simple human-readable data serialization format for dynamic configuration.**

:Author: peter1000
:Github: https://github.com/peter1000

|

:Version: 5.0 (20140621)

.. note:: the basic `LCONF Specification as of version 5.0 (20140621)` is considerate as finished.

.. contents::
   :depth: 3


Abstract
========

`LCONF` is a light - human-friendly, simple readable data serialization format for dynamic configuration.


Designed around:
----------------

- READABILITY
- NAMED SECTIONS
- FOUR MAIN STRUCTURES
- ONE DYNAMIC BLOCK STRUCTURE
- VALUE TRANSFORMATION
- ORDER
- DEFAULT VALUES
- PRETTY EMITTING/DUMPING

- **Readability**

   - Sections
   - Lines
   - Indentation
   - Strings
   - # Comments
   - # Default-Comment/Empty Lines


- **Named Sections**

   - allows for extended text/info/explanations before or after them without the need of **#** Comment tags

   - multiple LCONF-Sections can be within one 'LCONF text source/file'


.. _Four_Main_Structures:

- **Four Main Structures**

   - Key :: Value Pairs
      each `value` is always interpreted as a: `single string`
   - Key :: Value-Lists: oneline lists
      each `list item` is always interpreted as a: `single string`
   - Key-Value-Lists: multiline lists: values with indentation
      each `list item` is always interpreted as a: `single string`

      - just a different way of writing a list: mostly useful for long lists which might not be easy to read in one line

   - Key-Value-Mappings: items with indentation
      each `mapping item` is always interpreted as a: `Key :: Value pair`
         where the `value` is always interpreted as a: `single string`

         .. warning:: Key-Value-Mapping item **can not** have a list as value.

            Everything after the `Key-Value-Separator` is interpreted as a single string.


- **One Dynamic Block Structure**

   - Repeated Mapping-Blocks:

      - these allows to configure any number of such blocks within the 'LCONF text source/file'.


- **Value Transformation**

   - LCONF implements the idea of easy item value transformation.
      any Item-Value must be easily transformable using customary hook functions or some other ways to achieve such: depending on the library language

      Value Transformation is mostly used for type transformation (cast) because `basic LCONF is on purpose only text/string based`

         - but such `transformation` function could do also any other complex transformation

      .. note::

         - `Key :: Value Pairs`: each one can have a `transformation function` assigned

         - `Key-Value-Lists` and `Key :: Value-Lists`: can have only one `transformation function` which will be applied to each item in the list

            - of course it can be complex to transform each item to something different: e.g. item1 to int, item2 to float ect..

         - `Key-Value-Mappings`: can not have directly a `transformation function` assigned

               - but each item line `Key :: Value Pairs` can have a separate `transformation function` assigned


      .. warning::

         The following can never have a `transformation function` assigned:

            - `BLK Identifier` lines
            - `BLK-Name` lines
            - `Key-Value-Mapping` lines

               - but each item line can have a separate `transformation function` assigned

- **Order**
   in general LCONF is ordered:

      - Key-Value-Mappings:
         Items (Key :: Value pair) with indentation are unordered: but any library **must implement** an option to loop over it in order as defined in a `LCONF-Default-Template-Structure`

      - Repeated Mapping-Blocks:
         Block-Names are unordered: but any library **must implement** an option to loop over it in order as defined in the parsed 'LCONF text source/file'

   .. note::

      - Any order will always be based on the `LCONF-Default-Template-Structure` and not on the 'LCONF text source/file'

         - **EXCEPTION:** the order of Block-Names: will be always as in the 'LCONF text source/file' (as they are not previously known)


- **Default Values**
   Default LCONF-values and all structures must be implemented within the code. `LCONF-Template-Default-Structure`

   - parsing a LCONF-Section (string/file) will just overwrite any default values

      So the simplest LCONF is only a START/END TAG:
         which will be parsed to all implemented defaults as nothing gets overwritten
         There won't be any Repeated Blocks because there are no default Block-Names set.

      .. code-block:: python

         ___SECTION :: DefaultLCONF
         ___END


      .. note:: To get `Default-Values` do not define the item in the 'LCONF text source/file'

         - for `Repeated Blocks`: to get the `Default-Values` for a whole Block: only define the Block-Identifier and the Block-Name without any items defined

   - emitting/dumping must support for output of:

         - `Default-Comment/Empty Lines`

   - Any LCONF library **must** implement an option to emit/dump a default LCONF-Section with an optional 'dummy-blk'


- **Pretty Emitting/Dumping**

   LCONF actively supports `pretty` printing (emitting/dumping).

   1. By design there is a strict predefined outline of indentation, structure ect..
   2. For list items there are 2 option implemented:

      - oneline lists: empty lists or usually used for lists with few items
      - multiline lists with item indentation: usually used for lists with more items


   3. # `Default-Comment/Empty Lines`

      - unlike many other formats LCONF design has full support for emitting/dumping with `Default-Comment/Empty Lines`

      .. warning:: LCONF does not support parsing **#** Comment lines from the 'LCONF text source/file'

         - Such are skipped by design


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


Specification
=============


LCONF-Default-Template-Structure
--------------------------------

LCONF does require a predefined implemented `LCONF-Default-Template-Structure` - one can not >> `just parse` << a 'LCONF text source/file'

   - REASON: LCONF is based on the idea of defaults which must be implemented previously.

      -  parsing a 'LCONF text source/file' only overwrites the defaults for set items

Depending on the library and coding language such `LCONF-Default-Template-Structure` can be different but must have some common features:

1. should be quite easily to implement
2. must support options for easily defining value transformation
3. must support option to define: default comment lines, default empty lines which can be emitted/dumped
4. must support option to define: order of all LCONF items, keys, values, blocks ect..


Default-Comment/Empty Lines
---------------------------

The `LCONF-Default-Template-Structure` can define `Default-Comment/Empty Lines` which can be emitted/dumped.

.. warning::

   before `Block-Names` (dummy_blk) there may be no `Default-Comment/Empty Lines`

   .. note:: This does not apply to the 'LCONF text source/file' as such Comments are always skipped when the source text gets parsed


Strings
-------

The LCONF uses only one native type: strings

* **ALL:** key, value, list item, mapping item, repeated Block Identifier, repeated Block-Name, Comment lines: `are all strings`

.. note::

   - empty `Key :: Value-List` or `Key-Value-List`: [] returns an `empty type list`
      overwrites any default list values

   - unlike many other formats: e.g. LCONF does not use quotation for strings

   - additionally it supports:

      - empty string values: for `Key :: Value Pairs` are supported: where the value is left out and the last space after the double colon is skipped

         .. warning::   LCONF does not at all support trailing spaces

      - optional casting to different data types


Key :: Value Separator
----------------------

`one space, double colons, one space`  **Key :: Value**
   is used as a: KEY VALUE separator

.. note:: Exception for empty string values: the last space is skipped so that there is no trailing space.


Key :: Value Pair
-----------------

Key/Value mapping

Uses the `Key :: Value Separator`_ **::**

.. note:: Each `value` is always interpreted as a: `single string`

**KEY :: VALUE string**

   - `Color :: Blue`
   - `mykey :: a long sentence with`

   .. note:: Empty `Key :: Value Pair`: for empty values the last space of the `Key :: Value Separator`_ is skipped

      - `MyEmptyKeyValuePair ::`


Key :: Value-List
-----------------

Ordered collection of items: oneline list

Uses the `Key :: Value Separator`_ **::** and as value a collection of ordered items `enclosed in square brackets`

.. note:: Each `list item` is always interpreted as a: `single string` within a list obj.

**KEY :: VALUE list of strings**

   - `Names :: [Tim,Sandra,Max]`

      - `Key :: Value-List`

         - start with `left bracket` **[**
         - and end with`right bracket` **]**

      - items are separated by `comma` **,**

         - IMPORTANT: spaces are not stripped

      .. note:: Empty `Key :: Value-List`: empty lists are always one line lists using as value only the `square brackets`: **[]**

         - `MyEmptyListValue :: []`
            This overwrites any set default list values


Key-Value-List
--------------

Basically the same as `Key :: Value-List`_ just using a different notation for readability

Ordered collection of items: multi-line list

The Value lines (list items) uses one indentation level (3 spaces)

.. note:: Each `list item` is always interpreted as a: `single string` within a list obj.

**KEY**

   - `VALUE list item1 string`
   - `VALUE list item2 string`


   .. note:: Empty `Key-Value-List`: empty lists are always one line lists `Key :: Value-List`_ using as value only the `square brackets`: **[]**

      - `MyEmptyListValue :: []`
            This overwrites any set default list values


Key-Value-Mapping
-----------------

Unordered collection of items (`Key :: Value Pair`_) but any library must implement an option to loop over it in order as defined in a default template

The `Key :: Value Pair` lines (mapping items) uses one indentation level (3 spaces)

.. note:: Each `mapping item` is always interpreted as a: `Key :: Value Pair`_

**KEY**

   - `Car :: red`
   - `Shoes :: blue`


   .. note:: There are no empty `Key-Value-Mapping`

      Do get all default values for each item key: do not define the `Key-Value-Mapping` in the LCONF


Repeated Mapping-Block Identifier
---------------------------------

`asterisk, one space`
   is used as Repeated Mapping-Block Identifier

   - `* Color_BLK`


Comment-Line Identifier
-----------------------

`one number sign`
   is used as Comment-Line Identifier

   - `#`

If the first none space character in a line is **#** the line is considered a Comment-Line

Comment-Line must have the indentation level of the following line (disregarding empty lines)


Indentation
-----------

**Indentation** is exact 3 spaces per level

- NO_INDENT = 0 leading space

   - Key :: Value Pairs
   - Key :: Value-Lists
   - Key-Value-Lists: the key
   - Key-Value-Mappings: the key
   - Repeated Mapping-Blocks Identifier
   - # Comment-Lines

- ONE_INDENT = 3 leading spaces

   - Key-Value-Lists: the values with indentation
   - Key-Value-Mappings: the items (Key :: Value Pair) with indentation
   - Repeated Block-Names
   - # Comment-Lines

- TWO_INDENT = 6 leading spaces

   - Repeated Block: Key :: Value Pairs
   - Repeated Block: Key :: Value-Lists
   - Repeated Block: Key-Value-Lists: the key
   - Repeated Block: Key-Value-Mappings: the key
   - # Comment-Lines

- THREE_INDENT = 9 leading spaces

   - Repeated Block: Key-Value-Lists: the values with indentation
   - Repeated Block: Key-Value-Mappings: the items (Key :: Value Pair) with indentation
   - # Comment-Lines

|

Section Start/End Tags
----------------------

`___SECTION`, `___END`
   are reserved for the purpose of `SECTION START/END TAGS`

.. warning:: Section Start/End Tag are forbidden in any form except for the defined purpose. `Section Start/End Tags`_


- `three underlines, capital SECTION`

   **SECTION START TAG**
      `___SECTION`

      - This is followed by a `Key :: Value Separator`_ and the Section Name: l_section_name is required: can not be an empty string value

      - A first line for a LCONF-Section called: EXAMPLE would look like

         - `___SECTION :: EXAMPLE`

- `three underlines, capital END`

   **SECTION END TAG**

      - `___END`


Dynamic Repeated Blocks
-----------------------

Dynamic Repeated Blocks are for configurations where one wants to be able to specify multiple blocks

.. note:: there is one type of Dynamic Blocks:

   - Repeated Mapping-Blocks:
      this does not keep the order of the Block-Names
         but any library must implement an option to loop over it in order as defined in a default template

**Dynamic Repeated Blocks** consist of:

1. Block Identifier: NO_INDENT = 0 leading space

   - `Repeated Mapping-Block Identifier`_

   .. note:: Empty `Repeated Block Identifiers`: without any Block-Names are written the same way

2. Block-Names: ONE_INDENT = 3 leading spaces

   - any number of Block-Names:

   .. note:: if a `Block-Name` is defined without any items at all: it is still valid using all defaults

3. Block-Item:
   TWO_INDENT = 6 leading spaces
   and THREE_INDENT = 9 leading spaces

   A `Block-Item` can be any of the `Four_Main_Structures`_

      - Key :: Value Pairs
      - Key :: Value-Lists: oneline lists
      - Key-Value-Lists: values with indentation
      - Key-Value-Mappings: items with indentation


Example MultiAddresses
++++++++++++++++++++++

multiple addresses implemented with: Repeated Blocks

.. code-block:: python

   ___SECTION :: PERSON

   Name :: Rosa Jacko
   Sex :: female

   # Implementing multiple addresses: Repeated Mapping-Blocks
   # In this case one could configure any number of Addresses
   * AddressMappingBlock
      Address1
         Street :: my main street
         Zip_Code :: 123
         City :: New York

      Address2
         Street :: my summer place street
         Zip_Code :: 198
         City :: London

   ___END


Without using a dynamic repeated block option one can only use a predefined max number of Addresses:
because the keys must be unique and predefined in the implementing code

Example TwoAddresses
++++++++++++++++++++

two addresses implemented directly and with Key-Value-Mappings


.. code-block:: python

   ___SECTION :: PERSON

   Name :: Rosa Jacko
   Sex :: female

   # Implementing 2 addresses: Key :: Value Pairs
   Street1 :: my main street
   Zip_Code1 :: 123
   City1 :: New York

   Street2 :: my summer place street
   Zip_Code2 :: 198
   City2 :: London

   # Implementing 2 addresses: Key-Value-Mappings
   Address1
      Street :: my main street
      Zip_Code :: 123
      City :: New York

   Address2
      Street :: my summer place street
      Zip_Code :: 198
      City :: London

   ___END


Restrictions
------------

**A library does not have to validate this restrictions: validation is optional.**


Restrictions: Section Start/End Tag
+++++++++++++++++++++++++++++++++++

.. warning:: Section Start/End Tag are forbidden in any form except for the defined purpose. `Section Start/End Tags`_


Restrictions: List opening Tag: **[**
+++++++++++++++++++++++++++++++++++++

.. warning:: The first character after a `Key :: Value Separator`_ may not be a `left square bracket` **[**

   Except for `Key :: Value-List`_ or empty `Key-Value-List`_


Restrictions: Keys, Repeated Block Identifiers
++++++++++++++++++++++++++++++++++++++++++++++

`Keys`, `Repeated Block Identifiers` with `Block-Structure`, any `Default-Comment/Empty Lines` are predefined within the code of the `LCONF-Default-Template-Structure`.  For a python example see : "Code Usage - How To Implement" in the README

- all `Main Keys` and `Block-Identifier`: must be unique

- `withing a Key-Value-Mapping`: the keys must be unique

- `Block-Names`: must be unique within one ` Repeated Block Identifier`

- `Block-Keys`: must be unique within one `Block`


Restrictions: No Trailing Spaces
++++++++++++++++++++++++++++++++

Lines may not have any trailing spaces



Restrictions: Comments
++++++++++++++++++++++

Comment lines **#** within a `LCONF-Section` are required to have the indentation of the next none empty line


Restrictions: Default-Comment/Empty Lines
+++++++++++++++++++++++++++++++++++++++++

before `Block-Names` (dummy_blk) there may be no `Default-Comment/Empty Lines` within the code of the `LCONF-Default-Template-Structure`.



LCONF Examples
==============

EXAMPLE 1
---------

With many comments and explanations

LCONF: BASE EXAMPLE:

.. code-block:: python

   ___SECTION :: BaseEXAMPLE

   # Comment-Line: below: Main `Key :: Value Pair`
   key1value_pair :: value1
   # Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
   key2value_pair ::
   key3value_pair :: 1234
   key4value_pair :: True
   key5value_pair :: False
   key6value_pair :: None
   key7value_pair :: 1456.984
   key8value_pair :: true
   key9value_pair :: false

   # Comment-Line: below is a Main `Key-Value-Mapping`
   key10value_mapping
      # Comment-Line:  Key-Value-Mapping items: are `Key :: Value Pairs`
      mapping10_key1 :: null
      mapping10_key2 :: true
      mapping10_key3 :: 123456
      mapping10_key4 :: False
      mapping10_key5 :: None
      mapping10_key6 :: 0001-01-01-00:00

   # Comment-Line: below is a Main `Key-Value-Mapping` with an empty value
   #  the implementation supports: mapping11_key1, mapping11_key2
   key11value_mapping
      # Comment line1 to test `Key-Value-Mapping` recognition
      # Comment line2 to test `Key-Value-Mapping` recognition
      mapping11_key1 :: null
      mapping11_key2 :: ''

   # Comment-Line: below is a Main `Key-Value-List`
   key12list
      # Comment-Line: List item
      value_list_item1
      value_list_item2

   # Comment-Line: below is a Main `Key :: Value-List`
   key13value_pairlist :: [123,8945,278]

   # Comment-Line: below is a Main `Key :: Value-Lists` with an empty list: overwriting any defaults
   key14value_pairlist :: []

   # Comment-Line: below: `Repeated Mapping-Block Identifier`
   #  this will loose the order of the `Repeated Block-Names` after parsing
   #  but any library must implement an option to loop over it in order as defined in the section
   * RepeatedBlk1
      # Comment-Line: BLK_OBJ0 uses all 8 possible - defined items
      BLK_OBJ0
         # Comment-Line: below Block-Item `Key-Value-Mapping` with all 3 defined items
         MyKey1mapping
            # Comment-Line: below Block `Key-Value-Mapping-Item` blk_mapping_key1
            blk_mapping_key1 :: some text
            blk_mapping_key2 :: 12345.99
            blk_mapping_key3 :: True
         MyKey2 :: 789.9
         MyKey3 :: True
         MyKey4 :: 2014-05-08-13:45
         MyKey5list :: [test1,test2]
         # Comment-Line: Block-Item `Key :: Value-List` with Empty List
         MyKey6list :: []
         # Comment-Line: Block-Item `Key :: Value-List`
         MyKey7list :: [True,False,False,True]
         MyKey8 :: some text
      # Comment-Line: BLK_OBJ1 does only use a subset of the defined items:
      # all others will be set to default values as implemented
      BLK_OBJ1
         # Comment-Line: overwrites only 1 Main Key: MyKey2. All other items are default values
         MyKey2 :: 999.0

      BLK_OBJ2
         # Comment-Line: below Block-Item `Key-Value-Mapping` with only one defined item of 3: the rest gets default values
         MyKey1mapping
            blk_mapping_key3 :: False
         MyKey2 :: 89456.456
         MyKey3 :: True
         MyKey4 :: 1982-02-26-12:15
         # Comment-Line: Block-Item `Key :: Value-List`
         MyKey7list :: [True,False,False,True]
      BLK_OBJ3
         MyKey1mapping
            blk_mapping_key1 ::
            blk_mapping_key2 :: 188.0
            blk_mapping_key3 :: False
         MyKey2 :: 789.9
         MyKey3 :: True
         MyKey4 :: 2014-05-12-01:52
         MyKey5list :: [dog,cat]
         MyKey8 :: just a test
      # Comment-Line: Repeated Block-Name: will be using all default values
      BLK_OBJ4

   ___END


EXAMPLE 2 (JSON - LCONF)
------------------------

JSON

.. code-block:: python

   {
      "first": "John",
      "last": "Doe",
      "age": 39,
      "interests": [
         "Reading",
         "Mountain Biking",
         "Hacking"
      ],
      "registered": true,
      "salary": 70000,
      "sex": "M"
   }


LCONF Key-Value-List

.. code-block:: python

   ___SECTION :: PERSON
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


LCONF Key :: Value-List

.. code-block:: python

   ___SECTION :: PERSON
   first :: John
   last :: Doe
   age :: 39
   # Key :: Value-List
   interests :: [Reading,Mountain Biking,Hacking]
   registered :: true
   salary :: 70000
   sex :: M
   ___END


LCONF using dynamic Repeated Mapping-Block

.. code-block:: python

   ___SECTION :: PERSON
   # Repeated Mapping-Block
   * Persons_BLK
      person1
         first :: John
         last :: Doe
         age :: 39
         interests :: [Reading,Mountain Biking,Hacking]
         registered :: true
         salary :: 70000
         sex :: M
   ___END



EXAMPLE 3 (JSON - LCONF)
------------------------

JSON

.. code-block:: python

   {
      "first": "John",
      "last": "Doe",
      "sex": "M",
      "age": 39,
      "salary": 70000,
      "favorites": {
         "food": "Spaghetti",
         "sport": "Soccer",
         "color": "Blue"
      },
      "registered": true
   }


LCONF: using Key-Value-Mapping: note (it could also be written using a Repeated Block with only 1 Block-Name configured)

.. code-block:: python

   ___SECTION :: PERSON
   first :: John
   last :: Doe
   sex ::
   age :: 39
   salary :: 70000
   # Key-Value-Mapping
   favorites
      food :: Spaghetti
      sport :: Soccer
      color :: Blue
   registered :: True
   ___END

   '''


EXAMPLE 4 (JSON - LCONF)
------------------------

JSON

.. code-block:: python

   {
      "skills": [
         {
            "category": "PHP",
            "tests": [
               {
                  "score": 90,
                  "name": "One"
               },
               {
                  "score": 96,
                  "name": "Two"
               }
            ]
         },
         {
            "category": "Node.js",
            "tests": [
               {
                  "score": 97,
                  "name": "One"
               },
               {
                  "score": 93,
                  "name": "Two"
               }
            ]
         }
      ]
   }


.. note:: a json structure like above needs some small changes to work in LCONF

rewrite of the json `example` using a: Repeated Mapping-Block

.. code-block:: python

   ___SECTION :: SKILLS
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


rewrite of the json `example` using a: Repeated Mapping-Block and Key-Value-Mapping

.. code-block:: python

   ___SECTION :: SKILLS
   # Repeated Mapping-Block
   * categories
      PHP
         # Key-Value-Mapping
         tests
            test1_name :: One
            test1_score :: 90
            tests2_name :: Two
            tests2_score :: 96
      Node.js
         # Key-Value-Mapping
         tests
            test1_name :: One
            test1_score :: 97
            tests2_name :: Two
            tests2_score :: 93
   ___END

|
|

`LCONF` is distributed under the terms of the BSD 3-clause license.
Consult LICENSE.rst or http://opensource.org/licenses/BSD-3-Clause.

(c) 2014, `peter1000` https://github.com/peter1000
All rights reserved.

|
|
