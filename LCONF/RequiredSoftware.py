""" Checks for some Required, Optional/Recommended software

   **Module CONSTANTS:**
      SOFTWARE_PY `dict of tuples` - mapping of Required, Recommended python software package
         tuple format: (import package/module name, required boolean, minimum version, attribute access of version info)

            - minimum version: may only contain digits and dots

         if there is no valid attribute to check a version: define `minimum version` and `attribute access of version info` as an empty string

         Note: `python` itself is always required. Because it does not have an import package defined use an empty string
            Use as version info the output: version_info - (major=3, minor=3, micro=2) automatically done

         .. code-block:: python

            SOFTWARE_PY = {
               # Main Required Software
               'Python': ('', True, '3.4.0', ''),
               'Setuptools': ('setuptools', True, '3.4.4', '__version__'),
               # Additional Required Software
               'Nose': ('nose', True, '1.3.1', '__version__'),
               'Sphinx': ('sphinx', True, '1.3a0', '__version__'),
               'sphinxcontrib-napoleon': ('sphinxcontrib', True, '', ''),
               # Additional Recommended Software
               'coverage': ('coverage', False, '3.7.1', '__version__'),
               'flake8': ('flake8', False, '2.1.0', '__version__'),
               'pylint': ('pylint.__pkginfo__', False, '1.2.0', 'version'),
               'retext': ('ReText', False, '4.1.2', 'app_version'),
            }

      SOFTWARE_EXECUTABLES_NONE_PY `dict` - of Required, Recommended none python software executable: no version checked:
         Value: (bool) if required true else false

            .. code-block:: python

               SOFTWARE_EXECUTABLES_NONE_PY = {'docker': True}

      EXECUTABLES_ADDITIONAL_SEARCH_PATHS `list` - of additional path to look for the program executable:
         if set this will be searched first before any other ones found in `os.getenv('PATH')`

         .. code-block:: python

            EXECUTABLES_ADDITIONAL_SEARCH_PATHS = ['/home/my_apps/bin']

"""
import importlib
import os
from os import getenv
from os.path import (
   isfile,
   join,
   pathsep,
   split
)
import sys
from sys import version_info


# ====================== ADJUST HERE
SOFTWARE_PY = {
   # Main Required Software
   'Python': ('', True, '3.4.1', ''),
   'Setuptools': ('setuptools', True, '5.1', '__version__'),
   'RDICT': ('RDICT', True, '3.0.0', '__version__'),
   # Additional Required Software
   'Nose': ('nose', True, '1.3.3', '__version__'),
   'coverage': ('coverage', True, '3.7.1', '__version__'),
   'Sphinx': ('sphinx', True, '1.2.2', '__version__'),
   'sphinxcontrib-napoleon': ('sphinxcontrib', True, '', ''),
   # Additional Recommended Software
   'SpeedIT': ('SpeedIT', False, '2.0.0', '__version__'),
   'flake8': ('flake8', False, '2.1.0', '__version__'),
   'psutil': ('psutil', False, '2.1.1', '__version__'),
   'pylint': ('pylint.__pkginfo__', False, '1.2.1', 'version'),
   'retext': ('ReText', False, '4.1.2', 'app_version'),
   'pyenchant': ('enchant', False, '1.6.6', '__version__'),
   'pip': ('pip', False, '1.5.6', '__version__'),
}

SOFTWARE_EXECUTABLES_NONE_PY = {}

EXECUTABLES_ADDITIONAL_SEARCH_PATHS = []


def which(program, additional_search_paths):
   """ Searches for an executable.   Based on: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python

   Args:
      program (str): executable(program) name
      additional_search_paths (list): a list of additional path to look for the program executable:
                                          if set this will be searched first before any other ones found in `os.getenv('PATH')`
   Returns:
      string: path to the executable(program) or an empty string ``''``
   """
   result = ''
   fpath = split(program)[0]
   if fpath:
      if isfile(program) and os.access(program, os.X_OK):
         result = program
   else:
      search_paths = additional_search_paths + getenv('PATH').split(pathsep)
      for path_ in search_paths:
         exe_file = join(path_.strip('"'), program)
         if isfile(exe_file) and os.access(exe_file, os.X_OK):
            result = exe_file
            break
   return result


def get_current_versions(software_py):
   """ Get the current py software versions

   Args:
      software_py (dict of tuples) mapping of Required, Optional/Recommended python software package: (import package name, minimum version, required boolean)

         - For an example `software_py` see: the module description at the top

   Returns:
      dict: mapping 'name' to current version or an empty string

         .. code-block:: python

            {'rope_py3k': '0.9.4-1',
            'Python': '',
            'pylint': '',
            'crazy': 'IMPORT_ERROR',
            }

   Raises:
      ImportError/AttributeError
   """
   return_version_dict = {}
   for name in software_py:
      import_name = software_py[name][0]
      required = software_py[name][1]
      min_version = software_py[name][2]
      access_attribute = software_py[name][3]

      current_version = ''
      return_version_dict[name] = ''

      # python itself is special as we do not import it
      if name.lower() == 'python':
         current_version = '{}.{}.{}'.format(version_info.major, version_info.minor, version_info.micro)
         print('\n======== name: <{}> current_version: <{}>\n     -> required: <{}>, expected min_version: <{}>'.format(name, current_version, required, min_version))
      else:
         try:
            module_ = importlib.import_module(import_name)
            if min_version and access_attribute:
               try:
                  current_version = getattr(module_, access_attribute)
                  print('\n======== name: <{}> current_version: <{}>\n     -> required: <{}>, expected min_version: <{}>'.format(name, current_version, required, min_version))
               except AttributeError:
                  sys.exit('\nCODE-ERROR: trying to use a notimplemented version attribute: original: {}, {})'.format(name, software_py[name]))
            else:
               print('\n======== name: <{}> current_version: <undefined>\n     -> required: <{}>, expected min_version: <{}>'.format(name, required, min_version))
         except ImportError:
            current_version = 'IMPORT_ERROR'

      return_version_dict[name] = current_version
   return return_version_dict


def check_min_required_version(version_string, min_required_version_string):
   """ Returns True if version_string fulfills the min_required_version requirement: this can be used for simple comparison

   This is a rough check: taking into account only all integers till the first none integer / none dot char is encountered

   .. code-block:: text

      version_string: `1.3a0` checks: `1.3`
      version_string: `0.9.4-1` checks: `9.4`
      version_string: `1.9.0` checks: `1.9.0`
      version_string: `3.2ab0.3-t` checks: `3.2`

   Args:
      version_string (str)
      min_required_version_string(str): may only contain digits and dots

   Returns:
      bool: True if the `version_string` is the same or higher than the `min_required_version_string` else False
   """
   # check min_required_version_string contains only integers and dots
   for char_ in min_required_version_string:
      if char_ not in '.0123456789':
         sys.exit('\nCODE-ERROR: min_required_version_string: <{}> may only contain digits and dots'.format(min_required_version_string))

   min_required_version_list = min_required_version_string.split('.')

   version_used_digits_str = ''
   for char_ in version_string:
      if char_ not in '.0123456789':
         break
      version_used_digits_str += char_

   if not version_used_digits_str:
      sys.exit('\nCODE-ERROR: Could not parse the version_string: <{}>'.format(version_string))

   version_used_digits_list = version_used_digits_str.split('.')

   # make sure they are the same length
   len_version_used_digits_list = len(version_used_digits_list)
   len_min_required_version_list = len(min_required_version_list)

   if len_min_required_version_list > len_version_used_digits_list:
      for missing in range(len_min_required_version_list - len_version_used_digits_list):
         version_used_digits_list.append('0')
   elif len_version_used_digits_list > len_min_required_version_list:
      for missing in range(len_version_used_digits_list - len_min_required_version_list):
         min_required_version_list.append('0')

   for cur_part, min_required_part in zip(version_used_digits_list, min_required_version_list):
      cur_part = int(cur_part)
      min_required_part = int(min_required_part)
      if cur_part > min_required_part:
         return True
      elif cur_part < min_required_part:
         return False

   return True


def check_python_software(software_py):
   """ Check required/recommended python software inclusive minimum version

   Args:
      software_py (dict of tuples) mapping of Required, Recommended python software package: tuple format: (import package name, required boolean, minimum version, attribute access of version info)

         - For an example `software_py` see: the module description at the top

   Returns:
      dict of dicts: only with problem results

         .. code-block:: python

            {'required': {'ImportName': 'xxx', 'MinimumVersion': min_version, 'CurrentVersion': current_version_dict[name]},
            'recommended': {'ImportName': 'xxx', 'MinimumVersion': min_version, 'CurrentVersion': current_version_dict[name]}}
   """
   result = {'required': {}, 'recommended': {}}
   current_version_dict = get_current_versions(software_py)
   found_python = False

   for name in software_py:
      got_problem = False

      import_name = software_py[name][0]
      required = software_py[name][1]
      min_version = software_py[name][2]
      # python itself is special
      if name.lower() == 'python':
         found_python = True
         if not required:
            sys.exit('\nCODE-ERROR: Python must always be defined as a required: software_py: {} {}'.format(name, software_py[name]))

      if current_version_dict[name] == 'IMPORT_ERROR':
         got_problem = True
      elif not current_version_dict[name]:
         if min_version:
            got_problem = True
      elif not check_min_required_version(current_version_dict[name], min_version):
         got_problem = True

      if got_problem:
         if required:
            result['required'][name] = {'ImportName': import_name, 'MinimumVersion': min_version, 'CurrentVersion': current_version_dict[name]}
         else:
            result['recommended'][name] = {'ImportName': import_name, 'MinimumVersion': min_version, 'CurrentVersion': current_version_dict[name]}

   if not found_python:
      sys.exit('\nCODE-ERROR: Python must always be defined as a required: software_py: {}'.format('   \n'.join(software_py)))

   return result


def check_programs_executable(software_executables_none_py, additional_search_paths):
   """ Check required/recommended none python software if executable can be found

   Args:
      software_executables_none_py (dict): of required none python software executable: no version checked:
         Value: (bool) if required true else false
      additional_search_paths (list): of additional path to look for the program executable:
         if set this will be searched first before any other ones found in `os.getenv('PATH')`

   Returns:
      dict of lists: only with problem results: names for which the executable could not be found

         .. code-block:: python

            {'required': [],
            'recommended': []}
   """
   result = {'required': [], 'recommended': []}
   for search_executable, required in software_executables_none_py.items():
      found_executable = which(search_executable, additional_search_paths)
      if not found_executable:
         if required:
            result['required'].append(search_executable)
         else:
            result['recommended'].append(search_executable)
   return result


def check_software(software_py, software_executables_none_py, additional_search_paths):
   """ Check required/recommended software per minimum version: prints missing once

   Args:
      software_py (dict of tuples) mapping of Required, Optional/Recommended python software package: (import package name, minimum version, required boolean)

         - For an example `software_py` see: the module description at the top

      software_executables_none_py (dict): of required none python software executable: no version checked:
         Value: (bool) if required true else false
      additional_search_paths (list): of additional path to look for the program executable:
         if set this will be searched first before any other ones found in `os.getenv('PATH')`
   """
   found_all_recommended = True
   result_software_py = check_python_software(software_py)
   result_executables_none_py = check_programs_executable(software_executables_none_py, additional_search_paths)

   # get_text_problem_py helper function
   def get_text_problem_py(problem_py_dict):
      """ Helper: get_text_problem_py
      """
      txt_ = ['   {}: ImportName: <{}> - MinimumVersion: <{}> - found CurrentVersion: <{}>'.format(key, problem_py_dict[key]['ImportName'], problem_py_dict[key]['MinimumVersion'], problem_py_dict[key]['CurrentVersion']) for key in problem_py_dict]
      return '\n'.join(txt_)

   # get_text_problem_executable helper function
   def get_text_problem_executable(problem_executable_list):
      """ Helper: get_text_problem_executable
      """
      txt_ = ['   <{}>: Executable could not be found.'.format(key) for key in problem_executable_list]
      return '\n'.join(txt_)

   if result_software_py['recommended'] and result_executables_none_py['recommended']:
      txt = get_text_problem_py(result_software_py['recommended'])
      txt2 = get_text_problem_executable(result_executables_none_py['recommended'])
      print('\n\n================================================================\n')
      print('\nINFO: Could not satisfy all `RECOMMENDED` software:\n\n{}\n\n{} '.format(txt, txt2))
      found_all_recommended = False
   elif result_software_py['recommended']:
      txt = get_text_problem_py(result_software_py['recommended'])
      print('\n\n================================================================\n')
      print('\nINFO: Could not satisfy all `RECOMMENDED` software:\n\n{} '.format(txt))
      found_all_recommended = False
   elif result_executables_none_py['recommended']:
      txt2 = get_text_problem_executable(result_executables_none_py['recommended'])
      print('\n\n================================================================\n')
      print('\nINFO: Could not satisfy all `RECOMMENDED` software:\n\n{} '.format(txt2))
      found_all_recommended = False

   if result_software_py['required'] and result_executables_none_py['required']:
      txt = get_text_problem_py(result_software_py['required'])
      txt2 = get_text_problem_executable(result_executables_none_py['required'])
      print('\n\n================================================================\n')
      sys.exit('\n***ERROR: Could not satisfy all `REQUIRED` software:\n\n{}\n\n{} '.format(txt, txt2))
   elif result_software_py['required']:
      txt = get_text_problem_py(result_software_py['required'])
      print('\n\n================================================================\n')
      sys.exit('\n***ERROR: Could not satisfy all `REQUIRED` software:\n\n{} '.format(txt))
   elif result_executables_none_py['required']:
      txt2 = get_text_problem_executable(result_executables_none_py['required'])
      print('\n\n================================================================\n')
      sys.exit('\n***ERROR: Could not satisfy all `REQUIRED` software:\n\n{} '.format(txt2))
   elif found_all_recommended:
      print('\n\n================================================================\n')
      print('\n***SUCCESS: Seems all `REQUIRED` and all `RECOMMENDED` software could be found.\n\n')
   else:
      print('\n\n================================================================\n')
      print('\n***ALL `REQUIRED` software could be found.\n   BUT: Could not satisfy all `RECOMMENDED` software. Which is not a problem at all.\n\n')



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == '__main__':
   # print('\n\nget_current_versions: ', get_current_versions(SOFTWARE_PY))
   # print('\n\n check_min_required_version: <2.2000.1ab0.3-t>, <2.893.456>: ', check_min_required_version('2.2000.1ab0.3-t','2.893.456'))

   # print(check_programs_executable(SOFTWARE_EXECUTABLES_NONE_PY, EXECUTABLES_ADDITIONAL_SEARCH_PATHS))
   # print(check_python_software(SOFTWARE_PY))

   check_software(SOFTWARE_PY, SOFTWARE_EXECUTABLES_NONE_PY, EXECUTABLES_ADDITIONAL_SEARCH_PATHS)
