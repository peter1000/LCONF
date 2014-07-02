""" setup / install / distribute

This uses the WriteManifest module to include the items we want
"""
import setuptools
import sys

if sys.version_info[:2] < (3, 4):
   sys.exit('LCONF is only tested with Python 3.4.1 or higher:\ncurrent version: {0:d}.{1:d}'.format(sys.version_info[:2][0], sys.version_info[:2][1]))

from LCONF import Version
import WriteManifest


print('\n\n==============================\n`LCONF` VERSION: {}:\n   is developed on TESTED_HOST_OS platform: {}\n==============================\n\n'.format(Version.__version__, Version.TESTED_HOST_OS))


#======== GET INCLUDES for: MANIFEST.in:    CONFIGURE IN: write_manifest_in.py
WriteManifest.main()


def read_requires(filename):
   """ Helper: read_requires
   """
   requires = []
   with open(filename, 'r') as file_:
      for line in file_:
         line = line.strip()
         if not line or line.startswith('#'):
            continue
         requires.append(line)
   return requires


setuptools.setup(
   name='LCONF',
   version=Version.__version__,
   author='peter1000',
   author_email='https://github.com/peter1000',
   url='https://github.com/peter1000/',
   license='BSD-3-Clause',
   keywords='python markup configuration json yaml',
   packages=setuptools.find_packages(),
   include_package_data=True,
   scripts=[
      'bin/lconf-validate'
   ],
   install_requires=read_requires('requirements.txt'),
   test_suite='nose.collector',
   use_2to3=False,
   zip_safe=False,
   platforms=['Linux'],
   classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3',
      'Topic :: Text Processing :: Markup',
      'Topic :: Software Development :: Libraries :: Python Modules'
   ],
   description='L(ight) CONF(iguration): A simple human-readable data serialization format for dynamic configuration.',
   long_description=open("README.rst", "r").read(),
)

print('\n\n==============================\n`LCONF` VERSION: {}:\n   is developed on TESTED_HOST_OS platform: {}\n==============================\n\n'.format(Version.__version__, Version.TESTED_HOST_OS))


#use: make to generate a source distribution tar
