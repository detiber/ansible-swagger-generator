from .base import SwaggerBase, SwaggerObject, SwaggerField
from .exceptions import SwaggerTypeError, SwaggerValueError
from six.moves import UserString
from six import text_type, binary_type, integer_types
from pyrfc3339 import parse
from datetime import datetime
from distutils.util import strtobool
import pytz  # noqa


class SwaggerPrimitive(SwaggerBase):

    FORMATS = []

    def __init__(self, format_str=None, format_required=False):
        self.format_required = format_required
        self.format_str = format_str

        if format_str is None:
            if self.format_required:
                raise SwaggerTypeError("Format is required for this type")
        elif format_str not in self.FORMATS:
            raise SwaggerTypeError("Invalid format: {0}".format(format_str))


class SwaggerString(SwaggerPrimitive, UserString):

    FORMATS = ['byte', 'date', 'date-time']

    def __init__(self, string, format_str=None):
        SwaggerPrimitive.__init__(self, format_str)
        self.data = string
        self.validate_format()

    def validate_format(self):
        if self.format_str is None:
            if not isinstance(self.data, text_type):
                raise SwaggerValueError("Expected unicode value not: {0}".format(type(self.data)))
        elif self.format_str == 'byte':
            if not isinstance(self.data, binary_type):
                raise SwaggerValueError("Expected byte value not: {0}".format(type(self.data)))
        elif self.format_str == 'date':
            try:
                datetime.strptime(self.data, "%Y-%m-%d")
            except ValueError:
                raise SwaggerValueError("Expected date value not: {0}".format(self.data))
        elif self.format_str == 'date-time':
            try:
                parse(self.data)
            except ValueError:
                raise SwaggerValueError("Expected date-time value not: {0}".format(self.data))


class SwaggerInteger(SwaggerPrimitive):

    FORMATS = ['int32', 'int64']

    INT_LIMITS = {'int32': {'max': 2**32, 'min': -(2**32+1)},
                  'int64': {'max': 2**64, 'min': -(2**64+1)}}

    def __init__(self, int_val, format_str=None):
        SwaggerPrimitive.__init__(self, format_str, format_required=True)
        try:
            v = int_val if isinstance(int_val, integer_types) else int(int_val)
            if v < self.INT_LIMITS[format_str]['min'] or v > self.INT_LIMITS[format_str]['max']:
                raise SwaggerValueError("Value: {0} out of range for: {1}".format(v, format_str))
            self.data = v
        except ValueError:
            raise SwaggerValueError("Expected: {0} value not: {1}".format(format_str, int_val))


class SwaggerNumber(SwaggerPrimitive):

    FORMATS = ['float', 'double']

    def __init__(self, num, format_str=None):
        SwaggerPrimitive.__init__(self, format_str, format_required=True)

        # TODO: actually validate num is a float or a double

        if isinstance(num, float):
            self.data = num
        else:
            try:
                self.data = float(num)
            except ValueError:
                raise SwaggerValueError("Expected: {0} value not: {1}".format(format_str, num))


class SwaggerBool(SwaggerPrimitive):

    def __init__(self, bool_val, format_str=None):
        SwaggerPrimitive.__init__(self, format_str)

        if isinstance(bool_val, bool):
            self.data = bool_val
        else:
            try:
                self.data = strtobool(str(bool_val))
            except ValueError:
                raise SwaggerValueError("Expected boolean not: {0}".format(bool_val))


PRIMITIVES = {
    'integer': {
        'type': SwaggerInteger,
        'schema_type': int
    },
    'number': {
        'type': SwaggerNumber,
        'schema_type': float
    },
    'string': {
        'type': SwaggerString,
        'schema_type': text_type
    },
    'boolean': {
        'type': SwaggerBool,
        'schema_type': int
    }
}


class Items(SwaggerObject):
    def __init__(self, data):
        fields = {
            'type': SwaggerField(text_type),
            'format': SwaggerField(text_type),
            '$ref': SwaggerField(text_type),
        }
        SwaggerObject.__init__(self, data, fields)

        if 'type' in self:
            t = self['type']
            if t == 'array':
                raise SwaggerValueError("array is not a valid type for Items Object")
            elif t in PRIMITIVES:
                if 'format' in self:
                    f = self['format']
                    valid_formats = PRIMITIVES[t]['type'].FORMATS
                    if f not in valid_formats:
                        raise SwaggerValueError(
                            "format: {0} not valid for type: {1} expected one of: {2]".format(
                                f, t, ", ".join(valid_formats)
                            )
                        )
            else:
                # TODO: Add validator that type is valid model id
                if 'format' in self:
                    raise SwaggerValueError("format is only valid when type is a primitive")
        else:
            if 'format' in self:
                raise SwaggerValueError("format is only valid when type is a primitive")
            if '$ref' not in self:
                raise SwaggerValueError("$ref is required if type is not present")
            else:
                # TODO: Add validator that $ref references an existing model id
                pass


class DataType(SwaggerObject):
    def __init__(self, data):
        fields = {
            'type': SwaggerField(text_type),
            'format': SwaggerField(text_type),
            '$ref': SwaggerField(text_type),
            'defaultValue': SwaggerField(text_type),
            'enum': SwaggerField(list, subtype=text_type),
            'minimum': SwaggerField(text_type),
            'maximum': SwaggerField(text_type),
            'items': SwaggerField(Items),
            'uniqueItems': SwaggerField(bool),
        }
        SwaggerObject.__init__(self, data, fields)

        if '$ref' in self:
            # TODO: Add validator that $ref references an existing model id
            for key in self:
                if key != '$ref':
                    raise SwaggerValueError("field: {0} not valid when $ref is present".format(key))
        elif 'type' in self:
            t = self['type']
            if t in PRIMITIVES:
                for key in ['items', 'uniqueItems']:
                    if key in self:
                        raise SwaggerValueError("field: {0} not valid for type: {1}".format(key, t))
                if 'format' in self:
                    f = self['format']
                    valid_formats = PRIMITIVES[t]['type'].FORMATS
                    if f not in valid_formats:
                        raise SwaggerValueError(
                            "format: {0} not valid for type: {1} expected one of: {2}".format(
                                f, t, ", ".join(valid_formats)
                            )
                        )
                if 'defaultValue' in self:
                    try:
                        f = self['format'] if 'format' in self else None
                        PRIMITIVES[t]['type'](self['defaultValue'], f)
                    except SwaggerValueError:
                        type_str = "type: {0}".format(t)
                        if 'format' in self:
                            type_str += " format: {0}".format(self['format'])
                        raise SwaggerValueError(
                            "defaultValue: {0} is not valid for {1}".format(self['defaultValue'], type_str)
                        )

                if t == 'string':
                    for key in ['minimum', 'maximum']:
                        if key in self:
                            raise SwaggerValueError("field: {0} not valid for type: {1}".format(key, t))
                    if 'enum' in self and 'defaultValue' in self:
                        if self['defaultValue'] not in self['enum']:
                            raise SwaggerValueError(
                                "defaultValue: {0} not in  enum: {1}".format(
                                    self['defaultValue'], self['enum']
                                )
                            )
                elif t in ['integer', 'number']:
                    if 'enum' in self:
                        raise SwaggerValueError("enum not valid for type: {1}".format(key, t))
                    for key in ['minimum', 'maximum']:
                        if key in self:
                            try:
                                PRIMITIVES[t]['type'](self[key], f)
                            except SwaggerValueError:
                                type_str = "type: {0}".format(t)
                                if 'format' in self:
                                    type_str += " format: {0}".format(self['format'])
                                raise SwaggerValueError(
                                    "{0}: {1} is not valid for {2}".format(
                                        key, self[key], type_str
                                    )
                                )
                        if 'defaultValue' in self and key in self:
                            default = self['defaultValue']
                            value = self[key]
                            if key == 'minimum' and default < value:
                                raise SwaggerValueError(
                                    "defaultValue: {0} less than minimum: {1}".format(default, value)
                                )
                            if key == 'maximum' and default > value:
                                raise SwaggerValueError(
                                    "defaultValue: {0} greater than maximum: {1}".format(default, value)
                                )
                else:
                    for key in ['enum', 'minimum', 'maximum']:
                        if key in self:
                            raise SwaggerValueError("field: {0} not valid for type: {1}".format(key, t))
            elif t == 'array':
                for key in self:
                    if key not in ['type', 'items', 'uniqueItems']:
                        raise SwaggerValueError("field: {0} not valid for array type".format(key))
                if 'items' not in self:
                    raise SwaggerValueError("items is required when type is array")
            else:
                # TODO: Add validator that type is valid model id
                for key in self:
                    if key != 'type':
                        raise SwaggerValueError("field: {0} not valid when  type is a Model".format(key))
        else:
            raise SwaggerValueError("Either type or $ref is required for Data  Type")

        # TODO: Add validator that enum is only present if type is string
        # TODO: Add validator that minimum, maximum are present iff type is
        #       integer or number
        # TODO: Add validator that minimum, maximum are valid for their type

# class DataType(SwaggerBase):
#    def __init__(self, data_type, addtl_required, addtl_optional):
#        required_fields = addtl_required if addtl_required is not None else {}
#        optional_fields = addtl_optional if addtl_optional is not None else {}
#
#        if '$ref' in data_type:
#            required_fields['$ref'] = {'type': basestring}
#        elif 'type' in data_type:
#            req_type = data_type['type']
#            required_fields['type'] = {'type': basestring}
#            if req_type == 'array':
#                required_fields['items'] = {'type': Items}
#                optional_fields['uniqueItems'] = {'type': bool}
#
#            elif req_type in PRIMITIVES:
#                expected_type = PRIMITIVES[req_type]['type']
#                optional_fields['format'] = {'type': basestring}
#                optional_fields['defaultValue'] = {'type': expected_type}
#                req_format = data_type.get('format')
#                req_default = data_type.get('defaultValue')
#                valid_formats = PRIMITIVES[req_type]['formats']
#                if req_format is not None and req_format not in valid_formats:
#                    raise SwaggerTypeError(
#                        "Invalid format: {0} expected one of: {1}".format(req_format, ",".join(valid_formats))
#                    )
#                if req_type == 'string':
#                    optional_fields['enum'] = {'type': list, 'subtype': basestring}
#                    req_enum = data_type.get('enum')
#                    if req_enum is not None and req_default is not None and req_default not in req_enum:
#                        raise SwaggerTypeError(
#                            "Invalid defaultValue: {0} expected one of: {1}".format(req_default, ",".join(req_enum))
#                        )
#                elif req_type in ('number', 'integer'):
#                    optional_fields['minimum'] = {'type': basestring}
#                    optional_fields['maximum'] = {'type': basestring}
#                    req_min = data_type.get('minimum')
#                    req_max = data_type.get('maximum')
#                    if req_default is not None:
#                        if req_min is not None and req_default < expected_type(req_min):
#                            raise SwaggerTypeError(
#                                "Invalid defaultValue: {0} expected a value greater than or equal to: {1}".format(
#                                    req_default, req_min
#                                )
#                            )
#                        if req_max is not None and req_default > expected_type(req_max):
#                            raise SwaggerTypeError(
#                                "Invalid defaultValue: {0} expected a value less than or equal to: {1}".format(
#                                    req_default, req_max
#                                )
#                            )
#
#        else:
#            raise SwaggerFieldError("Either type or $ref are required")
#
#        SwaggerBase.__init__(self, required_fields, optional_fields, data_type)
