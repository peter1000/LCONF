""" tests LCONF Cast functions
"""
from datetime import datetime
from inspect import (
   getfile,
   currentframe
)
from os.path import (
   abspath,
   dirname,
   join
)
from sys import path as syspath

from nose import tools

SCRIPT_PATH = dirname(abspath(getfile(currentframe())))
PROJECT_ROOT = dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

syspath.insert(0, PROJECT_ROOT)


from LCONF.Transform import (
   lconf_to_bool,
   lconf_to_int,
   lconf_to_float,
   lconf_to_number,
   lconf_to_pathexpanduser,
   lconf_to_datetime
)
from LCONF.ProjectErr import Err


@tools.raises(Err)
def test_cast__lconf_to_bool__expect_failure():
   """ Tests: cast to bool <must be any of: True, true, False, false>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_bool__expect_failure()')
   test_value = 'TT'
   lconf_to_bool(test_value, test_value)


@tools.raises(Err)
def test_cast__lconf_to_int__expect_failure():
   """ Tests: cast to int <must contain only digits plus optional a leading - (minus sign)>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_int__expect_failure()')
   test_value = '1234.5'
   lconf_to_int(test_value, test_value)


@tools.raises(Err)
def test_cast__lconf_to_int__expect_failure2():
   """ Tests: cast to int <must contain only digits plus optional a leading - (minus sign)>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_int__expect_failure2()')
   test_value = '1--234.5'
   lconf_to_int(test_value, test_value)
   
   
@tools.raises(Err)
def test_cast__lconf_to_float__expect_failure():
   """ Tests: cast to float <must contain only digits and exact 1 dot>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_float__expect_failure()')
   test_value = '12345'
   lconf_to_float(test_value, test_value)


@tools.raises(Err)
def test_cast__lconf_to_number__expect_failure():
   """ Tests: cast to number <only digits and maximum one dot allowed>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_number__expect_failure()')
   test_value = '12345l'
   lconf_to_number(test_value, test_value)


@tools.raises(Err)
def test_cast__to_lconf_pathexpanduser__expect_failure():
   """ Tests: cast to number <path_str must start with <~> or </>>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_number__expect_failure()')
   test_value = '12345'
   lconf_to_pathexpanduser(test_value, test_value)


@tools.raises(AssertionError)
def test_cast__to_lconf_pathexpanduser__expect_failure2():
   """ Tests: cast to lconf_pathexpanduser2 <expect path to be expanded>  (expect failure)
   """
   print('::: TEST: test_cast__to_lconf_pathexpanduser__expect_failure()')
   test_value = '~/etc/mypath'
   tools.eq_(lconf_to_pathexpanduser(test_value, test_value), test_value, msg=None)


@tools.raises(Err)
def test_cast__lconf_to_datetime__expect_failure():
   """ Tests: cast to lconf_to_datetime <date_str must be in the format: 16 character long: `YYYY-MM-DD-hh:mm`>  (expect failure)
   """
   print('::: TEST: test_cast__lconf_to_datetime__expect_failure()')
   test_value = '2014-05-08-13:39.001'
   tools.eq_(lconf_to_datetime(test_value, test_value), test_value, msg=None)


def test_cast__lconf_to_bool():
   """ Tests: cast to bool: True, true, False, false
   """
   print('::: TEST: test_cast__lconf_to_bool()')
   test_value = 'True'
   tools.ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'true'
   tools.ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'False'
   tools.ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)
   test_value = 'false'
   tools.ok_(isinstance(lconf_to_bool(test_value, test_value), bool), msg=None)


def test_cast__lconf_to_int():
   """ Tests: cast to int <must contain only digits>
   """
   print('::: TEST: test_cast__lconf_to_int()')
   test_value = '1234'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '012345'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '9856123456789'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '-1234'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '-012345'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)
   test_value = '-9856123456789'
   tools.ok_(isinstance(lconf_to_int(test_value, test_value), int), msg=None)


def test_cast__lconf_to_float():
   """ Tests: cast to float <must contain only digits and exact 1 dot>
   """
   print('::: TEST: test_cast__lconf_to_float()')
   test_value = '12345.0'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '12345.000001234'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '0000012345.000001234'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-12345.0'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-12345.000001234'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)
   test_value = '-0000012345.000001234'
   tools.ok_(isinstance(lconf_to_float(test_value, test_value), float), msg=None)


def test_cast__lconf_to_number():
   """ Tests: cast to number <only digits and maximum one dot allowed>
   """
   print('::: TEST: test_cast__lconf_to_number()')
   test_value = '12345'
   tools.ok_(isinstance(lconf_to_number(test_value, test_value), float), msg=None)
   test_value = '12345.000001234'
   tools.ok_(isinstance(lconf_to_number(test_value, test_value), float), msg=None)
   test_value = '-12345'
   tools.ok_(isinstance(lconf_to_number(test_value, test_value), float), msg=None)
   test_value = '-12345.000001234'
   tools.ok_(isinstance(lconf_to_number(test_value, test_value), float), msg=None)
   

def test_cast__to_lconf_pathexpanduser():
   """ Tests: cast to lconf_pathexpanduser <path_str must start with <~> or </>>
   """
   print('::: TEST: test_cast__to_lconf_pathexpanduser()')
   test_value = '/etc/mypath'
   tools.eq_(lconf_to_pathexpanduser(test_value, test_value), test_value, msg=None)
   test_value = '~/etc/mypath'
   tools.ok_(lconf_to_pathexpanduser(test_value, test_value) != test_value, msg=None)
   test_value = '~/etc/mypath'
   tools.ok_(lconf_to_pathexpanduser(test_value, test_value).startswith('/'), msg=None)


def test_cast__lconf_to_datetime():
   """ Tests: cast to number <only digits and maximum one dot allowed>
   """
   print('::: TEST: test_cast__lconf_to_datetime()')
   test_value = '2014-05-08-13:39'
   tools.ok_(isinstance(lconf_to_datetime(test_value, test_value), datetime), msg=None)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == '__main__':
   test_cast__lconf_to_bool__expect_failure()
   test_cast__lconf_to_int__expect_failure()
   test_cast__lconf_to_int__expect_failure2()
   test_cast__lconf_to_float__expect_failure()
   test_cast__lconf_to_number__expect_failure()
   test_cast__to_lconf_pathexpanduser__expect_failure()
   test_cast__to_lconf_pathexpanduser__expect_failure2()
   test_cast__lconf_to_datetime__expect_failure()

   test_cast__lconf_to_bool()
   test_cast__lconf_to_int()
   test_cast__lconf_to_float()
   test_cast__lconf_to_number()
   test_cast__to_lconf_pathexpanduser()
   test_cast__lconf_to_datetime()
