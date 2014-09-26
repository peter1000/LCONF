"""
===============
LCONF.transform
===============

Overview
========
This module provides ready Transform and TypeConversion functions for casting.

.. seealso:: :ref:`Value Transformation <value-transformation>`

.. todo::

   maybe change code for `lconf_to_float`, `lconf_to_number` to use python float to validate


Functions
=========
.. autofunction:: lconf_to_bool
.. autofunction:: lconf_to_int
.. autofunction:: lconf_to_float
.. autofunction:: lconf_to_number
.. autofunction:: lconf_to_pathexpanduser
.. autofunction:: lconf_to_datetime

"""
from datetime import datetime
from os.path import (
   abspath as path_abspath,
   expanduser as path_expanduser
)

from LCONF.utils import Err


def lconf_to_bool(bool_str, extra_err_info):
   """ Return `python True or False` for the input bool_str

   :param bool_str: (str) must be any of: True, true, False, false
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (bool) conversion of the input int_str
   :raise Err:
   """
   if bool_str == 'True' or bool_str == 'true':
      return True
   elif bool_str == 'False' or bool_str == 'false':
      return False
   raise Err('bool_str', [
      'bool_str must be any of: True, true, False, false.  We got: <{}>'.format(bool_str),
      '    extra_err_info: {}'.format(extra_err_info)
   ])


def lconf_to_int(int_str, extra_err_info):
   """ Return an integer of the input int_str

   :param int_str: (str) string of a number must contain only digits plus optional a leading - (minus sign)
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (int)conversion of the input int_str
   :raise Err:
   """
   # check leading -
   if int_str[0] == '-':
      if int_str[1:].isdigit():
         return int(int_str)
   elif int_str.isdigit():
      return int(int_str)
   raise Err('int_str', [
      'int_str must contain only digits plus optional a leading - (minus sign).  We got: <{}>'.format(int_str),
      '    extra_err_info: {}'.format(extra_err_info)
   ])


def lconf_to_float(float_str, extra_err_info):
   """ Return a float of the input float_str

   :param float_str: (str) string of a number: must contain only digits and exact 1 dot plus optional a leading - (minus
      sign)
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (float) conversion of the input float_str
   :raise Err:
   """
   if '.' in float_str:
      before_dot, after_dot = float_str.split('.', 1)
      # check leading -
      if before_dot[0] == '-':
         if before_dot[1:].isdigit() and after_dot.isdigit():
            return float(float_str)
      elif before_dot.isdigit() and after_dot.isdigit():
         return float(float_str)
   raise Err('float_str', [
      'float_str must contain only digits and exact 1 dot plus optional a leading - (minus sign).  We got: <{}>'.format(
         float_str
      ),
      '    extra_err_info: {}'.format(extra_err_info)
   ])


def lconf_to_number(number_str, extra_err_info):
   """ Return a float of the input number_str

   :param number_str: (str) string of a number: only digits and maximum one dot plus optional a leading - (minus sign)
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (float) conversion of the input number_str
   :raise Err:
   """
   # check leading -
   if number_str[0] == '-':
      tmp_number_str = number_str[1:]
   else:
      tmp_number_str = number_str

   if tmp_number_str.isdigit():
      return float(number_str)
   elif '.' in tmp_number_str:
      before_dot, after_dot = tmp_number_str.split('.', 1)
      if before_dot.isdigit() and after_dot.isdigit():
         return float(number_str)
   raise Err('lconf_to_number', [
      'number_str must contain only digits and maximum 1 dot plus optional a leading - (minus sign).  We got: <{}>'.format(
         lconf_to_number
      ),
      '    extra_err_info: {}'.format(extra_err_info)
   ])


def lconf_to_pathexpanduser(path_str, extra_err_info):
   """ Return a path string if it starts with `~` expanduser else return it unchanged

   :param path_str: (str) string of a path which must start with `~` or `/`
   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (str) if input starts with `~` expanduser else return it unchanged
   :raise Err:
   """
   # must start with ~ or /
   if path_str[0] == '/' or path_str[0] == '~':
      return path_abspath(path_expanduser(path_str))

   raise Err('lconf_to_pathexpanduser', [
      'path_str must start with <~> or </>.  We got: <{}>'.format(lconf_to_pathexpanduser),
      '    extra_err_info: {}'.format(extra_err_info)
   ])


def lconf_to_datetime(date_str, extra_err_info):
   """ Return a python datetime of the input date_str

   :param date_str: (str) string of a datetime: format:

         16 character long: `YYYY-MM-DD hh:mm`     e.g. `2014-05-08 13:39`
         19 character long: `YYYY-MM-DD hh:mm:ss`  e.g. `2014-05-08 13:39:00`

   :param extra_err_info: (str) any additional info which will be printed if an error is raised: e.g line number, original
      line ect..

   :return: (datetime) conversion of the input date_str
   :raise Err:
   """
   date_str_len = len(date_str)
   if date_str_len == 16:
      try:
         return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
      except:
         raise Err('lconf_to_datetime', [
            'date_str must be in the format: 16 character long: `YYYY-MM-DD hh:mm`',
            'OR: 19 character long: `YYYY-MM-DD hh:mm:ss`',
            '  We got: date_str_len: <{}> date_str: <{}>'.format(date_str_len, date_str),
            '    extra_err_info: {}'.format(extra_err_info)
         ])
   elif date_str_len == 19:
      try:
         return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
      except:
         raise Err('lconf_to_datetime', [
            'date_str must be in the format: 16 character long: `YYYY-MM-DD hh:mm`',
            'OR: 19 character long: `YYYY-MM-DD hh:mm:ss`',
            '  We got: date_str_len: <{}> date_str: <{}>'.format(date_str_len, date_str),
            '    extra_err_info: {}'.format(extra_err_info)
         ])
   else:
      raise Err('lconf_to_datetime', [
         'date_str must be in the format: 16 character long: `YYYY-MM-DD hh:mm`',
         'OR: 19 character long: `YYYY-MM-DD hh:mm:ss`',
         '  We got: date_str_len: <{}> date_str: <{}>'.format(date_str_len, date_str),
         '    extra_err_info: {}'.format(extra_err_info)
      ])
