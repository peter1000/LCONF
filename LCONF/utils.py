"""
===============
LCONF.utils
===============

Overview
========
This module defines a couple of helpers.


Classes
=======
.. autoclass:: Err

.. autoclass:: MethodDeactivatedErr


Functions
=========
.. autofunction:: build_cython_extension

"""
from distutils.dist import Distribution
from distutils.errors import DistutilsArgError
from distutils.extension import Extension
from os.path import (
   basename as path_basename,
   dirname as path_dirname,
   splitext as path_splitext,
   join as path_join,
)

from Cython.Distutils import build_ext as cython_build_ext

from LCONF import TESTED_HOST_OS


class Err(Exception):
   """ Prints an own raised Project Error

   :param error_type: (str) to specify mostly from which part the error comes: e.g. CONFIG
   :param info: (list) list of strings (text info) to print as message: each list item starts at a new line
   """

   def __init__(self, error_type, info):
      """ Constructor.
      """
      Exception.__init__(self, error_type, info)
      self.__error_type = error_type
      self.__info = '\n'.join(info)
      self.__txt = '''

========================================================================
LCONF-{} ERROR:


  {}

This `LCONF` was tested with:
  HOST OS: {}
========================================================================

'''.format(self.__error_type, self.__info, TESTED_HOST_OS)
      print(self.__txt)


# ===========================================================================================================================
# public helpers
# ===========================================================================================================================
def build_cython_extension(py_or_pyx_file_path, cython_force_rebuild=True):
   """ Build a cython extension from a `.py` or `.pyx` file

   - build will be done in a sub-folder named `_pyxbld` in the py_or_pyx_file_path

   :param py_or_pyx_file_path: (str) path to a `.py` or `.pyx` file
   :param cython_force_rebuild: (bool) If True the cython extension is rebuild even if it was already build
   :return: (tuple) cython_extension_module_path, cython_module_c_file_path, cython_build_dir_path
   """
   module_dir = path_dirname(py_or_pyx_file_path)
   module__cython_name = path_splitext(path_basename(py_or_pyx_file_path))[0]
   cython_module_c_file_path = path_join(module_dir, module__cython_name + '.c')
   cython_build_dir_path = path_join(module_dir, '_pyxbld')

   args = ['--quiet', 'build_ext', '--build-lib', module_dir]
   if cython_force_rebuild:
      args.append('--force')
   dist = Distribution({'script_name': None, 'script_args': args})
   dist.ext_modules = [Extension(name=module__cython_name, sources=[py_or_pyx_file_path])]
   dist.cmdclass = {'build_ext': cython_build_ext}
   build = dist.get_command_obj('build')
   build.build_base = cython_build_dir_path

   try:
      dist.parse_command_line()
   except DistutilsArgError as err:
      raise Err('utils.build_cython_extension', [
         'py_or_pyx_file_path: <{}>'.format(py_or_pyx_file_path),
         '  DistutilsArgError: <{}>'.format(err)
      ])

   try:
      obj_build_ext = dist.get_command_obj('build_ext')
      dist.run_commands()
      cython_extension_module_path = obj_build_ext.get_outputs()[0]
      if path_dirname(py_or_pyx_file_path) != module_dir:
         raise Err('utils.build_cython_extension', [
            'py_or_pyx_file_path: <{}>'.format(py_or_pyx_file_path),
            '  <module_dir> differs from final <cython_module_dir>',
            '   module_dir: <{}>'.format(module_dir),
            '   cython_module_dir: <{}>'.format(path_dirname(py_or_pyx_file_path))
         ])
   except Exception as err:
      raise Err('utils.build_cython_extension', [
         'py_or_pyx_file_path: <{}>'.format(py_or_pyx_file_path),
         '  Exception: <{}>'.format(err)
      ])

   return cython_extension_module_path, cython_module_c_file_path, cython_build_dir_path


class MethodDeactivatedErr(Exception):
   """ Prints an own raised Deactivated Err
   """

   def __init__(self):
      """ Constructor.
      """
      Exception.__init__(self, 'Method is deactivated.')
      self.__txt = '''

========================================================================
LCONF-MethodDeactivated ERROR:


  Method is deactivated.

========================================================================

'''
      print(self.__txt)
