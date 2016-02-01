import json
from .exceptions import SwaggerFieldError, SwaggerTypeError, SwaggerValueError
from six import iteritems, string_types

try:  # pragma: no cover
    from collections import MutableSequence
    from UserDict import IterableUserDict as UserDict
except ImportError:  # pragma: no cover
    from collections.abc import MutableSequence
    from collections import UserDict


class SwaggerBase(object):
    @staticmethod
    def cast_type(val, to_type):
        try:
            return val if isinstance(val, to_type) else to_type(val)
        except ValueError:
            raise SwaggerValueError("Value: {0} is not of type: {1}".format(val, to_type))


class SwaggerField(SwaggerBase):
    def __init__(self, f_type, required=False, subtype=None):
        self.required = required
        self.type = f_type
        if issubclass(f_type, SwaggerList) or issubclass(f_type, SwaggerDict):
            if subtype is None:
                raise SwaggerTypeError("subtype is required for type: {0}".format(f_type))
            self.subtype = subtype

    def cast_value(self, data):
        if isinstance(data, self.type):
            return data
        elif issubclass(self.type, (SwaggerList, SwaggerDict)):
            return self.type(data, self.subtype)
        else:
            return self.cast_type(data, self.type)


class SwaggerObject(SwaggerBase, UserDict):
    def __init__(self, data_in, fields):
        self.fields = SwaggerDict(fields, SwaggerField)
        self.keys = set([name for name in self.fields])
        self.required_keys = set([name for name, field in iteritems(self.fields) if field.required])
        self.data = {}

        if isinstance(data_in, string_types):
            data_in = json.loads(data_in)

        keys_in = set(list(data_in))

        if not self.required_keys <= keys_in:
            missing = self.required_keys - keys_in
            raise SwaggerFieldError("Required fields: {0} missing".format(", ".join(missing)))

        if not keys_in <= self.keys:
            unknown = self.keys - keys_in
            raise SwaggerFieldError("Unexpected fields: {0} found".format(", ".join(unknown)))

        data = {}
        for key, value in iteritems(data_in):
            data[key] = self.fields[key].cast_value(value)

        self.update(data)

    def __setitem__(self, key, item):
        if key not in self.keys:
            raise SwaggerFieldError("Invalid field: {0}".format(key))
        UserDict.__setitem__(self, key, self.fields[key].cast_value(item))

    def __delitem__(self, key):
        if key in self.required_keys:
            raise SwaggerFieldError("Cannot delete required field: {0}".format(key))
        UserDict.__delitem__(self, key)


class SwaggerList(SwaggerBase, MutableSequence):
    def __init__(self, data, data_type):
        if data is None:
            data = []
        self.type = data_type
        self.data = [self.cast_type(x, self.type) for x in data]

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = self.cast_type(value, self.type)

    def __delitem__(self, index):
        del self.data[index]

    def insert(self, index, value):
        self.data.insert(index, self.cast_type(value, self.type))

    def __len__(self):
        return len(self.data)


class SwaggerDict(SwaggerBase, UserDict):
    def __init__(self, data, data_type):
        self.type = data_type
        UserDict.__init__(self, data)
        for key, value in iteritems(self.data):
            self.data[key] = self.cast_type(value, self.type)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, self.cast_type(item, self.type))
