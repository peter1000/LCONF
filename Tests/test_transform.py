""" tests LCONF Cast functions
"""
from datetime import datetime
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from sys import path as sys_path

from nose.tools import (
   eq_,
   ok_,
   raises as nose_raises
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

from LCONF.transform import (
   lconf_to_bool,
   lconf_to_int,
   lconf_to_float,
   lconf_to_pathexpanduser,
   lconf_to_datetime
)
from LCONF.utils import Err


@nose_raises(Err)
def test_cast__lconf_to_bool__expect_failure():
   """ Tests: test_cast__lconf_to_bool__expect_failure
   """
   print('::: TEST: test_cast__lconf_to_bool__expect_failure()')
   test_value = 'TT'
   lconf_to_bool(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_int__expect_failure():
   """ Tests: test_cast__lconf_to_int__expect_failure
   """
   print('::: TEST: test_cast__lconf_to_int__expect_failure()')
   test_value = '1234.5'
   lconf_to_int(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_int__expect_failure2():
   """ Tests: test_cast__lconf_to_int__expect_failure2
   """
   print('::: TEST: test_cast__lconf_to_int__expect_failure2()')
   test_value = '1-234'
   lconf_to_int(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_int__expect_failure3():
   """ Tests: test_cast__lconf_to_int__expect_failure3
   """
   print('::: TEST: test_cast__lconf_to_int__expect_failure3()')
   test_value = '-1-234'
   lconf_to_int(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_float__expect_failure():
   """ Tests: test_cast__lconf_to_float__expect_failure
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure()')
   test_value = '1k2345'
   lconf_to_float(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_float__expect_failure2():
   """ Tests: test_cast__lconf_to_float__expect_failure2
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure2()')
   test_value = '-123m45.0'
   lconf_to_float(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_float__expect_failure3():
   """ Tests: test_cast__lconf_to_float__expect_failure3
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure3()')
   test_value = '-12345.0me4'
   lconf_to_float(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_float__expect_failure4():
   """ Tests: test_cast__lconf_to_float__expect_failure4
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure4()')
   test_value = '123m45.0'
   lconf_to_float(test_value, test_value)


@nose_raises(Err)
def test_cast__lconf_to_float__expect_failure5():
   """ Tests: test_cast__lconf_to_float__expect_failure5
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure5()')
   test_value = '12345.0m134'
   lconf_to_float(test_value, test_value)


@nose_raises(Err)
def test_cast__to_lconf_pathexpanduser__expect_failure():
   """ Tests: test_cast__to_lconf_pathexpanduser__expect_failure
   """
   print('::: TEST: test_cast__to_lconf_pathexpanduser__expect_failure()')
   test_value = '12345'
   lconf_to_pathexpanduser(test_value, test_value)


@nose_raises(AssertionError)
def test_cast__to_lconf_pathexpanduser__expect_failure2():
   """ Tests: test_cast__to_lconf_pathexpanduser__expect_failure2
   """
   print('::: TEST: test_cast__to_lconf_pathexpanduser__expect_failure()')
   test_value = '~/etc/mypath'
   eq_(lconf_to_pathexpanduser(test_value, test_value), test_value, msg=None)


@nose_raises(Err)
def test_cast__lconf_to_datetime__expect_failure():
   """ Tests: test_cast__lconf_to_datetime__expect_failure
   """
   print('::: TEST: test_cast__lconf_to_datetime__expect_failure()')
   test_value = '2014-05-08 13:39.001'
   eq_(lconf_to_datetime(test_value, test_value), test_value, msg=None)


def test_cast__lconf_to_bool():
   """ Tests: test_cast__lconf_to_bool
   """
   print('::: TEST: test_cast__lconf_to_bool()')
   test_value = 'True'
   ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'true'
   ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'False'
   ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'false'
   ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)


def test_cast__lconf_to_int():
   """ Tests: test_cast__lconf_to_int
   """
   print('::: TEST: test_cast__lconf_to_int()')
   test_value = '1234'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '012345'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '9856123456789'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   eq_(lconf_to_int(test_value, test_value), 9856123456789, msg=None)
   test_value = '-1234'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '-012345'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '-9856123456789'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   eq_(lconf_to_int(test_value, test_value), -9856123456789, msg=None)
   test_value = '-9856123456789454326526986957054678588524573046472685674286049426748692487326864209401319467586728573829587'
   ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   eq_(
      lconf_to_int(test_value, test_value), 
      -9856123456789454326526986957054678588524573046472685674286049426748692487326864209401319467586728573829587, 
      msg=None
   )


def test_cast__lconf_to_float():
   """ Tests: test_cast__lconf_to_float
   """
   print('::: TEST: test_cast__lconf_to_float()')
   test_value = '12345.0'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '12345.000001234'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '0000012345.000001234'
   eq_(lconf_to_float(test_value, test_value), 12345.000001234, msg=None)
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-12345.0'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-12345.000001234'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-0000012345.000001234'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   eq_(lconf_to_float(test_value, test_value), -12345.000001234, msg=None)
   test_value = '+1.23'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   eq_(lconf_to_float(test_value, test_value), 1.23, msg=None)
   test_value = '   -12345\n'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   eq_(lconf_to_float(test_value, test_value), -12345.0, msg=None)
   test_value = '1e-003'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   eq_(lconf_to_float(test_value, test_value), 0.001, msg=None)
   test_value = '+1E6'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   eq_(lconf_to_float(test_value, test_value), 1000000.0, msg=None)
   test_value = '-Infinity'
   ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)


def test_cast__to_lconf_pathexpanduser():
   """ Tests: test_cast__to_lconf_pathexpanduser
   """
   print('::: TEST: test_cast__to_lconf_pathexpanduser()')
   test_value = '/etc/mypath'
   eq_(lconf_to_pathexpanduser(test_value, test_value), test_value, msg=None)
   test_value = '~/etc/mypath'
   ok_(lconf_to_pathexpanduser(test_value, test_value) != test_value, msg=None)
   test_value = '~/etc/mypath'
   ok_(lconf_to_pathexpanduser(test_value, test_value).startswith('/'), msg=None)


def test_cast__lconf_to_datetime():
   """ Tests: test_cast__lconf_to_datetime
   """
   print('::: TEST: test_cast__lconf_to_datetime()')

   test_value = '2014-05-08 13:39'
   ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)

   test_value = '2014-05-08 13:39:00'
   ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)


@nose_raises(Err)
def test_cast__lconf_to_datetime_expect_failure1():
   """ Tests: test_cast__lconf_to_datetime_expect_failure1
   """
   print('::: TEST: test_cast__lconf_to_datetime_expect_failure1()')

   test_value = '2014-05-08-13:39'
   ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)


@nose_raises(Err)
def test_cast__lconf_to_datetime_expect_failure2():
   """ Tests: test_cast__lconf_to_datetime_expect_failure2
   """
   print('::: TEST: test_cast__lconf_to_datetime_expect_failure2()')

   test_value = '2014-05-08-13:39:25'
   ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)


@nose_raises(Err)
def test_cast__lconf_to_datetime_expect_failure3():
   """ Tests: test_cast__lconf_to_datetime_expect_failure3
   """
   print('::: TEST: test_cast__lconf_to_datetime_expect_failure3()')

   test_value = '2014-05-08  13:39:25'
   ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == '__main__':
   pass
   test_cast__lconf_to_bool__expect_failure()
   test_cast__lconf_to_int__expect_failure()
   test_cast__lconf_to_int__expect_failure2()
   test_cast__lconf_to_int__expect_failure3()
   test_cast__lconf_to_float__expect_failure()
   test_cast__lconf_to_float__expect_failure2()
   test_cast__lconf_to_float__expect_failure3()
   test_cast__lconf_to_float__expect_failure4()
   test_cast__lconf_to_float__expect_failure5()
   test_cast__to_lconf_pathexpanduser__expect_failure()
   test_cast__to_lconf_pathexpanduser__expect_failure2()
   test_cast__lconf_to_datetime__expect_failure()

   test_cast__lconf_to_bool()
   test_cast__lconf_to_int()
   test_cast__lconf_to_float()
   test_cast__to_lconf_pathexpanduser()
   test_cast__lconf_to_datetime()

   test_cast__lconf_to_datetime_expect_failure1()
   test_cast__lconf_to_datetime_expect_failure2()
   test_cast__lconf_to_datetime_expect_failure3()
