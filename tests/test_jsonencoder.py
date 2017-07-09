
# -*- coding: utf-8 -*-

from sys import hexversion

import random
import json
#from .context import disktypes
from disktypes import DiskList, JSONDiskTypesEncoder
from itertools import chain
from nose.tools import raises

def test_serialize():
    dl = DiskList(range(100))
    assert range(100) == dl.serialize()
    dl.destroy()

def test_dumps():
    dl = DiskList(range(100))
    assert sorted(json.loads(
        json.dumps(dl, cls=JSONDiskTypesEncoder)
    )) == sorted(range(100))
    dl.destroy()

if __name__ == '__main__':
    import nose
    nose.main()
