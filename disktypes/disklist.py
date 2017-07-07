import os, shutil, uuid

class DiskList(object):
    def __init__(self, iterable=(), location=None, _pickle=None):
        self.location = location or "disklist_store_" + str(uuid.uuid4())
        self.id_order = []
        self.id_counter=0

        if _pickle:
            self.pickle = _pickle
        else:
            import cPickle
            self.pickle = cPickle

        os.mkdir(self.location)

        if iterable:
            for el in iterable:
                self.append(el)

    def destroy(self):
        self.id_order = []
        self.id_counter = 0
        shutil.rmtree(self.location)

    def __iadd__(self, iterable):
        if type(iterable) != list:
            raise TypeError(
                'can only concatenate list (not "{}") to list'.format(type(iterable))
            )
        for el in iterable:
            self.append(el)
        
    def __contains__(self, obj):
        for el in self:
            if el == obj:
                return True
        return False

    def __delitem__(self, idx):
        if isinstance(idx, slice):
            for ii in xrange(
                *idx.indices(
                    len(self.id_order)
                )
            ):
                del self[ii] 
        elif isinstance(idx, int):
            os.remove(self._get_path(self.id_order[idx]))
            del self.id_order[idx]
        else:
            raise TypeError, "Invalid argument type."

    def __delslice__(self, i, j):
        raise NotImplementedError("this method is not implemented")

    def __eq__(*_):
        raise NotImplementedError("this method is not implemented")

    def __ge__(*_):
        raise NotImplementedError("this method is not implemented")

    def _return_item(self, idx):
        my_id = self.id_order[idx]
        return self.pickle.load(open(self._get_path(my_id), "rb" ))
        
    def __getitem__(self, key):
        if isinstance(key, slice):
            return [
                self._return_item(ii) for ii in xrange(
                    *key.indices(
                        len(self.id_order)
                    )
                )
            ]
        elif isinstance(key, int):
            if key < 0:
                key += len(self.id_order)
            if key < 0 or key >= len(self):
                raise IndexError, "The index (%d) is out of range."%key
            return self._return_item(key)
        else:
            raise TypeError, "Invalid argument type."

    def __gt__(*_):
        raise NotImplementedError("this method is not implemented")
    def __add__(*_):
        raise NotImplementedError("this method is not implemented")
    def __imul__(*_):
        raise NotImplementedError("this method is not implemented")

    def __iter__(self):
        idx = 0
        while idx < len(self.id_order):
            yield self[idx]
            idx += 1

    def __le__(*_):
        raise NotImplementedError("this method is not implemented")

    def __len__(self):
        return len(self.id_order)

    def __lt__(*_):
        raise NotImplementedError("this method is not implemented")
    def __mul__(*_):
        raise NotImplementedError("this method is not implemented")
    def __ne__(*_):
        raise NotImplementedError("this method is not implemented")

    def __repr__(self):
        return "DiskList({})".format([val for val in self])

    def __reversed__(self):
        idx = len(self.id_order)
        while idx > 0:
            idx -= 1
            yield self[idx]

    def __rmul__(*_):
        raise NotImplementedError("this method is not implemented")

    def __setitem__(self, idx, obj):
        print "idx", idx, "len", len(self.id_order)
        if idx >= len(self.id_order):
            raise IndexError("list assignment index out of range")
        os.remove(self._get_path(self.id_order[idx]))
        del self.id_order[idx]
        self.insert(idx, obj) 
 
    def __setslice__(*_):
        raise NotImplementedError("this method is not implemented")

    def __sizeof__(*_):
        raise NotImplementedError("this method is not implemented")

    def _get_path(self, _id):
        return os.path.sep.join([self.location, "{}.pck".format(_id)])

    def append(self, obj):
        self.id_counter += 1
        new_id = self.id_counter
        self.pickle.dump(obj, open(self._get_path(new_id), "wb" ))
        self.id_order.append(new_id)

    def add(self, obj):
        return self.append(obj)

    def count(self, value):
        count = 0
        for el in self:
            if el == value:
                count += 1
        return count

    def extend(self, iterable):
        for el in iterable:
            self.append(el)

    def index(self, value, start=0, stop=None):
        #idx = 0
        if stop == None:
            stop = len(self.id_order)
        pos = start
        for _id in self.id_order[start:stop]:
            if self.pickle.load(open(self._get_path(_id), "rb" )) == value:
                return pos
            pos += 1
        raise ValueError("{} is not in the list".format(value))

    def insert(self, idx, obj):
        self.id_counter += 1
        new_id = self.id_counter
        self.pickle.dump(obj, open(self._get_path(new_id), "wb" ))
        self.id_order.insert(idx, new_id)

    def pop(self, idx=None):
        if idx == None:
            idx = len(self.id_order) - 1
        value = self[idx]
        del self[idx]
        return value

    def remove(self, value):
        idx = self.index(value)
        print "remove idx", idx
        del self[idx]

    def reverse(self):
        return self.id_order.reverse()

    def sort(*_):
        raise NotImplementedError("this method is not implemented")

    # extra/non list functions
    def copy(self):
        return DiskList(self[:])
