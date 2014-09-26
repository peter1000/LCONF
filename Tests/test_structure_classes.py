""" test structure classes
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
from LCONF.lconf_structure_classes import (
   Blk,
   BlkI,
   KVList,
   KVMap,
   Root,
   ListOT,
   _deactivated as lconf_structure_classes_deactivated,
)
from LCONF.utils import (
   Err,
   MethodDeactivatedErr,
)


@nose_raises(MethodDeactivatedErr)
def test_lconf_structure_classes_deactivated_expect_failure():
   """ Tests: test_lconf_structure_classes_deactivated_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes_deactivated_expect_failure()')

   lconf_structure_classes_deactivated()


@nose_raises(Err)
def test_lconf_structure_classes0_expect_failure():
   """ Tests: test_lconf_structure_classes0_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes0_expect_failure()')

   Blk(('key', 'value'))


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes1():
   """ Tests: test_lconf_structure_classes1
   """
   print('::: TEST: test_lconf_structure_classes1()')

   obj_ = Blk([('key', 'value')])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   obj_.__reduce__()


@nose_raises(Err)
def test_lconf_structure_classes2_expect_failure():
   """ Tests: test_lconf_structure_classes2_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes2_expect_failure()')

   BlkI(-1, -1, [('key', 'value')])


@nose_raises(Err)
def test_lconf_structure_classes3_expect_failure():
   """ Tests: test_lconf_structure_classes3_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes3_expect_failure()')

   BlkI(-1, -1, Blk([]))


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes4():
   """ Tests: test_lconf_structure_classes4
   """
   print('::: TEST: test_lconf_structure_classes4()')

   obj_ = BlkI(-1, -1, Blk([('key', 'value')]))
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   obj_.__reduce__()


@nose_raises(Err)
def test_lconf_structure_classes0_expect_failure5():
   """ Tests: test_lconf_structure_classes0_expect_failure5
   """
   print('::: TEST: test_lconf_structure_classes0_expect_failure5()')

   KVList(True, ('1', '2'))


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes6():
   """ Tests: test_lconf_structure_classes6
   """
   print('::: TEST: test_lconf_structure_classes6()')

   obj_ = KVList(True, ['1', '2'])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)


@nose_raises(Err)
def test_lconf_structure_classes0_expect_failure7():
   """ Tests: test_lconf_structure_classes0_expect_failure7
   """
   print('::: TEST: test_lconf_structure_classes0_expect_failure7()')

   KVMap(('1', '2'))


@nose_raises(Err)
def test_lconf_structure_classes8_expect_failure():
   """ Tests: test_lconf_structure_classes8_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes8_expect_failure()')

   KVMap([])


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes9():
   """ Tests: test_lconf_structure_classes9
   """
   print('::: TEST: test_lconf_structure_classes9()')

   obj_ = KVMap([('key', 'value'), ('key1', 'value1')])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   obj_.__reduce__()


@nose_raises(Err)
def test_lconf_structure_classes10_expect_failure():
   """ Tests: test_lconf_structure_classes10_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes10_expect_failure()')

   Root(())


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes11():
   """ Tests: test_lconf_structure_classes11
   """
   print('::: TEST: test_lconf_structure_classes11()')

   obj_ = Root([('key', 'value'), ('key1', 'value1')])
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   obj_.__reduce__()


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
def test_lconf_structure_classes12():
   """ Tests: test_lconf_structure_classes12
   """
   print('::: TEST: test_lconf_structure_classes12()')

   obj_ = Root([('key', 'value'), ('key1', 'value1')])
   obj_.set_class__dict__item('mydata', 'new value')

   dumps_result = pickle_dumps(obj_, protocol=P_HIGHEST_PROTOCOL)
   obj_from_pickle = Root.frompickle(dumps_result)

   eq_(obj_.mydata, 'new value', msg=None)
   eq_(obj_.key_order, ['key', 'key1'], msg=None)
   eq_(obj_.mydata, obj_from_pickle.mydata, msg=None)
   eq_(obj_.key_order, obj_from_pickle.key_order, msg=None)


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes13_expect_failure():
   """ Tests: test_lconf_structure_classes13_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes13_expect_failure()')

   dumps_result = pickle_dumps([('key', 'value'), ('key1', 'value1')], protocol=P_HIGHEST_PROTOCOL)
   obj_from_pickle = Root.frompickle(dumps_result)


@nose_raises(Err)
def test_lconf_structure_classes14_expect_failure():
   """ Tests: test_lconf_structure_classes14_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes14_expect_failure()')

   ListOT(['a', 'b'], ())


@nose_raises(Err)
def test_lconf_structure_classes15_expect_failure():
   """ Tests: test_lconf_structure_classes15_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes15_expect_failure()')

   ListOT([], [('11', '22')])


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes16_expect_failure():
   """ Tests: test_lconf_structure_classes16_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes16_expect_failure()')

   # noinspection PyRedundantParentheses
   obj_ = ListOT(('a', 'b'), [('11', '22')], column_replace_missing=('-1'))


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes17_expect_failure():
   """ Tests: test_lconf_structure_classes17_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes17_expect_failure()')

   obj_ = ListOT(('a', 'b'), [('11', '22')], column_replace_missing=('-1',))


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes18():
   """ Tests: test_lconf_structure_classes18
   """
   print('::: TEST: test_lconf_structure_classes18()')

   obj_ = ListOT(('a', 'b'), [('11', '22')], column_replace_missing=('-1', '-1'))
   obj_.set_class__dict__item('mydata', 'new value')
   eq_(obj_.mydata, 'new value', msg=None)

   eq_(obj_.column_names, ('a', 'b'), msg=None)
   eq_(obj_.column_names_idx_lookup, {'a': 0, 'b': 1}, msg=None)
   eq_(obj_.column_names_counted, 2, msg=None)
   eq_(obj_.column_replace_missing, ('-1', '-1'), msg=None)


@nose_raises(Err)
def test_lconf_structure_classes19_expect_failure():
   """ Tests: test_lconf_structure_classes19_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes19_expect_failure()')

   obj_ = ListOT(('a', 'b', 'a'), [('11', '22', '33')])
   obj_.replace_column_names(('a', 'b', 'c'))


@nose_raises(Err)
def test_lconf_structure_classes20_expect_failure():
   """ Tests: test_lconf_structure_classes20_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes20_expect_failure()')

   obj_ = ListOT(('a', 'b'), [('11', '22')])
   obj_.replace_column_names('wrong type')


# noinspection PyUnresolvedReferences,PyUnresolvedReferences
def test_lconf_structure_classes21():
   """ Tests: test_lconf_structure_classes21
   """
   print('::: TEST: test_lconf_structure_classes21()')

   obj_ = ListOT(('a', 'b', 'c'), [('11', '22', '33')])
   eq_(obj_.column_names, ('a', 'b', 'c'), msg=None)

   obj_.replace_column_names(('new a', 'new b', 'new c'))
   eq_(obj_.column_names, ('new a', 'new b', 'new c'), msg=None)
   eq_(obj_[0], ('11', '22', '33'), msg=None)


@nose_raises(Err)
def test_lconf_structure_classes22_expect_failure():
   """ Tests: test_lconf_structure_classes22_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes22_expect_failure()')

   obj_ = ListOT(('a', 'b', 'c'), [('11', '22', '33')])
   obj_.replace_column_names(('a', 'b'))


@nose_raises(Err)
def test_lconf_structure_classes23_expect_failure():
   """ Tests: test_lconf_structure_classes23_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes23_expect_failure()')

   obj_ = ListOT(('a', 'b', 'c'), [('11', '22', '33')])
   obj_.replace_column_names(('a', 'b', 'b'))


@nose_raises(Err)
def test_lconf_structure_classes24_expect_failure():
   """ Tests: test_lconf_structure_classes24_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes24_expect_failure()')

   obj_ = ListOT(('a', 'b', 'c'), [('11', '22', '33'), ('111', '222', '333')])
   obj_.this_column_values('x')


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes25_expect_failure():
   """ Tests: test_lconf_structure_classes25_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes25_expect_failure()')

   obj_ = BlkI(-2, -1, Blk([('key', 'value')]))


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes26_expect_failure():
   """ Tests: test_lconf_structure_classes26_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes26_expect_failure()')

   obj_ = BlkI(-1, -2, Blk([('key', 'value')]))


# noinspection PyUnusedLocal
@nose_raises(Err)
def test_lconf_structure_classes27_expect_failure():
   """ Tests: test_lconf_structure_classes27_expect_failure
   """
   print('::: TEST: test_lconf_structure_classes27_expect_failure()')

   obj_ = BlkI(-2, -2, Blk([('key', 'value')]))


# noinspection PyUnresolvedReferences
def test_lconf_structure_classes28():
   """ Tests: test_lconf_structure_classes28
   """
   print('::: TEST: test_lconf_structure_classes28()')

   obj_ = ListOT(('a', 'b', 'c'), [('11', '22', '33'), ('111', '222', '333')])
   values_column_a = obj_.this_column_values('a')

   obj_.replace_column_names(('new a', 'new b', 'new c'))
   eq_(obj_.column_names, ('new a', 'new b', 'new c'), msg=None)
   eq_(values_column_a, ['11', '111'], msg=None)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   pass
   test_lconf_structure_classes_deactivated_expect_failure()
   test_lconf_structure_classes0_expect_failure()
   test_lconf_structure_classes1()
   test_lconf_structure_classes2_expect_failure()
   test_lconf_structure_classes3_expect_failure()
   test_lconf_structure_classes4()
   test_lconf_structure_classes0_expect_failure5()
   test_lconf_structure_classes6()
   test_lconf_structure_classes0_expect_failure7()
   test_lconf_structure_classes8_expect_failure()
   test_lconf_structure_classes9()
   test_lconf_structure_classes10_expect_failure()
   test_lconf_structure_classes11()
   test_lconf_structure_classes12()
   test_lconf_structure_classes13_expect_failure()
   test_lconf_structure_classes14_expect_failure()
   test_lconf_structure_classes15_expect_failure()
   test_lconf_structure_classes16_expect_failure()
   test_lconf_structure_classes17_expect_failure()
   test_lconf_structure_classes18()
   test_lconf_structure_classes19_expect_failure()
   test_lconf_structure_classes20_expect_failure()
   test_lconf_structure_classes21()
   test_lconf_structure_classes22_expect_failure()
   test_lconf_structure_classes23_expect_failure()
   test_lconf_structure_classes24_expect_failure()
   test_lconf_structure_classes25_expect_failure()
   test_lconf_structure_classes26_expect_failure()
   test_lconf_structure_classes27_expect_failure()
   test_lconf_structure_classes28()
