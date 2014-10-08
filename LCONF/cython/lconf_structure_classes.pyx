"""
=============================
LCONF.lconf_structure_classes
=============================

Overview
========
Most of this code is based on the `ReOBJ package <https://github.com/peter1000/ReOBJ>`_. see `LICENSE` for more info

These Classes are used for the :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` to implement the
defaults and order.


.. _lconf-default-template-structure-usage-example:

.. index:: LCONF; usage LCONF-Default-Template-Structure, Usage; LCONF-Default-Template-Structure usage

LCONF-Default-Template-Structure-Usage
======================================

`LCONF` does require a predefined implemented `LCONF-Default-Template-Structure` one can not >> `just parse` << a
'LCONF text source/file'.

The "official python lconf library" uses for a `LCONF-Default-Template-Structure` **exclusively** the predefined classes in
this module: `LCONF/LconfStructureClasses.py`


.. index:: Usage; LCONF: START/END TAG: (Root class)

`LCONF MAIN (ROOT) obj`: uses the **Root class**
------------------------------------------------

.. lconf-example::

   .. code-block:: lconf

      # Comment-Line: Root/Main LCONF-Section START TAG Line
      ___SECTION :: Example LCONF Root
      key1 :: value1
      key2 :: value2
      key3 :: value3
      key4 ::
      # Comment-Line: Root/Main LCONF-Section END TAG Line
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: Root

   Every `LCONF-Default-Template-Structure` must have at least the `Root class`

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: Root/Main key value pair'),
         ('key1', 'default_value1'),
         ('key2', 'default_value2', transform_function),
         ('#2', '# Comment: Root/Main key value pair with transform_function and `Empty-KeyValuePair-ReplacementValue`'),
         ('key3', 'default_value3', transform_function, 'empty_replacement_value3'),
         ('key4', 'default_value4', transform_function, 'empty_replacement_value4'),
      ])


.. index:: Usage; LCONF: `Key-Value-Mapping`: (KVMap class)

LCONF `Key-Value-Mapping`: uses the **KVMap class**
---------------------------------------------------

.. lconf-example::

   # `Key-Value-Mapping` can not have a direct transform function applied

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key-Value-Mapping`
      # Comment-Line: below is a Main `Key-Value-Mapping`
      . key_value_mapping
         key1 :: value1
         key2 :: value2
         key3 :: value3
         key4 ::
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: KVMap

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `Key-Value-Mapping`
            ('key_value_mapping', KVMap([
            ('#1', '# Comment-Line: Root/Main key value pair'),
            ('key1', 'default_value1'),
            ('key2', 'default_value2', transform_function),
            ('#2', '# Comment: Root/Main key value pair with transform_function and  `Empty-KeyValuePair-ReplacementValue`'),
            ('key3', 'default_value3', transform_function, 'empty_replacement_value3'),
            ('key4', 'default_value4', transform_function, 'empty_replacement_value4'),
         ])),
      ])


.. index:: Usage; LCONF: `Key :: Value-List`: (KVList class)

LCONF `Key :: Value-List`: uses the **KVList class**
----------------------------------------------------

`Key :: Value-List` and `Key-Value-List` both use the **KVList class**

The implementation of them are the same except that the parameter `use_oneline` is set for default emitting.

.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key :: Value-List`
      # Comment-Line: below is a Main `Key :: Value-List`
      - list :: 1,2,3
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: KVList

   to emit as default `Key :: Value-List` set parameter **use_oneline** to **True**

   # using **no transform function**

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: below is a Main `Key :: Value-List`: use_oneline is True'),
         ('list', KVList(True, ['default_value1', 'default_value2']))
      ])

   # using **a transform function**: applied to each list item

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: below is a Main `Key :: Value-List`: with transform_function - use_oneline is True '),
         ('list', KVList(True, ['default_value1', 'default_value2']), transform_function)
      ])

.. index:: Usage; LCONF: `Key-Value-List`: (KVList class)

LCONF `Key-Value-List`: uses the **KVList class**
-------------------------------------------------

`Key-Value-List` is very similar to `Key :: Value-List` and also uses the **KVList class**

.. lconf-example::

   to emit as default `Key-Value-List` set parameter **use_oneline** to **False**

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key-Value-List`
      # Comment-Line: below is a Main `Key-Value-List`
      - list
         1
         2
         3
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: KVList

   # using **no transform function**

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: below is a Main `Key :: Value-List`: use_oneline is False'),
         ('list', KVList(False, ['default_value1', 'default_value2']))
      ])

   # using **a transform function**: applied to each list item

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: below is a Main `Key :: Value-List`: with transform_function - use_oneline is False '),
         ('list', KVList(False, ['default_value1', 'default_value2']), transform_function)
      ])


.. index:: Usage; LCONF: `List-Of-Tuples`: (ListOT class)

LCONF `List-Of-Tuples`: uses the **ListOT class**
-------------------------------------------------

.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `List-Of-Tuples`
      # Comment-Line: below is a Main `List-Of-Tuples` with 4 items: |Color Name|Red|Green|Blue|
      - list_of_color_tuples |Color Name|Red|Green|Blue|
         # Comment-Line: `List-Of-Tuples` item lines (rows)
         forestgreen,   34,   139,  34
         brick,         156,  102,  31
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: ListOT

   # using **no transform function**

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'
         ('list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), [
            ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue'),
            ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue')
         ])),
      ])

   # using **multiple transform functions**

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 4 columns: |Color Name|Red|Green|Blue|'
         ('list_of_color_tuples', ListOT(('Color Name', 'Red', 'Green', 'Blue'), [
            ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue'),
            ('default_value_Color_Name', 'default_value_Red', 'default_value_Green', 'default_value_Blue')
         ]), (None, transform_function, transform_function, transform_function)),
      ])

.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `List-Of-Tuples`
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      - list_of_point_tuples |x|y|z|
         # Comment-Line: `List-Of-Tuples` item lines (rows)
         1,3,7
         2,6,14
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: ListOT

   # using **one transform function** for each item in every list tuple (row)

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
         ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
            ('default_value_x', 'default_value_y', 'default_value_z'),
            ('default_value_x', 'default_value_y', 'default_value_z'),
         ]), transform_function),
      ])

.. lconf-example::

   `List-Of-Tuples` with missing items

   .. code-block:: lconf

      ___SECTION :: Example LCONF `List-Of-Tuples`
      # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
      - list_of_point_tuples |x|y|z|
         # Comment-Line: `List-Of-Tuples` item lines (rows) with missing items
         ,,
         2, ,14
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: ListOT

   # using **no column_replace_missing** items

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
         ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
            ('default_value_x', 'default_value_y', 'default_value_z'),
            ('default_value_x', 'default_value_y', 'default_value_z'),
         ])),
      ])

   # using **column_replace_missing** items

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
         ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
            ('default_value_x', 'default_value_y', 'default_value_z'),
            ('default_value_x', 'default_value_y', 'default_value_z'),
         ], column_replace_missing=('-1', '-1', '-1'))),
      ])

   # using **column_replace_missing** items and **one transform function** for each item in every list tuple (row)

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
         ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
            ('default_value_x', 'default_value_y', 'default_value_z'),
            ('default_value_x', 'default_value_y', 'default_value_z'),
         ], column_replace_missing=('-1', '-1', '-1')), transform_function),
      ])

   # using **column_replace_missing** items and **multiple transform function** for each item in every list tuple (row)

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: below is a Main `List-Of-Tuples` with 3 items: |x|y|z|
         ('list_of_point_tuples', ListOT(('x', 'y', 'z'), [
            ('default_value_x', 'default_value_y', 'default_value_z'),
            ('default_value_x', 'default_value_y', 'default_value_z'),
         ], column_replace_missing=('-1', '-1', '-1')), (transform_function, transform_function, transform_function)),
      ])


.. index:: Usage; LCONF: `Repeated-Block-Identifier`: (BlkI class)

LCONF `Repeated-Block-Identifier`: uses the **BlkI class**
----------------------------------------------------------

.. lconf-example::

   # `Repeated-Block-Identifier` can not have a direct transform function applied

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Repeated-Block-Identifier`
      # Comment-Line: below is a Main `Repeated-Block-Identifier`
      * My_Repeated_Block

         BlockName1
            key1 :: value1
            key2 :: value2
            key3 ::

         BlockName2
            key1 :: value1
            key2 :: value2
            key3 :: value3

      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: BlkI

   # `Repeated-Block-Identifier` **min_required_blocks, max_allowed_blocks** not defined (-1)

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: Root/Main `Repeated-Block-Identifier`: **min_required_blocks, max_allowed_blocks** not defined (-1)
         ('My_Repeated_Block', BlkI(-1, -1,
            # Comment-Line: Dummy Block
            Blk([
               # Comment-Line: Block key value pair
               ('key1', 'default_value1`'),
               # Comment-Line: Block key value pair with transform_function
               ('key2', 'default_value2', transform_function),
               ('#1', '# Comment: Block key value pair with transform_function and `Empty-KeyValuePair-ReplacementValue`'),
               ('key3', 'default_value3', transform_function, 'empty_replacement_value3'),
            ])
         )),

   # `Repeated-Block-Identifier` **min_required_blocks, max_allowed_blocks** set both to 2

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: Root/Main `Repeated-Block-Identifier`: **min_required_blocks, max_allowed_blocks** set both to 2
         ('My_Repeated_Block', BlkI(2, 2,
            # Comment-Line: Dummy Block
            Blk([
               # Comment-Line: Block key value pair
               ('key1', 'default_value1`'),
               # Comment-Line: Block key value pair with transform_function
               ('key2', 'default_value2', transform_function),
               ('#1', '# Comment: Block key value pair with transform_function and `Empty-KeyValuePair-ReplacementValue`'),
               ('key3', 'default_value3', transform_function, 'empty_replacement_value3'),
            ])
         )),
      ])


.. index:: Usage; LCONF: `Block-Name` - `Block` (dummy block): (Blk class)

LCONF `Block-Name` - `Block` (dummy block): uses the **BlkI class**
-------------------------------------------------------------------

.. lconf-example::

   # `Block-Name` - `Block` (dummy block) can not have a direct transform function applied

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Block-Name` - `Block` (dummy block)
      * My_Repeated_Block
         # Comment-Line: below is a `Block-Name` - `Block` (dummy block)
         BlockName1
            key1 :: value1
            key2 :: value2
            key3 :: value3
         # Comment-Line: below is another `Block-Name` - `Block` (dummy block)
         BlockName2
            key1 :: value1
            key2 :: value2
            key3 ::
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using class: Blk

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: Root/Main `Repeated-Block-Identifier`: **min_required_blocks set to 2, max_allowed_blocks** set to 5
         ('My_Repeated_Block', BlkI(2, 5,
            # Comment-Line: Dummy Block
            Blk([
               # Comment-Line: Block key value pair
               ('key1', 'default_value1`'),
               # Comment-Line: Block key value pair with transform_function
               ('key2', 'default_value2', transform_function),
               ('#1', '# Comment: Block key value pair with transform_function and `Empty-KeyValuePair-ReplacementValue`'),
               ('key3', 'default_value3', transform_function, 'empty_replacement_value3'),
            ])
         )),
      ])


.. index:: Usage; LCONF: `Key :: Value Pairs` items

LCONF `Key :: Value Pairs` items
--------------------------------
Tuple format may vary depending on implementation:

- (KEY, DEFAULT_VALUE)
- (KEY, DEFAULT_VALUE, TRANSFORM_FUNCTION)
- (KEY, DEFAULT_VALUE, TRANSFORM_FUNCTION OR None, Empty-KeyValuePair-ReplacementValue)

.. important:: TRANSFORM FUNCTIONS

   Must always be a proper `transform-function` except for `Key :: Value Pairs` which do not use any transformfunction but
   still an `Empty-KeyValuePair-ReplacementValue`. In such case the one uses `None` instead of any transform-function.

   - (KEY, DEFAULT_VALUE, None, Empty-KeyValuePair-ReplacementValue)


.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key :: Value Pairs` items
      # Comment-Line: Root/Main key value pair
      key1 :: value1
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using `Key :: Value Pairs` items

   # using **no transform function**

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: Root/Main key value pair
         ('key1', 'default_value1'),
      ])

   # using **a transform function**

   .. code-block:: python3

      example_lconf_template = Root([
         # Comment-Line: Root/Main key value pair with transform_function
         ('key1', 'default_value1', transform_function),
      ])

   # using **a transform function** and **Empty-KeyValuePair-ReplacementValue**

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment-Line: Root/Main key value pair with transform_function and Empty-KeyValuePair-ReplacementValue'),
         ('key1', 'default_value1', transform_function, 'empty_replacement_value1'),
      ])

   # using **no transform function** and **Empty-KeyValuePair-ReplacementValue**

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1a', '# Comment: Root/Main key value pair with no transform_function and Empty-KeyValuePair-ReplacementValue'),
         ('#1b', '#          Instead of the transform_function use None'),
         ('key1', 'default_value1', None, 'empty_replacement_value1'),
      ])

.. index:: Usage; LCONF: Empty `Key :: Value Pairs` items `Empty-KeyValuePair-ReplacementValue`

Empty `Key :: Value Pairs`
``````````````````````````
Empty `Key :: Value Pairs` are supported. One can optionally define an `Empty-KeyValuePair-ReplacementValue` in the
`LCONF-Default-Template-Structure`.


.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key :: Value Pairs` items
      # Comment-Line: Root/Main key value pair
      key1 :: value1
      key2 :: Red
      key3 ::
      ___END

.. python-example:: Example `LCONF-Default-Template-Structure`: using Empty `Key :: Value Pairs` with
                    `Empty-KeyValuePair-ReplacementValue` items

   # using **no transform function but with  `Empty-KeyValuePair-ReplacementValue`**
      if no transform function is used one MUST set it to `None`

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment: Root/Main key value pair - no transform function - with  `Empty-KeyValuePair-ReplacementValue`'),
         ('key1', 'default_value1', None, 'Empty-KeyValuePair-ReplacementValue'),
         ('key2', 'Blue', None, 'NO-COLOR-DEFINED'),
         ('key3', 'Blue', None, 'NO-COLOR-DEFINED'),
      ])


.. lconf-example::

   .. code-block:: lconf

      ___SECTION :: Example LCONF `Key :: Value Pairs` items
      # Comment-Line: Root/Main key value pair
      key1 :: value1
      key2 ::
      key3 ::
      ___END

   # using **a transform function and with `Empty-KeyValuePair-ReplacementValue`**

   .. code-block:: python3

      example_lconf_template = Root([
         ('#1', '# Comment Root/Main key value pair - with transform function - with `Empty-KeyValuePair-ReplacementValue`'),
         ('key1', 'default_value1', transform_function, 'Empty-KeyValuePair-ReplacementValue'),
         # Comment-Line: in the case below: if `key2` is in the `LCONF source` set to empty: the parsed lconf obj will have
         # the `Empty-KeyValuePair-ReplacementValue` -1
         ('key2', 500, lconf_to_int, -1),
         # Comment-Line: in the case below: if `key3` is by default empty: the parsed lconf obj will have
         #     the `Empty-KeyValuePair-ReplacementValue` -1 except the `LCONF source` to be parsed has set it to something
         ('key3', '', lconf_to_float, -999.4),
      ])


.. index:: Usage; LCONF: `Default Comments`

LCONF `Default Comments`
------------------------
`Default-Comments` are implemented in the `LCONF-Default-Template-Structure` like `Key :: Value Pairs` items but are special:

Key and value must start with an `one number sign` **#**

   - usually the keys are just incremented numbers to make them unique

.. code-block:: python3

   example_lconf_template = Root([
      ('#1', '# Comment this is a `Default Comment Line` which can be emitted'),
      ('key1', 'default_value1'),
      ('#2', '# this is another `Default Comment Line` which can be emitted'),
      ('key2', 'default_value1'),
   ])


LCONF `Default Comments`
````````````````````````
Key must start with an `one number sign` **#**

   - usually the keys are just incremented numbers to make them unique

The Value must be an empty string.

.. code-block:: python3

   example_lconf_template = Root([
      # Comment below is an `Empty default Comment Line` which can be emitted
      ('#1', ''),
      ('key1', 'default_value1'),
      # Comment below is another `Empty default Comment Line` which can be emitted
      ('#2', ''),
      ('key2', 'default_value1'),
   ])


Classes
=======
.. autoclass:: Blk
   :members: set_class__dict__item

.. autoclass:: BlkI
   :members: set_class__dict__item

.. autoclass:: KVList
   :members: set_class__dict__item

.. autoclass:: KVMap
   :members: set_class__dict__item

.. autoclass:: Root
   :members: set_class__dict__item, frompickle

.. autoclass:: ListOT
   :members: set_class__dict__item, replace_column_names, this_column_values


   ..note:: after the initialization all of them are unchangeable: except some: extra_data

"""
from pickle import (
   loads as ploads
)

from LCONF.utils import (
   Err,
   MethodDeactivatedErr
)


# noinspection PyUnusedLocal
def _deactivated(*args, **kwargs):
   """ Helper: used to raise MethodDeactivatedErr

   :param args:
   :param kwargs:
   :raise MethodDeactivatedErr:
   """
   raise MethodDeactivatedErr()


# === === === `LCONF-Default-Template-Structure` Classes === === === #
class Blk(dict):
   """ (Blk)Block Class: LCONF-Default-Template-Structure `Block-Name` class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order as initialized inclusive `Default-Comment/Empty Lines`
      - :attr:`key_order_no_comments` (list) the keys in order as initialized exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

   :param key_value_list: (list) of tuples: FORMAT: (key, value)
   :raise Err:
   """

   # noinspection PyTypeChecker
   def __init__(self, key_value_list):
      """ Constructor
      """
      if key_value_list.__class__ is list:
         dict.__init__(self, {key_value_tuple[0]: key_value_tuple[1:] for key_value_tuple in key_value_list})
         _temp_key_order = [item[0] for item in key_value_list]
         self.__dict__['key_order'] = _temp_key_order
         self.__dict__['key_order_no_comments'] = [key for key in _temp_key_order if key[0] != '#']
         self.__dict__['key_empty_replacementvalue'] = {key_value_tuple[0]: key_value_tuple[3] for key_value_tuple in
            key_value_list if len(key_value_tuple) > 3}
      else:
         raise Err('Blk.__init__()', [
            'key_value_list must be a list of key/value pairs: We got type: <{}>'.format(type(key_value_list)),
            '   <{}>'.format(key_value_list)
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self],), self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class BlkI(dict):
   """ (Blk)Block (I)dentifier Class: LCONF-Default-Template-Structure `Repeated-Block-Identifier` class

   **Has additional attributes**:

      - :attr:`min_required_blocks` (int)
      - :attr:`max_allowed_blocks` (int)

   :param min_required_blocks: (int) number of minimum required blocks when a `LCONF text/source` is parsed`

      - 0 or greater

      - to not define it: set it to -1

   :param max_allowed_blocks: (int) number of maximum required blocks when a `LCONF text/source` is parsed`

      - 1 or greater

      - to not define it: set it to -1

   :param dummy_blk_obj: (Blk obj) the defaults for any Block
   :raise Err:
   """

   # noinspection PyTypeChecker
   def __init__(self, min_required_blocks, max_allowed_blocks, dummy_blk_obj):
      """ Constructor
      """
      if dummy_blk_obj.__class__ is Blk:
         if dummy_blk_obj:
            if min_required_blocks < -1:
               raise Err('BlkI.__init__()', ['min_required_blocks: <{}> must be -1 or greater'.format(min_required_blocks)])
            if max_allowed_blocks < -1 or max_allowed_blocks == 0:
               raise Err('BlkI.__init__()', [
                  'max_allowed_blocks: <{}> must be -1 or greater than 0'.format(max_allowed_blocks)
               ])
            dict.__init__(self, {'dummy_blk': dummy_blk_obj})
            self.__dict__['min_required_blocks'] = min_required_blocks
            self.__dict__['max_allowed_blocks'] = max_allowed_blocks
         else:
            raise Err('BlkI.__init__()', [
               'dummy_blk_obj may not be empty: We got type: <{}>'.format(dummy_blk_obj),
               '   <{}>'.format(type(dummy_blk_obj))
            ])
      else:
         raise Err('BlkI.__init__()', [
            'dummy_blk_obj must be a `Blk obj`: We got type: <{}>'.format(type(dummy_blk_obj)),
            '   <{}>'.format(type(dummy_blk_obj))
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self],), self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class KVList(list):
   """ (K)ey(V)alueList Class: LCONF-Default-Template-Structure `Key :: Value-List` and `Key-Value-List` class

   **Has additional attributes**:

      - :attr:`use_oneline` (bool) will be initialized: default option to emit it as oneline or multiline list

         - useful in case the list has many default values or very long values

   :param use_oneline: (bool)

      - Set it to True: if the default list should be a oneline list `Key :: Value-List`
      - Set it to False: if the default list should be a multiline list `Key-Value-List`
   :param list_of_items: (list)
   :raise Err:
   """

   # noinspection PyTypeChecker
   def __init__(self, use_oneline, list_of_items):
      """ Constructor
      """
      if list_of_items.__class__ is list:
         list.__init__(self, list_of_items)
         self.__dict__['use_oneline'] = use_oneline
      else:
         raise Err('KVList.__init__()', [
            'list_of_items must be a list: We got type: <{}>'.format(type(list_of_items)),
            '   <{}>'.format(list_of_items)
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   append = _deactivated
   extend = _deactivated
   insert = _deactivated
   pop = _deactivated
   remove = _deactivated


class KVMap(dict):
   """ (K)ey(V)alue(Map)ping Class: LCONF-Default-Template-Structure `Key-Value-Mappings` class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order as initialized inclusive `Default-Comment/Empty Lines`
      - :attr:`key_order_no_comments` (list) the keys in order as initialized exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

   :param key_value_list: (list) of tuples: FORMAT: (key, value)

         - may not be empty
   """

   # noinspection PyTypeChecker
   def __init__(self, key_value_list):
      """ Constructor
      """
      if key_value_list.__class__ is list:
         if key_value_list:
            dict.__init__(self, {key_value_tuple[0]: key_value_tuple[1:] for key_value_tuple in key_value_list})
            _temp_key_order = [item[0] for item in key_value_list]
            self.__dict__['key_order'] = _temp_key_order
            self.__dict__['key_order_no_comments'] = [key for key in _temp_key_order if key[0] != '#']
            self.__dict__['key_empty_replacementvalue'] = {key_value_tuple[0]: key_value_tuple[3] for key_value_tuple in
               key_value_list if len(key_value_tuple) > 3}
         else:
            raise Err('KVMap.__init__()', [
               'key_value_list must be a list of key/value pairs and can not be Empty: We got type: <{}>'.format(
                  type(key_value_list)
               ),
               '   <{}>'.format(key_value_list)
            ])
      else:
         raise Err('KVMap.__init__()', [
            'key_value_list must be a list of key/value pairs: We got type: <{}>'.format(type(key_value_list)),
            '   <{}>'.format(key_value_list)
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self],), self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class Root(dict):
   """ (M)ain/Root Class: LCONF-Default-Template-Structure Main/Root obj class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order as initialized inclusive `Default-Comment/Empty Lines`
      - :attr:`key_order_no_comments` (list) the keys in order as initialized exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

   :param key_value_list: (list) of tuples: FORMAT: (key, value)
   :raise Err:
   """

   # noinspection PyTypeChecker
   def __init__(self, key_value_list):
      """ Constructor
      """
      if key_value_list.__class__ is list:
         dict.__init__(self, {key_value_tuple[0]: key_value_tuple[1:] for key_value_tuple in key_value_list})
         _temp_key_order = [item[0] for item in key_value_list]
         self.__dict__['key_order'] = _temp_key_order
         self.__dict__['key_order_no_comments'] = [key for key in _temp_key_order if key[0] != '#']
         self.__dict__['key_empty_replacementvalue'] = {key_value_tuple[0]: key_value_tuple[3] for key_value_tuple in
            key_value_list if len(key_value_tuple) > 3}
      else:
         raise Err('Root.__init__()', [
            'key_value_list must be a list of key/value pairs: We got type: <{}>'.format(type(key_value_list), ),
            '   <{}>'.format(key_value_list)
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self],), self.__dict__.copy())

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Root` from a pickled dumps.

      :param in_pickle_dumps: (bytes) a pickled `Root` dumps
      :return: (obj) a new Root object
      :raise Err:
      """
      new_obj = ploads(in_pickle_dumps)
      if new_obj.__class__ is Root:
         return new_obj
      else:
         raise Err('Root.frompickle()', [
            'Error: `in_pickle_dumps` does not seem to be a `Root` object: Got type: <{}>'.format(type(new_obj))
         ])

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class ListOT(list):
   """ List(O)f(T)uples Class: LCONF-Default-Template-Structure `List-Of-Tuples` class

   Tuple items (rows) should only be simple objects: no nested list, dictionary ect..

   .. note:: to replace column_names use the :py:meth:`replace_column_names` as it also updates related things

   **Has additional attributes**:

      - :attr:`column_names` (tuple): will be initialized: with column_names

      - :attr:`column_names_idx_lookup` (dict): will be initialized: column_name, to tuple_idx mapping

      - :attr:`column_names_counted` (int): will be initialized: with the number of column_names

      - :attr:`column_replace_missing` (tuple)

   :param column_names: (tuple) strings of column names: must be unique names
   :param list_of_tuples: (list) items (tuples - rows) must have the same number of values as there are column_names
   :param column_replace_missing: (tuple)

      - if not empty: then for each column one replacement value must be defined
         these are values which will replace missing column items

      .. note:: this will ALSO run through any transform functions: values must be type string

   :raise Err:
   """

   # noinspection PyTypeChecker,PyUnresolvedReferences
   def __init__(self, column_names, list_of_tuples, column_replace_missing=()):
      """ Constructor
      """
      if list_of_tuples.__class__ is list:
         if column_names.__class__ is tuple:
            list.__init__(self, list_of_tuples)
            self.__dict__['column_names'] = column_names
            self.__dict__['column_names_idx_lookup'] = {key: idx for idx, key in enumerate(column_names)}
            self.__dict__['column_names_counted'] = len(column_names)
            self.__dict__['column_replace_missing'] = column_replace_missing
            if column_replace_missing:
               if column_replace_missing.__class__ is tuple:
                  if len(column_replace_missing) != self.column_names_counted:
                     raise Err('ListOT.__init__()', [
                        '`column_replace_missing` must be an empty or have the same number of values as column_names.',
                        '    column_replace_missing items: <{}>  column_names items: <{}>'.format(
                           len(column_replace_missing),
                           len(column_names)
                        ),
                        '      column_replace_missing: <{}>'.format(column_replace_missing),
                        '      column_names: <{}>'.format(column_names)
                     ])
               else:
                  raise Err('ListOT.__init__()', [
                     'column_replace_missing must be a tuple: We got type: <{}>'.format(type(column_replace_missing)),
                     '   <{}>'.format(column_replace_missing)
                  ])
            # Check unique names
            if len(self.column_names_idx_lookup) != self.column_names_counted:
               raise Err('ListOT.__init__()', [
                  'All column names are not unique: Problems: <{}>'.format(self._helper_find_duplicates(column_names)),
                  '   column_names: <{}>'.format(column_names)
               ])
         else:
            raise Err('ListOT.__init__()', [
               'column_names must be a tuple: We got type: <{}>'.format(type(column_names)),
               '   <{}>'.format(column_names)
            ])
      else:
         raise Err('ListOT.__init__()', [
            'list_of_tuples must be a `list of tuples`: We got type: <{}>'.format(type(list_of_tuples)),
            '   <{}>'.format(list_of_tuples)
         ])

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   @staticmethod
   def _helper_find_duplicates(seq):
      """ Helper Returns a list of duplicates

      :param seq: (sequence)
      :return: (set) seen_twice
      """
      seen = {}
      seen_twice = {}
      for item in seq:
         if item in seen:
            seen_twice[item] = None
         else:
            seen[item] = None
      return seen_twice.keys()

   # noinspection PyUnresolvedReferences
   def replace_column_names(self, new_column_names_tuple):
      """ Replaces the `column_names (tuple)` with the new_column_names_tuple

      :param new_column_names_tuple: (tuple) must have the same number of names as the current `column_names`
      :raise Err:
      """
      if new_column_names_tuple.__class__ is tuple:
         if len(new_column_names_tuple) == self.column_names_counted:
            self.__dict__['column_names'] = new_column_names_tuple
            self.__dict__['column_names_idx_lookup'] = {key: idx for idx, key in enumerate(new_column_names_tuple)}
            # Check unique names
            if len(self.column_names_idx_lookup) != self.column_names_counted:
               raise Err('ListOT.replace_column_names()', [
                  'All column names are not unique: Problems: <{}>'.format(
                     self._helper_find_duplicates(new_column_names_tuple)
                  ),
                  '   new_column_names_tuple: <{}>'.format(new_column_names_tuple)
               ])
         else:
            raise Err('ListOT.replace_column_names()', [
               'new_column_names: <{}> must be the same number as column_names_counted: <{}>'.format(
                  len(new_column_names_tuple),
                  self.column_names_counted,
               ),
               '   <{}>'.format(new_column_names_tuple)
            ])
      else:
         raise Err('ListOT.replace_column_names()', [
            'new_column_names_tuple must be a <tuple> with: <{}> column_names: We got type: <{}>'.format(
               new_column_names_tuple,
               type(new_column_names_tuple)
            ),
            '   <{}>'.format(new_column_names_tuple)
         ])

   # noinspection PyUnresolvedReferences
   def this_column_values(self, column_name):
      """ Returns the items of all rows for the column

      :param column_name: (string)
      :return: (list) all items of the column for all rows
      :raise Err:
      """
      if column_name in self.column_names:
         idx = self.column_names_idx_lookup[column_name]
         return [row[idx] for row in self]
      else:
         raise Err('ListOT.this_column_values()', [
            'column_name: <{}> is not a valid one.'.format(column_name),
            '   Registered names: <{}>'.format(self.column_names)
         ])

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   __setitem__ = _deactivated
   __setattr__ = _deactivated
   append = _deactivated
   extend = _deactivated
   insert = _deactivated
   pop = _deactivated
   remove = _deactivated
