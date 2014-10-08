"""
===================
LCONF.lconf_classes
===================

Overview
========
Most of this code is based on the `ReOBJ package <https://github.com/peter1000/ReOBJ>`_. see `LICENSE` for more info

These Classes are used for the final default/parsed LCONF object.

.. note:: after the initialization all of them are in some ways changeable

   - some allow also adding new keys, appending items

Classes
=======
.. autoclass:: LconfBlk
   :members: set_class__dict__item

.. autoclass:: LconfBlkI
   :members: __setitem__, set_class__dict__item

.. autoclass:: LconfKVList
   :members: set_class__dict__item

.. autoclass:: LconfKVMap
   :members: set_class__dict__item

.. autoclass:: LconfRoot
   :members: set_class__dict__item, frompickle

.. autoclass:: LconfListOT
   :members: set_class__dict__item, replace_column_names, this_column_values

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


# ===========================================================================================================================
# `Normal LCONF` Classes
# ===========================================================================================================================
class LconfBlk(dict):
   """ (Blk)Block Class: LCONF `Block-Name` class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order but exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

           This is needed for :py:func:`LCONF.main_code.lconf_emit` to check if `empty_key_value_pair` is True

   :param data: (dict)
   :param key_order_list: (list) ordered data dictionary keys but exclusive `Default-Comment/Empty Lines`
   :param key_empty_replacementvalue: (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`
   """

   # noinspection PyTypeChecker
   def __init__(self, data, key_order_list, key_empty_replacementvalue):
      """ Constructor
      """
      dict.__init__(self, data)
      self.__dict__['key_order'] = key_order_list
      self.__dict__['key_empty_replacementvalue'] = key_empty_replacementvalue

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses,PyUnresolvedReferences
   def __reduce__(self):
      """ Return state information for pickling

      :return: state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self], self.key_order,), self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   # __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class LconfBlkI(dict):
   """ (Blk)Block (I)dentifier Class: LCONF `Repeated-Block-Identifier` class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys (block_names) in order as added - see param :py:attr:`block_names_list`
      - :attr:`min_required_blocks` (int) - see param :py:attr:`min_required_blocks`
      - :attr:`max_allowed_blocks` (int) - see param :py:attr:`max_allowed_blocks`
      - :attr:`has_comments` (bool): defaults to False

         - this must be set to True: if it is init with comments: this is needed when a Blk is prepared

   :param data: (dict)
   :param block_names_list: (list)
   :param min_required_blocks: (int) number of minimum required blocks when a `LCONF text/source` is parsed`

      - 0 or greater

      - to not define it: set it to -1

   :param max_allowed_blocks: (int) number of maximum required blocks when a `LCONF text/source` is parsed`

      - 1 or greater

      - to not define it: set it to -1

   """

   # noinspection PyTypeChecker
   def __init__(self, data, block_names_list, min_required_blocks, max_allowed_blocks):
      """ Constructor
      """
      dict.__init__(self, data)
      self.__dict__['key_order'] = block_names_list
      self.__dict__['min_required_blocks'] = min_required_blocks
      self.__dict__['max_allowed_blocks'] = max_allowed_blocks
      self.__dict__['has_comments'] = False

   # noinspection PyUnresolvedReferences
   def __setitem__(self, block_name, blk_obj):
      """ Called to implement assignment to self[key]. If `block_name` is not in `key_order` it will be added.

      :param block_name:
      :param blk_obj:
      """
      if block_name not in self:
         self.key_order.append(block_name)
      dict.__setitem__(self, block_name, blk_obj)

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyUnresolvedReferences
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__,
      ([(key, self[key]) for key in self], self.key_order, self.min_required_blocks, self.max_allowed_blocks,),
      self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   # __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class LconfKVList(list):
   """ (K)ey(V)alueList Class: LCONF `Key :: Value-List` and `Key-Value-List` class

   **Has additional attributes**:

      - :attr:`use_oneline` (bool) will be initialized: default option to emit it as oneline or multiline list

         - useful in case the list has many default values or very long values

   :param data: (list)
   :param use_oneline: (bool)

      - Set it to True: if the default list should be a oneline list `Key :: Value-List`
      - Set it to False: if the default list should be a multiline list `Key-Value-List`
   """

   # noinspection PyTypeChecker
   def __init__(self, data, use_oneline):
      """ Constructor
      """
      list.__init__(self, data)
      self.__dict__['use_oneline'] = use_oneline

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
   # append = _deactivated
   extend = _deactivated
   insert = _deactivated
   pop = _deactivated
   remove = _deactivated


class LconfKVMap(dict):
   """ (K)ey(V)alue(Map)ping Class: LCONF `Key-Value-Mappings` class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order but exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

           This is needed for :py:func:`LCONF.main_code.lconf_emit` to check if `empty_key_value_pair` is True

   :param data: (dict)
   :param key_order_list: (list) ordered data dictionary keys but exclusive `Default-Comment/Empty Lines`
   :param key_empty_replacementvalue: (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`
   """

   # noinspection PyTypeChecker
   def __init__(self, data, key_order_list, key_empty_replacementvalue):
      """ Constructor
      """
      dict.__init__(self, data)
      self.__dict__['key_order'] = key_order_list
      self.__dict__['key_empty_replacementvalue'] = key_empty_replacementvalue

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses,PyUnresolvedReferences
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, ([(key, self[key]) for key in self], self.key_order.copy()), self.__dict__.copy())

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   # __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class LconfRoot(dict):
   """ Lconf(M)ain/Root Class: LCONF Main/LconfRoot obj class

   **Has additional attributes**:

      - :attr:`key_order` (list) the keys in order but exclusive `Default-Comment/Empty Lines`
      - :attr:`key_empty_replacementvalue` (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`

         - if :ref:`LCONF-Default-Template-Structure <lconf_default_template_structure>` defines an
           `Empty-KeyValuePair-ReplacementValue` then the key is added with the `Empty-KeyValuePair-ReplacementValue`

           This is needed for :py:func:`LCONF.main_code.lconf_emit` to check if `empty_key_value_pair` is True

      - :attr:`section_name` (str) defaults to 'missing section name'
      - :attr:`is_parsed` (bool) defaults to False
      - :attr:`has_comments` (bool) defaults to False

         - this must be set to True: if it is init with comments: this helps that one does not need to check for comments
           later on

   :param data: (dict)
   :param key_order_list: (list) ordered data dictionary keys but exclusive `Default-Comment/Empty Lines`
   :param key_empty_replacementvalue: (dict) all keys which have `Empty-KeyValuePair-ReplacementValue`
   """

   # noinspection PyTypeChecker
   def __init__(self, data, key_order_list, key_empty_replacementvalue):
      """ Constructor
      """
      dict.__init__(self, data)
      self.__dict__['key_order'] = key_order_list
      self.__dict__['key_empty_replacementvalue'] = key_empty_replacementvalue
      self.__dict__['section_name'] = 'missing section name'
      self.__dict__['is_parsed'] = False
      self.__dict__['has_comments'] = False

   def set_class__dict__item(self, key, value):
      """ Sets the class __dict__: key to value: if key did not exist it is added

      :param key: (str)
      :param value: (any)
      """
      self.__dict__[key] = value

   # noinspection PyRedundantParentheses,PyUnresolvedReferences
   def __reduce__(self):
      """ Return state information for pickling
      """
      return (self.__class__, (
         [(key, self[key]) for key in self],
         self.key_order.copy(),
         self.key_empty_replacementvalue.copy()
      ),
      self.__dict__.copy()
      )


   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `LconfRoot` from a pickled dumps.

      :param in_pickle_dumps: (bytes) a pickled `LconfRoot` dumps
      :return: (obj) a new LconfRoot object
      :raise Err:
      """
      new_obj = ploads(in_pickle_dumps)
      if new_obj.__class__ is LconfRoot:
         return new_obj
      else:
         raise Err('LconfRoot.frompickle()', [
            'Error: `in_pickle_dumps` does not seem to be a `LconfRoot` object: Got type: <{}>'.format(type(new_obj))
         ])

   # DEACTIVATED
   clear = _deactivated
   copy = _deactivated
   __add__ = _deactivated
   __delattr__ = _deactivated
   __delitem__ = _deactivated
   # __setitem__ = _deactivated
   __setattr__ = _deactivated
   setdefault = _deactivated
   pop = _deactivated
   popitem = _deactivated
   update = _deactivated
   get = _deactivated
   fromkeys = _deactivated


class LconfListOT(list):
   """ List(O)f(T)uples Class: LCONF `List-Of-Tuples` class

   Tuple items (rows) should only be simple objects: no nested list, dictionary ect..

   .. note:: to replace column_names use the :py:meth:`replace_column_names` as it also updates related things

   **Has additional attributes**:

      - :attr:`column_names` (tuple): will be initialized: with column_names

      - :attr:`column_names_idx_lookup` (dict): will be initialized: column_name, to tuple_idx mapping

      - :attr:`column_names_counted` (int): will be initialized: with the number of column_names

      - :attr:`column_replace_missing` (tuple)

   :param data: list) items (tuples - rows) must have the same number of values as there are column_names
   :param column_names: (tuple) strings of column names: must be unique names
   :param column_names_idx_lookup: (dict) column_name, to tuple_idx mapping
   :param column_names_counted: (int) number of column_names
   :param column_replace_missing: (tuple)

      - if not empty: then for each column one replacement value must be defined
         these are values which will replace missing column items

      .. note:: this will ALSO run through any transform functions

   """

   # noinspection PyTypeChecker
   def __init__(self, data, column_names, column_names_idx_lookup, column_names_counted, column_replace_missing):
      """ Constructor
      """
      list.__init__(self, data)
      self.__dict__['column_names'] = column_names
      self.__dict__['column_names_idx_lookup'] = column_names_idx_lookup
      self.__dict__['column_names_counted'] = column_names_counted
      self.__dict__['column_replace_missing'] = column_replace_missing

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
               raise Err('LconfListOT.replace_column_names()', [
                  'All column names are not unique: Problems: <{}>'.format(
                     self._helper_find_duplicates(new_column_names_tuple)
                  ),
                  '   new_column_names_tuple: <{}>'.format(new_column_names_tuple)
               ])
         else:
            raise Err('LconfListOT.replace_column_names()', [
               'new_column_names: <{}> must be the same number as column_names_counted: <{}>'.format(
                  len(new_column_names_tuple),
                  self.column_names_counted,
               ),
               '   <{}>'.format(new_column_names_tuple)
            ])
      else:
         raise Err('LconfListOT.replace_column_names()', [
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
         raise Err('LconfListOT.this_column_values()', [
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
   # append = _deactivated
   extend = _deactivated
   insert = _deactivated
   pop = _deactivated
   remove = _deactivated
