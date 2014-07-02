""" Write MANIFEST.in file for setup.py
"""
import os
from os import path
import sys


INCLUDE_PATHS = []
EXCLUDE_PATHS = []

#======== CONFIGURE HERE
# IMPORTANT: EXCLUDE precedes over INCLUDE

# === FIRST INCLUDE:
INCLUDE_FILES = [
   # common
   '.coveragerc',
   'CHANGELOG.txt',
   'LICENSE.rst',
   '.gitignore',
   'Makefile',
   'MANIFEST.in',
   'project_pycharm.dic',
   'README.rst',
   'requirements.txt',
   'setup.cfg',
   'setup.py',
   'WriteManifest.py',
   'TODO.txt',
]


# AUTO INCLUDE DIRS/FILES
# format: dict: relative path to setup.py : [] list of extensions. To include all use an empty list for file extensions
# to specify the top level dir use '.'
# e.g. add all '.txt' and '.rst' files of docs: AUTO_INCLUDE_DIRS_FILES = {'docs': ['.txt', '.rst']}
# e.g. add all files specify an empty list of docs: AUTO_INCLUDE_DIRS_FILES = {'docs': []}
AUTO_INCLUDE_DIRS_FILES = {
   '.': [],
}


# === SECOND EXCLUDE:
# EXCLUDE:FILES: relative path to setup.py: e.g. .coverage
EXCLUDE_FILES = ['.coverage']


# AUTO EXCLUDE DIRS/FILES
# format: dict: relative path to setup.py : [] list of extensions. To include all use an empty list for file extensions
# to specify the top level dir use '.'
# e.g. exclude all '.pyc' files of project: AUTO_EXCLUDE_DIRS_FILES = {'.': ['.pyc']}
AUTO_EXCLUDE_DIRS_FILES = {'.': ['.pyc'], 'build': [], 'dist': [], }


# AUTO EXCLUDE DIRS/SUBDIRS
# format: dict: relative path to setup.py : [] list of sub_dirs to exclude: all files below a defined subdir will be excluded
# to specify the top level dir use '.'
# e.g. exclude all directories with name: 'test.egg-info' under   folder 'bin': AUTO_EXCLUDE_DIRS_SUBDIRS = {'bin': ['test.egg-info']}
AUTO_EXCLUDE_DIRS_SUBDIRS = {'.': ['__pycache__', '.git', '.idea', 'cover', 'LCONF.egg-info']}

#======== END CONFIGURE HERE


def get_auto_dirs_files(auto_dirs_files):
   """ Returns all files matching extension criteria

   Args:
      auto_dirs_files (dict): format: {'str': [])
         dict-key: string defines a search directory relative to the folder of this script (should reside in the project root next to the setup.py)
         dict-value: a list of file extensions one want to be included.:
         NOTE: to include all files below the search directory use an empty list as value

      Examples:
         include all .pyc, .log files below current directory: and include also all files below: directory docs

         {
         '.': ['.pyc', '.log'],
         'docs': []
         }

   Returns:
      List: A list of matching file paths:
      if we specified a key '.' the leading 2 cars are stripped off leading dir ./
   """
   auto_files = []
   for search_root_dir, extensions in auto_dirs_files.items():
      for root, dirs, files in os.walk(search_root_dir):
         root_path = root[2:] if search_root_dir == '.' else root  # strip leading dir ./ if we specified a key '.'
         for incl_file in files:
            if not extensions:
               auto_files.append(path.join(root_path, incl_file))
            elif path.splitext(incl_file)[1] in extensions:
               auto_files.append(path.join(root_path, incl_file))
   return sorted(auto_files)


def get_auto_dirs_subdirs(auto_dirs_subdirs):
   """ Returns all files matching search subdirectories criteria

   Args:
      auto_dirs_subdirs (dict): format: {'str': [])
         dict-key: string defines a search directory relative to the folder of this script (should reside in the project root next to the setup.py)
         dict-value: a list of subdirectories one wants to search for to be included

   Examples
      include all files below any '.git' nad any '__pycache__'   directories starting in this script folder

      {'.': ['__pycache__', '.git']}

   Returns:
      List: A list of matching file paths:
      if we specified a key '.' the leading 2 cars are stripped off leading dir ./
   """
   auto_files = []
   for search_root_dir, find_subdirs in auto_dirs_subdirs.items():
      if not find_subdirs:
         sys.exit('ERROR: auto_dirs_files: for search_root_dir: <{}> is no find_subdirs list defined.'.format(search_root_dir))
      for root, dirs, files in os.walk(search_root_dir):
         for dir_ in dirs:
            if dir_ in find_subdirs:
               for sub_root, sub_dirs, sub_files in os.walk(path.join(root, dir_)):
                  sub_root_path = sub_root[2:] if search_root_dir == '.' else sub_root  # strip leading dir ./ if we specified a key '.'
                  for incl_file in sub_files:
                     auto_files.append(path.join(sub_root_path, incl_file))
   return auto_files


def get_final_manifest_content(include_files, excl_file):
   """ Return final file paths to be included in the MANIFEST.in
   IMPORTANT: EXCLUDE precedes over INCLUDE

   Args:
      include_files (list): list of files one wants to include (may also contain doubles)
      excl_file (list): list of files one wants to exclude (may also contain doubles)

   Returns:
      List: A list of all include files which are not excluded.
   """
   manifest_files = []
   frozen_excl_file = frozenset(excl_file)
   for incl_file in frozenset(include_files):
      if not incl_file in frozen_excl_file:
         manifest_files.append(incl_file)
   return manifest_files


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
def main():
   """ Writes the MANIFEST.in in current directory. """
   # === FIRST INCLUDE:
   INCLUDE_PATHS.extend([file_ for file_ in INCLUDE_FILES])
   INCLUDE_PATHS.extend(get_auto_dirs_files(AUTO_INCLUDE_DIRS_FILES))

   # === SECOND INCLUDE:
   EXCLUDE_PATHS.extend([file_ for file_ in EXCLUDE_FILES])
   EXCLUDE_PATHS.extend(get_auto_dirs_files(AUTO_EXCLUDE_DIRS_FILES))
   EXCLUDE_PATHS.extend(get_auto_dirs_subdirs(AUTO_EXCLUDE_DIRS_SUBDIRS))

   add_to_manifest = get_final_manifest_content(INCLUDE_PATHS, EXCLUDE_PATHS)

   write_txt = '\n'.join(['include {0}'.format(incl_file_path) for incl_file_path in add_to_manifest])
   with open('MANIFEST.in', 'w') as file_f:
      file_f.write(write_txt)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
