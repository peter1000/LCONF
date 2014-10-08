.. image:: _static/LCONFMain350_220.png
   :align: center

.. _LCONF_specification:

.. index:: LCONF; specification examples, Examples; examples

=============================
LCONF: Specification Examples
=============================

EXAMPLE 1
=========

LCONF: BASE EXAMPLE

.. lconf-example:: LCONF `BaseEXAMPLE` with many comments and explanations

   .. code-block:: lconf

      ___SECTION :: BaseEXAMPLE

      # Comment-Line: below Main `Key :: Value Pair` using an `Empty-KeyValuePair-ReplacementValue` "NOT-DEFINED"
      #               Transform Function is not used and set to None
      key1value_pair ::
      # Comment-Line: below is a `Key :: Value Pair` with an empty value string: which is skipped
      key2value_pair ::
      key3value_pair ::
      key4value_pair :: True
      key5value_pair :: False
      key6value_pair :: None
      # Comment-Line: Using a Transform Function and using an `Empty-KeyValuePair-ReplacementValue` "-94599.5"
      #               as default value an empty string is set
      key7value_pair ::
      key8value_pair :: true
      # Comment-Line: Values can be most characters and also longer lines
      key9value_pair :: different characters # \n * | , & @  https://translate.google.com/ translate ਅਨੁਵਾਦ  翻訳する μεταφράζω

      # Comment-Line: below is a Main `Key-Value-Mapping`
      . key10value_mapping
         # Comment-Line:  Key-Value-Mapping items: `Key :: Value Pair`
         mapping10_key1 :: False
         mapping10_key2 :: true
         mapping10_key3 :: 123456

         # Comment-Line:  Key-Value-Mapping item: `Key :: Value-List`
         - mapping10_key4_list :: 1,2

         # Comment-Line:  Key-Value-Mapping item: `Key-Value-List`
         - mapping10_key5_list
            1
            2

         # Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`
         - mapping10_key6_list |x|y|
            1,3
            2,6

         # Comment-Line:  Key-Value-Mapping item: `List-Of-Tuples`
         - mapping10_key7_list |name|b|c|
            Tom,     2.0, 3
            Peter,   2.4, 5

      # Comment-Line: below is a Main `Key-Value-Mapping`
      . key11value_mapping
         # Comment-Line:  Key-Value-Mapping item: `Key :: Value Pair`
         mapping11_key1 :: /home/examples/

         # Comment-Line:  Key-Value-Mapping item: an other nested `Key-Value-Mapping`
         . mapping11_key2_mapping
            # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pair`
            mapping11_key2_nested_mapping_key1 :: 2014-05-08 13:39

            # Comment-Line:  nested Key-Value-Mapping item: `Repeated-Block-Identifier`
            * mapping11_key2_nested_mapping_key2_block_identifier

               # Comment-Line: `Block-Name1`
               sky_blue_blk_name1
                  # Comment-Line:  Block items: `Key :: Value Pairs`
                  #       Using a Transform Function and using an `Empty-KeyValuePair-ReplacementValue` "0"
                  #               as default value an empty string is set
                  blk_item_red ::
                  blk_item_green :: 206
                  blk_item_blue :: 235

            # Comment-Line:  nested Key-Value-Mapping item: `Key :: Value Pair`
            mapping11_key2_nested_mapping_key3 :: car

            # Comment-Line: nested Key-Value-Mapping item: `Key-Value-List`
            - mapping11_key2_nested_mapping_key4_list
               # Comment-Line: List item
               value_list_item1
               value_list_item2

      # Comment-Line: below is a Main `Key-Value-List`
      - key12list
         # Comment-Line: List item
         value_list_item1
         value_list_item2

      # Comment-Line: below is a Main `Key :: Value-List`
      - key13value_pairlist :: 123,8945,278

      # Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
      - key14list_of_color_tuples |Color Name|Red|Green|Blue|
         # Comment-Line: `List-Of-Tuples` item lines (rows)
         forestgreen,   34,   139,  34
         brick,         156,  102,  31

      # Comment-Line: below is a Main `Key :: Value-List` with an empty list: overwriting any defaults
      - key15value_pairlist ::

      # Comment-Line: below is a Main `Key-Value-List` with an empty list: overwriting any defaults
      - key16value_pairlist

      # Comment-Line: below is a Main `List-Of-Tuples` with an empty list: overwriting any defaults
      - key17list_of_tuples |a|b|c|


      # Comment-Line: below: `Repeated-Block-Identifier`
      #  this will loose the order of the `Repeated Block-Names` after parsing
      #  but any library must implement an option to loop over it in order as defined in the section
      * RepeatedBlk1
         # Comment-Line: BLK_OBJ1 (Block-Name) uses all 8 possible - defined items
         BLK_OBJ1

            # Comment-Line: below Block-Item `Key-Value-Mapping` with all 4 defined items
            . MyKey1_mapping
               blk_mapping_key1 :: some text
               # Comment-Line: Using a default value: "9999.999" and Transform Function
               #               as well as  using an `Empty-KeyValuePair-ReplacementValue` "-9999999999.99999999"
               blk_mapping_key2 :: 12345.99
               blk_mapping_key3 :: True

               # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
               . blk_mapping_key4
                  nested_mapping_key1 :: franz
                  # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
                  - interests
                     sport
                     reading

                  # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
                  * Nested Repeated Block Identifier
                     # Comment-Line:  keys do not have to be a single word: below a multi words Block-Name
                     Nested Block Name1
                        block-item_key1 :: 12345.99
                        - block-item_key2_list :: False,True,True
                        # Comment-Line:  block-item_key3_list: `List-Of-Tuples`
                        - block-item_key3_list |name|height_cm|weight_kg|
                           # Comment-Line: |name|height_cm|weight_kg|
                           Tim,     178,     86
                           John,    166,   67

            MyKey2 :: 789.9
            MyKey3 :: True

            # Comment-Line:  empty `Key :: Value Pair`
            MyKey4 ::
            - MyKey5list :: test1,test2

            # Comment-Line: Block-Item `Key :: Value-List` with Empty List
            - MyKey6list ::

            # Comment-Line: Block-Item `Key :: Value-List`
            - MyKey7list :: True,False,False,True

            MyKey8 :: some text

         # Comment-Line: BLK_OBJ2 (Block-Name)
         BLK_OBJ2

            # Comment-Line: below Block-Item `Key-Value-Mapping` with only some defined items
            . MyKey1_mapping
               blk_mapping_key1 :: some text
               # Comment-Line: Using a default value: "9999.999" and Transform Function
               #               as well as  using an `Empty-KeyValuePair-ReplacementValue` "-9999999999.99999999"
               blk_mapping_key2 ::
               blk_mapping_key3 :: False

               # Comment-Line:  Block-Item `Key-Value-Mapping`: an other nested `Key-Value-Mapping`
               . blk_mapping_key4
                  nested_mapping_key1 :: julia
                  # Comment-Line:  Block-Item  nested `Key-Value-Mapping` item: an other nested `Key-Value-Lists`
                  - interests
                     golf
                     flowers

                  # Comment-Line:  Block-Item: an other deep nested `Repeated-Block-Identifier`
                  * Nested Repeated Block Identifier
                     # Comment-Line:  Block-Name: all values will use defaults
                     Nested Block Name1
                     # Comment-Line:  Block-Name: and defining an empty list: block-item_key2_list
                     Nested Block Name2
                        - block-item_key2_list ::
                        # Comment-Line:  block-item_key3_list: `List-Of-Tuples`: to define an empty list: skip any item lines
                        - block-item_key3_list |name|height_cm|weight_kg|

            # Comment-Line: Block-Item `Key-Value-Lists`
            - MyKey7list
               True
               False
               True

         BLK_OBJ3
            # Comment-Line: below Block-Item empty `Key-Value-Mapping`: will use all defaults
            #     similar if it would not be defined at all
            . MyKey1_mapping

            # Comment-Line:  `Key :: Value Pairs`
            MyKey4 ::
            - MyKey5list :: test1,test2

         # Comment-Line: Repeated Block-Name: will be using all default values
         #    Note: nested Blocks are not having any default names: so the items are skipped
         BLK_OBJ4

      ___END


EXAMPLE 2
=========

(JSON - LCONF)

.. json-example::

   .. code-block:: json

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

.. lconf-example:: LCONF using `Key-Value-List`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 2 a
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      salary :: 70000
      # Comment-Line: `Key-Value-List`
      - interests
         Reading
         Mountain Biking
         Hacking
      registered :: True
      ___END


.. lconf-example:: LCONF using `Key :: Value-List`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 2 b
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      salary :: 70000
      # Comment-Line: `Key :: Value-List`
      - interests :: Reading,Mountain Biking,Hacking
      registered :: True
      ___END


EXAMPLE 3
=========

(JSON - LCONF)

.. json-example::

   .. code-block:: json

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

.. lconf-example:: LCONF using `Key-Value-Mapping`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 3
      first :: John
      last :: Doe
      sex :: M
      age :: 39
      salary :: 70000
      # Comment-Line: `Key-Value-Mapping`
      . favorites
         food :: Spaghetti
         sport :: Soccer
         color :: Blue
      registered :: True
      ___END


EXAMPLE 4
=========

(JSON - LCONF)

.. json-example::

   .. code-block:: json

      {
         "registered_employees": 28594,
         "Employee": {
            "Person1": {
               "first": "John",
               "last": "Doe",
               "sex": "M",
               "age": "39",
               "past_salary": {
                  "year2012": 45000,
                  "year2013": 62000
               },
               "emails": [
                  "<xaver@dot.com>",
                  "<xaver23@yahoo.com>"
               ]
            }
         },
         "registered_customer": 28594,
         "accounting": [
            [
               "2010",
               38459845,
               15835945,
               3000945
            ],
            [
               "2011",
               38459845,
               15835945,
               3000945
            ],
            [
               "2012",
               28456849,
               4846123,
               2599901
            ],
            [
               "2013",
               38459845,
               15835945,
               3000945
            ]
         ]
      }


.. lconf-example::

   LCONF: using `Repeated-Block Identifier` and `List-Of-Tuples`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 4 a
      registered_employees :: 28594
      * Employee
         Person1
            first :: John
            last :: Doe
            sex :: M
            age :: 39
            . past_salary
               year2012 :: 45000
               year2013 :: 62000
            - emails
               <xaver@dot.com>
               <xaver23@yahoo.com>
      registered_customer :: 28594
      - accounting |item1|item2|item3|item4|
         2010,38459845,15835945,3000945
         2011,38459845,15835945,3000945
         2012,28456849,4846123,2599901
         2013,38459845,15835945,3000945
      ___END


   LCONF: using `Key-Value-Mapping Identifier` and `List-Of-Tuples`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 4 b
      registered_employees :: 28594
      . Employee
         . Person1
            first :: John
            last :: Doe
            sex :: M
            age :: 39
            . past_salary
               year2012 :: 45000
               year2013 :: 62000
            - emails
               <xaver@dot.com>
               <xaver23@yahoo.com>
      registered_customer :: 28594
      - accounting |item1|item2|item3|item4|
         2010,38459845,15835945,3000945
         2011,38459845,15835945,3000945
         2012,28456849,4846123,2599901
         2013,38459845,15835945,3000945
      ___END


EXAMPLE 5
=========

(JSON - LCONF)

.. json-example::

   .. code-block:: json

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

   Reason: List items may not be an other mapping (dict/dictionary) or list:
   :ref:`Restrictions Item Types in Lists <restrictions_item_types_in_lists>`


Rewrite of the json `example` for `LCONF`


.. lconf-example::

   LCONF: using `Repeated-Block` and renaming the item values to support 2 groups

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 5 a
      # Repeated-Block-Identifier
      * categories
         # using `Block-Names`
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


.. lconf-example::
   LCONF: using `Repeated-Block` and `Key-Value-Mapping`

   .. code-block:: lconf

      ___SECTION :: EXAMPLE 5 b
      # Repeated-Block-Identifier
      * categories
         # using `Block-Names`
         PHP
            # Key-Value-Mapping
            . test1
               name :: One
               score :: 90
            . test2
               name :: Two
               score :: 96
         Node.js
            # Key-Value-Mapping
            . test1
               name :: One
               score :: 97
            . test2
               name :: Two
               score :: 93
      ___END
