""" test lconf classes
"""
from inspect import (
   getfile as inspect_getfile,
   currentframe as inspect_currentframe,
)
from os.path import (
   abspath as path_abspath,
   dirname as path_dirname,
   join as path_join,
)
from pickle import (
   dumps as pickle_dumps,
   HIGHEST_PROTOCOL as P_HIGHEST_PROTOCOL
)
from sys import path as sys_path

from nose.tools import (
   eq_,
   raises as nose_raises,
)


SCRIPT_PATH = path_dirname(path_abspath(inspect_getfile(inspect_currentframe())))
PROJECT_ROOT = path_dirname(SCRIPT_PATH)

ROOT_PACKAGE_NAME = 'LCONF'
ROOT_PACKAGE_PATH = path_join(PROJECT_ROOT, ROOT_PACKAGE_NAME)

sys_path.insert(0, PROJECT_ROOT)

# noinspection PyProtectedMember
from LCONF.lconf_classes import (
   LconfBlk,
   LconfBlkI,
   LconfKVList,
   LconfKVMap,
   LconfRoot,
   LconfListOT,
   _deactivated as lconf_classes_deactivated,
)
from LCONF.utils import (
   Err,
   MethodDeactivatedErr,
)


@nose_raises(MethodDeactivatedErr)
def test_lconf_classes_deactivated_expect_failure():
   """ Tests: test_lconf_classes_deactivated_expect_failure
   """
   print('::: TEST: test_lconf_classes_deactivated_expect_failure()')

   lconf_classes_deactivated()


# noinspection PyUnresolvedReferences,PyUnresolvedReferences
def test_lconf_classes0():
   """ Tests: test_lconf_classes0
   """
   print('::: TEST: test_lconf_classes0()')

   obj_ = LconfBlk({'key1': '1', 'key2': '2'}, ['key1', 'key2'])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)
   eq_(obj_.key_order, ['key1', 'key2'], msg=None)

   obj_.__reduce__()


# noinspection PyUnresolvedReferences
def test_lconf_classes1():
   """ Tests: test_lconf_classes1
   """
   print('::: TEST: test_lconf_classes1()')

   obj_ = LconfBlkI(
      {
         'block1': LconfBlk({'block1key1': '1', 'block1key2': '2'}, ['block1key1', '3']),
         'block2': LconfBlk({'block2key1': '1', 'block2key2': '2'}, ['block2key1', '3'])
      },
      ['block1', 'block2'],
      -1,
      -1
   )

   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)
   eq_(obj_.key_order, ['block1', 'block2'], msg=None)
   eq_(obj_.min_required_blocks, -1, msg=None)
   eq_(obj_.max_allowed_blocks, -1, msg=None)
   eq_(obj_.has_comments, False, msg=None)

   obj_.__setitem__('block3', LconfBlk({'block3key1': '1', 'block3key2': '2'}, ['block3key1', '3']))
   eq_(obj_.key_order, ['block1', 'block2', 'block3'], msg=None)
   eq_(obj_['block3'], {'block3key1': '1', 'block3key2': '2'}, msg=None)

   obj_.__setitem__('block3', LconfBlk({'block3key1New': '1', 'block3key2New': '2'}, ['block3key1New', '3']))
   eq_(obj_['block3'], {'block3key1New': '1', 'block3key2New': '2'}, msg=None)

   obj_.__reduce__()


# noinspection PyUnresolvedReferences
def test_lconf_classes2():
   """ Tests: test_lconf_classes2
   """
   print('::: TEST: test_lconf_classes2()')

   obj_ = LconfKVList(['1', '2'], True)
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)


# noinspection PyUnresolvedReferences
def test_lconf_classes3():
   """ Tests: test_lconf_classes3
   """
   print('::: TEST: test_lconf_classes3()')

   obj_ = LconfKVMap({'key': 'value', 'key1': 'value1'}, ['key', 'key1'])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   obj_.__reduce__()


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
def test_lconf_classes4():
   """ Tests: test_lconf_classes4
   """
   print('::: TEST: test_lconf_classes4()')

   obj_ = LconfRoot({'key': 'value', 'key1': 'value1'}, ['key', 'key1'])
   obj_.set_class__dict__item('mydata', 'new value')

   dumps_result = pickle_dumps(obj_, protocol=P_HIGHEST_PROTOCOL)
   obj_from_pickle = LconfRoot.frompickle(dumps_result)

   eq_(obj_.mydata, 'new value', msg=None)
   eq_(obj_.key_order, ['key', 'key1'], msg=None)
   eq_(obj_.mydata, obj_from_pickle.mydata, msg=None)
   eq_(obj_.key_order, obj_from_pickle.key_order, msg=None)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_classes5_expect_failure():
   """ Tests: test_lconf_classes5_expect_failure
   """
   print('::: TEST: test_lconf_classes5_expect_failure()')

   obj_ = LconfRoot({'key': 'value', 'key1': 'value1'}, ['key', 'key1'])
   obj_.set_class__dict__item('mydata', 'new value')

   dumps_result = pickle_dumps([('key', 'value'), ('key1', 'value1')], protocol=P_HIGHEST_PROTOCOL)
   obj_from_pickle = LconfRoot.frompickle(dumps_result)


# noinspection PyUnresolvedReferences
def test_lconf_classes6():
   """ Tests: test_lconf_classes6
   """
   print('::: TEST: test_lconf_classes6()')

   obj_ = LconfListOT(
      [('11', '22')],
      ('a', 'b'),
      {'a': 0, 'b': 1},
      2,
      ('-1', '-1')
   )
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   eq_(obj_.column_names, ('a', 'b'), msg=None)
   eq_(obj_.column_names_idx_lookup, {'a': 0, 'b': 1}, msg=None)
   eq_(obj_.column_names_counted, 2, msg=None)
   eq_(obj_.column_replace_missing, ('-1', '-1'), msg=None)

   obj_.replace_column_names(('new a', 'new b'))
   eq_(obj_.column_names, ('new a', 'new b'), msg=None)
   eq_(obj_[0], ('11', '22'), msg=None)


@nose_raises(Err)
def test_lconf_classes7_expect_failure():
   """ Tests: test_lconf_classes7_expect_failure
   """
   print('::: TEST: test_lconf_classes7_expect_failure()')

   obj_ = LconfListOT(
      [('11', '22', '33')],
      ('a', 'b', 'c'),
      {'a': 0, 'b': 1, 'c': 2},
      3,
      ('-1', '-1', '-1')
   )
   obj_.replace_column_names(('a', 'b'))


@nose_raises(Err)
def test_lconf_classes8_expect_failure():
   """ Tests: test_lconf_classes8_expect_failure
   """
   print('::: TEST: test_lconf_classes8_expect_failure()')

   obj_ = LconfListOT(
      [('11', '22', '33')],
      ('a', 'b', 'c'),
      {'a': 0, 'b': 1, 'c': 2},
      3,
      ('-1', '-1', '-1')
   )
   obj_.replace_column_names(('a', 'b', 'b'))


@nose_raises(Err)
def test_lconf_classes9_expect_failure():
   """ Tests: test_lconf_classes9_expect_failure
   """
   print('::: TEST: test_lconf_classes9_expect_failure()')

   obj_ = LconfListOT(
      [('11', '22', '33')],
      ('a', 'b', 'c'),
      {'a': 0, 'b': 1, 'c': 2},
      3,
      ('-1', '-1', '-1')
   )
   obj_.replace_column_names('Wrong Type')


@nose_raises(Err)
def test_lconf_classes10_expect_failure():
   """ Tests: test_lconf_classes10_expect_failure
   """
   print('::: TEST: test_lconf_classes10_expect_failure()')

   obj_ = LconfListOT(
      [('11', '22')],
      ('a', 'b'),
      {'a': 0, 'b': 1},
      2,
      ('-1', '-1')
   )
   obj_.this_column_values('x')


# noinspection PyUnresolvedReferences
def test_lconf_classes11_expect_failure():
   """ Tests: test_lconf_classes11_expect_failure
   """
   print('::: TEST: test_lconf_classes11_expect_failure()')

   obj_ = LconfListOT(
      [('11', '22'), ('111', '222')],
      ('a', 'b'),
      {'a': 0, 'b': 1},
      2,
      ('-1', '-1')
   )
   values_column_a = obj_.this_column_values('a')

   obj_.replace_column_names(('new a', 'new b'))
   eq_(obj_.column_names, ('new a', 'new b'), msg=None)
   eq_(values_column_a, ['11', '111'], msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_classes_deactivated_expect_failure()
   test_lconf_classes0()
   test_lconf_classes1()
   test_lconf_classes2()
   test_lconf_classes3()
   test_lconf_classes4()
   test_lconf_classes5_expect_failure()
   test_lconf_classes6()
   test_lconf_classes7_expect_failure()
   test_lconf_classes8_expect_failure()
   test_lconf_classes9_expect_failure()
   test_lconf_classes10_expect_failure()
   test_lconf_classes11_expect_failure()
