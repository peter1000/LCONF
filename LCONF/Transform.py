""" TypeConversion for casting
"""
from datetime import datetime
from os.path import (
   abspath,
   expanduser
)
from LCONF.ProjectErr import Err


def lconf_to_bool(bool_str, extra_err_info):
   """ Return `python True or False` for the input bool_str

   Args:
      lconf_to_bool (str): must be any of: True, true, False, false
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      bool: conversion of the input int_str
   """
   if bool_str == 'True' or bool_str == 'true':
      return True
   elif bool_str == 'False' or bool_str == 'false':
      return False
   raise Err('bool_str', 'bool_str must be any of: True, true, False, false.  We got: <{}>\n    extra_err_info: {}'.format(bool_str, extra_err_info))


def lconf_to_int(int_str, extra_err_info):
   """ Return an integer of the input int_str

   Args:
      int_str (str): string of a number must contain only digits plus optional a leading - (minus sign)
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      int: conversion of the input int_str
   """
   # check leading -
   if int_str[0] == '-':
      if int_str[1:].isdigit():
         return int(int_str)
   elif int_str.isdigit():
      return int(int_str)
   raise Err('int_str', 'int_str must contain only digits plus optional a leading - (minus sign):  We got: <{}>\n    extra_err_info: {}'.format(int_str, extra_err_info))


def lconf_to_float(float_str, extra_err_info):
   """ Return a float of the input float_str

   Args:
      float_str (str): string of a number: must contain only digits and exact 1 dot plus optional a leading - (minus sign)
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      float: conversion of the input float_str
   """
   if '.' in float_str:
      before_dot, after_dot = float_str.split('.', 1)
      # check leading -
      if before_dot[0] == '-':
         if before_dot[1:].isdigit() and after_dot.isdigit():
            return float(float_str)
      elif before_dot.isdigit() and after_dot.isdigit():
         return float(float_str)
   raise Err('float_str', 'float_str must contain only digits and exact 1 dot plus optional a leading - (minus sign):  We got: <{}>\n    extra_err_info: {}'.format(float_str, extra_err_info))


def lconf_to_number(number_str, extra_err_info):
   """ Return a float of the input number_str

   Args:
      number_str (str): string of a number: only digits and maximum one dot allowed plus optional a leading - (minus sign)
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      float: conversion of the input number_str
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
   raise Err('lconf_to_number', 'number_str must contain only digits and maximum 1 dot plus optional a leading - (minus sign):  We got: <{}>\n    extra_err_info: {}'.format(number_str, extra_err_info))


def lconf_to_pathexpanduser(path_str, extra_err_info):
   """ Return a path string if it starts with `~` expanduser else return it unchanged

   Args:
      path_str (str): string of a path which must start with `~` or `/`
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      str: if input starts with `~` expanduser else return it unchanged
   """
   # must start with ~ or /
   if path_str[0] == '/' or path_str[0] == '~':
      return abspath(expanduser(path_str))

   raise Err('lconf_to_pathexpanduser', 'path_str must start with <~> or </>:  We got: <{}>\n    extra_err_info: {}'.format(path_str, extra_err_info))


def lconf_to_datetime(date_str, extra_err_info):
   """ Return a python datetime of the input date_str

   Args:
      date_str (str): string of a datetime: format: 16 character long: `YYYY-MM-DD-hh:mm`
         * e.g. `2014-05-08-13:39`
      extra_err_info (str): any additional info which will be printed if an error is raised: e.g line number, original line ect..

   Returns:
      datetime: conversion of the input date_str
   """
   try:
      return datetime.strptime(date_str, '%Y-%m-%d-%H:%M')
   except:
      raise Err('lconf_to_datetime', 'date_str must be in the format: 16 character long: `YYYY-MM-DD-hh:mm`.  We got: <{}>\n    extra_err_info: {}'.format(date_str, extra_err_info))
