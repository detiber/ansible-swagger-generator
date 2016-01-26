from .base import SwaggerBase
from .exceptions import SwaggerFieldError, SwaggerTypeError


PRIMITIVES = {
    'integer': {
        'formats': ['int32', 'int64'],
        'type': int
    },
    'number': {
        'formats': ['float', 'double'],
        'type': float
    },
    'string': {
        'formats': ['byte', 'date', 'date-time'],
        'type': basestring
    },
    'boolean': {
        'formats': [],
        'type': bool
    }
}


class Items(SwaggerBase):
    def __init__(self, items):
        required_fields = {}
        optional_fields = {}

        if '$ref' in items:
            required_fields['$ref'] = {'type': basestring}
        elif 'type' in items:
            required_fields['type'] = {'type': basestring}
            if items['type'] in PRIMITIVES:
                optional_fields['format'] = {'type': basestring}
            if items['type'] == 'array':
                raise SwaggerTypeError("Type: array is not valid for Items")
        else:
            raise SwaggerFieldError("Either type or $ref are required")

        SwaggerBase.__init__(self, required_fields, optional_fields, items)


class DataType(SwaggerBase):
    def __init__(self, data_type, addtl_required, addtl_optional):
        required_fields = addtl_required if addtl_required is not None else {}
        optional_fields = addtl_optional if addtl_optional is not None else {}

        if '$ref' in data_type:
            required_fields['$ref'] = {'type': basestring}
        elif 'type' in data_type:
            req_type = data_type['type']
            required_fields['type'] = {'type': basestring}
            if req_type == 'array':
                required_fields['items'] = {'type': Items}
                optional_fields['uniqueItems'] = {'type': bool}

            elif req_type in PRIMITIVES:
                expected_type = PRIMITIVES[req_type]['type']
                optional_fields['format'] = {'type': basestring}
                optional_fields['defaultValue'] = {'type': expected_type}
                req_format = data_type.get('format')
                req_default = data_type.get('defaultValue')
                valid_formats = PRIMITIVES[req_type]['formats']
                if req_format is not None and req_format not in valid_formats:
                    raise SwaggerTypeError(
                        "Invalid format: {0} expected one of: {1}".format(req_format, ",".join(valid_formats))
                    )
                if req_type == 'string':
                    optional_fields['enum'] = {'type': list, 'subtype': basestring}
                    req_enum = data_type.get('enum')
                    if req_enum is not None and req_default is not None and req_default not in req_enum:
                        raise SwaggerTypeError(
                            "Invalid defaultValue: {0} expected one of: {1}".format(req_default, ",".join(req_enum))
                        )
                elif req_type in ('number', 'integer'):
                    optional_fields['minimum'] = {'type': basestring}
                    optional_fields['maximum'] = {'type': basestring}
                    req_min = data_type.get('minimum')
                    req_max = data_type.get('maximum')
                    if req_default is not None:
                        if req_min is not None and req_default < expected_type(req_min):
                            raise SwaggerTypeError(
                                "Invalid defaultValue: {0} expected a value greater than or equal to: {1}".format(
                                    req_default, req_min
                                )
                            )
                        if req_max is not None and req_default > expected_type(req_max):
                            raise SwaggerTypeError(
                                "Invalid defaultValue: {0} expected a value less than or equal to: {1}".format(
                                    req_default, req_max
                                )
                            )

        else:
            raise SwaggerFieldError("Either type or $ref are required")

        SwaggerBase.__init__(self, required_fields, optional_fields, data_type)
