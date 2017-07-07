# -*- coding: utf-8 -*-

from sys import hexversion

import random
#from .context import disktypes
from disktypes import DiskList
from itertools import chain
from nose.tools import raises

if False:
    class DiskList(list):
        def destroy(self):
            pass
        def add(self, *args):
            return self.append(*args)
        def copy(self):
            return DiskList(self[:])
    
if hexversion < 0x03000000:
    from itertools import izip as zip
    range = xrange

def test_init():
    dl = DiskList(range(100))#, location='test_disklist')
    assert all(tup[0] == tup[1] for tup in zip(dl, range(100)))
    dl.destroy()

def test_add():
    random.seed(0)
    dl = DiskList()
    for val in range(10):
        dl.add(val)
    dl.destroy()

    dl = DiskList()
    for val in range(10, 0, -1):
        dl.add(val)
    dl.destroy()

    dl = DiskList()
    for val in range(10):
        dl.add(random.random())
    dl.destroy()

def test_contains():
    dl = DiskList()
    assert 0 not in dl

    dl.extend(range(10))

    for val in range(10):
        assert val in dl

    assert 10 not in dl
    dl.destroy()

def test_remove():
    dl = DiskList([0])

    assert dl.remove(0) == None
    assert len(dl) == 0
    
    dl = DiskList([1, 2, 2, 2, 3, 3, 5])

    dl.remove(2)
    
    assert all(tup[0] == tup[1] for tup in zip(dl, [1, 2, 2, 3, 3, 5]))
    dl.destroy()

@raises(ValueError)
def test_index_nonexisting_value():
    dl = DiskList()
    dl.index(0)
    dl.destroy()

@raises(ValueError)
def test_remove_valueerror1():
    dl = DiskList()
    dl.remove(0)
    dl.destroy()

@raises(ValueError)
def test_remove_valueerror2():
    dl = DiskList(range(100))
    dl.remove(100)
    dl.destroy()

@raises(ValueError)
def test_remove_valueerror3():
    dl = DiskList([1, 2, 2, 2, 3, 3, 5])
    dl.remove(4)
    dl.destroy()

def test_delete():
    dl = DiskList(range(20))
    for val in range(20):
        dl.remove(val)
    assert len(dl) == 0
    dl.destroy()

def test_sort():
    dl = DiskList([5, 4, 3, 2, 1])
    dl.sort()
    assert dl[0] == 1 and dl[4] == 5
    dl.destroy()

def test_getitem():
    random.seed(0)
    dl = DiskList()
    lst = list()
    for _ in range(100):
        val = random.random()
        dl.add(val)
        lst.append(val)
    assert all(dl[idx] == lst[idx] for idx in range(100))
    assert all(dl[idx - 99] == lst[idx - 99] for idx in range(100))
    dl.destroy()

def test_getitem_slice():
    random.seed(0)
    dl = DiskList()

    lst = list()

    for rpt in range(100):
        val = random.random()
        dl.append(val)
        lst.append(val)

    lst.sort()
    dl.sort()

    assert all(dl[start:] == lst[start:]
               for start in [-75, -25, 0, 25, 75])

    assert all(dl[:stop] == lst[:stop]
               for stop in [-75, -25, 0, 25, 75])

    assert all(dl[::step] == lst[::step]
               for step in [-5, -1, 1, 5])

    assert all(dl[start:stop] == lst[start:stop]
               for start in [-75, -25, 0, 25, 75]
               for stop in [-75, -25, 0, 25, 75])

    assert all(dl[:stop:step] == lst[:stop:step]
               for stop in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])

    assert all(dl[start::step] == lst[start::step]
               for start in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])

    assert all(dl[start:stop:step] == lst[start:stop:step]
               for start in [-75, -25, 0, 25, 75]
               for stop in [-75, -25, 0, 25, 75]
               for step in [-5, -1, 1, 5])
    dl.destroy()

def test_getitem_slice_big():
    dl = DiskList(range(4))
    lst = list(range(4))

    itr = ((start, stop, step)
           for start in [-6, -4, -2, 0, 2, 4, 6]
           for stop in [-6, -4, -2, 0, 2, 4, 6]
           for step in [-3, -2, -1, 1, 2, 3])

    for start, stop, step in itr:
        assert dl[start:stop:step] == lst[start:stop:step]
    dl.destroy()

@raises(ValueError)
def test_getitem_slicezero():
    dl = DiskList(range(100))
    dl[::0]
    dl.destroy()

@raises(IndexError)
def test_getitem_indexerror1():
    dl = DiskList()
    dl[5]
    dl.destroy()

@raises(IndexError)
def test_getitem_indexerror2():
    dl = DiskList(range(100))
    dl[200]
    dl.destroy()

@raises(IndexError)
def test_getitem_indexerror3():
    dl = DiskList(range(100))
    dl[-101]
    dl.destroy()

def test_delitem():
    random.seed(0)
    dl = DiskList(range(100))
    while len(dl) > 0:
        pos = random.randrange(len(dl))
        del dl[pos]
    dl.destroy()
    dl = DiskList(range(100))
    del dl[:]
    assert len(dl) == 0
    dl.destroy()

def test_delitem_slice():
    dl = DiskList(range(100))
    del dl[10:40:1]
    del dl[10:40:-1]
    del dl[10:40:2]
    del dl[10:40:-2]
    dl.destroy()

def test_setitem():
    random.seed(0)
    dl = DiskList(range(0, 100, 10))
    print dl
    values = list(enumerate(range(5, 105, 10)))
    print values
    random.shuffle(values)
    for pos, val in values:
        dl[pos] = val
    dl[-2] = 85
    dl.destroy()

def test_setitem_slice():
    dl = DiskList(range(100))
    dl[:10] = iter(range(10))
    assert dl == list(range(100))
    dl[:10:2] = iter(val * 2 for val in range(5))
    assert dl == list(range(100))
    dl[:50] = range(-50, 50)
    assert dl == list(range(-50, 100))
    dl[:100] = range(50)
    assert dl == list(range(100))
    dl[:] = range(100)
    assert dl == list(range(100))
    dl[90:] = []
    assert dl == list(range(90))
    dl[:10] = []
    assert dl == list(range(10, 90))
    dl.destroy()

def test_setitem_slice_aliasing():
    dl = DiskList([0])
    dl[1:1] = dl
    assert dl == [0, 0]
    dl.destroy()

def test_setitem_empty_slice():
    dl = DiskList(['a'])
    dl[1:0] = ['b']
    assert dl == ['a', 'b']
    dl.destroy()

def test_setitem_extended_slice():
    dl = DiskList(range(0, 1000, 10))
    lst = list(range(0, 1000, 10))
    lst[10:90:10] = range(105, 905, 100)
    dl[10:90:10] = range(105, 905, 100)
    assert dl == lst
    dl.destroy()

@raises(ValueError)
def test_setitem_extended_slice_bad1():
    dl = DiskList(range(100))
    dl[20:80:3] = list(range(10))
    dl.destroy()

def test_setitem1():
    dl = DiskList(range(10))
    dl[9] = 0
    assert dl[9] == 0
    dl.destroy()

def test_setitem2():
    dl = DiskList(range(10))
    dl[0] = 10
    assert dl[0] == 10
    dl.destroy()

def test_iter():
    dl = DiskList(range(100))
    itr = iter(dl)
    assert all(tup[0] == tup[1] for tup in zip(range(100), itr))
    dl.destroy()

def test_reversed():
    dl = DiskList(range(100))
    rev = reversed(dl)
    assert all(tup[0] == tup[1] for tup in zip(range(99, -1, -1), rev))
    dl.destroy()

def test_len():
    dl = DiskList()
    for val in range(100):
        dl.append(val)
        assert len(dl) == (val + 1)
    dl.destroy()

def test_copy():
    alpha = DiskList(range(100))
    beta = alpha.copy()
    alpha.append(100)
    assert len(alpha) == 101
    assert len(beta) == 100
    alpha.destroy()
    beta.destroy()

def test_copy_copy():
    import copy
    alpha = DiskList(range(100))
    beta = copy.copy(alpha)
    alpha.append(100)
    assert len(alpha) == 101
    print len(beta)
    assert len(beta) == 100
    alpha.destroy()

def test_count():
    dl = DiskList()
    assert dl.count(0) == 0
    for iii in range(100):
        for jjj in range(iii):
            dl.append(iii)
    for iii in range(100):
        assert dl.count(iii) == iii
    assert dl.count(100) == 0
    dl.destroy()

def test_append():
    dl = DiskList()
    dl.append(0)
    for val in range(1, 10):
        dl.append(val)
    dl.destroy()

def test_append():
    dl = DiskList(range(100))
    dl.append(5)
    dl.destroy()

def test_extend():
    dl = DiskList()
    dl.extend([])
    dl.extend(range(100))
    dl.extend([])
    dl.extend(list(range(100, 200)))
    
    for val in range(200, 300):
        dl.extend([val] * (val - 199))
    dl.destroy()

def test_extend_valueerror1():
    dl = DiskList()
    dl.extend([1, 2, 3, 5, 4, 6])
    dl.destroy()

def test_extend_valueerror2():
    dl = DiskList(range(20))
    dl.extend([17, 18, 19, 20, 21, 22, 23])
    dl.destroy()

def test_insert():
    dl = DiskList(range(10))
    dl.insert(-1, 9)
    dl.insert(-100, 0)
    dl.insert(100, 10)
    dl.destroy()

    dl = DiskList()
    dl.insert(0, 5)
    dl.destroy()

    dl = DiskList(range(5, 15))
    for rpt in range(8):
        dl.insert(0, 4)
    dl.destroy()


    dl = DiskList(range(10))
    dl.insert(8, 8)
    dl.destroy()

def test_insert_insert1():
    dl = DiskList(range(10))
    dl.insert(10, 5)
    dl.destroy()

def test_insert_insert2():
    dl = DiskList(range(10))
    dl.insert(0, 10)
    dl.destroy()

def test_pop():
    dl = DiskList(range(10))
    assert dl.pop() == 9
    assert dl.pop(0) == 0
    assert dl.pop(-2) == 7
    assert dl.pop(4) == 5
    dl.destroy()

@raises(IndexError)
def test_pop_indexerror1():
    dl = DiskList(range(10))
    dl.pop(-11)
    dl.destroy()

@raises(IndexError)
def test_pop_indexerror2():
    dl = DiskList(range(10))
    dl.pop(10)
    dl.destroy()

@raises(IndexError)
def test_pop_indexerror3():
    dl = DiskList()
    dl.pop()
    dl.destroy()

def test_index():
    dl = DiskList(range(100))
    for val in range(100):
        assert val == dl.index(val)
    assert dl.index(99, 0, 1000) == 99
    dl.destroy()

    dl = DiskList((0 for rpt in range(100)))
    for start in range(100):
        for stop in range(start, 100):
            assert dl.index(0, start, stop + 1) == start
    for start in range(100):
        assert dl.index(0, -(100 - start)) == start
    assert dl.index(0, -1000) == 0
    dl.destroy()


@raises(ValueError)
def test_index_valueerror1():
    dl = DiskList([0] * 10)
    dl.index(0, 10)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror2():
    dl = DiskList([0] * 10)
    dl.index(0, 0, -10)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror3():
    dl = DiskList([0] * 10)
    dl.index(0, 7, 3)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror4():
    dl = DiskList([0] * 10)
    dl.index(1)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror5():
    dl = DiskList()
    dl.index(1)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror6():
    dl = DiskList(range(10))
    dl.index(3, 5)
    dl.destroy()

@raises(ValueError)
def test_index_valueerror7():
    dl = DiskList([0] * 10 + [2] * 10)
    dl.index(1, 0, 10)
    dl.destroy()

def test_mul():
    this = DiskList(range(10))
    that = this * 5
    assert this == list(range(10))
    assert that == sorted(list(range(10)) * 5)
    assert this != that
    this.destroy()

def test_imul():
    this = DiskList(range(10))
    this *= 5
    assert this == sorted(list(range(10)) * 5)
    this.destroy()

def test_op_add():
    this = DiskList(range(10))
    assert (this + this + this) == (this * 3)
    that = DiskList(range(10))
    that += that
    that += that
    assert that == (this * 4)
    this.destroy()
    that.destroy()

def test_eq():
    this = DiskList(range(10))
    assert this == list(range(10))
    assert not (this == list(range(9)))
    this.destroy()

def test_ne():
    this = DiskList(range(10))
    assert this != list(range(9))
    assert this != tuple(range(11))
    assert this != [0, 1, 2, 3, 3, 5, 6, 7, 8, 9]
    assert this != (val for val in range(10))
    assert this != set()
    this.destroy()

def test_lt():
    this = DiskList(range(10, 15))
    assert this < [10, 11, 13, 13, 14]
    assert this < [10, 11, 12, 13, 14, 15]
    assert this < [11]
    this.destroy()

def test_le():
    this = DiskList(range(10, 15))
    assert this <= [10, 11, 12, 13, 14]
    assert this <= [10, 11, 12, 13, 14, 15]
    assert this <= [10, 11, 13, 13, 14]
    assert this <= [11]
    this.destroy()

def test_gt():
    this = DiskList(range(10, 15))
    assert this > [10, 11, 11, 13, 14]
    assert this > [10, 11, 12, 13]
    assert this > [9]
    this.destroy()

def test_ge():
    this = DiskList(range(10, 15))
    assert this >= [10, 11, 12, 13, 14]
    assert this >= [10, 11, 12, 13]
    assert this >= [10, 11, 11, 13, 14]
    assert this >= [9]
    this.destroy()

def test_repr():
    this = DiskList(range(10))
    assert repr(this) == 'DiskList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'
    this.destroy()

#def test_repr_recursion():
#    this = DiskList([[1], [2], [3], [4]])
#    this._lists[-1].append(this)
#    assert repr(this) == 'DiskList([[1], [2], [3], [4], ...])'
#    this.destroy()

def test_repr_subclass():
    class CustomDiskList(DiskList):
        pass
    this = CustomDiskList([1, 2, 3, 4])
    assert repr(this) == 'CustomDiskList([1, 2, 3, 4])'
    this.destroy()

def test_pickle():
    import pickle
    alpha = DiskList(range(100))
    beta = pickle.loads(pickle.dumps(alpha))
    assert alpha == beta
    alpha.destroy()

if __name__ == '__main__':
    import nose
    nose.main()
