import json
from .disklist import DiskList

class JSONDiskTypesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DiskList):
            return obj.serialize()
            #return json.JSONEncoder(obj.serialize())
            # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
