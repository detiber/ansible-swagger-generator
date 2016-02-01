from .base import SwaggerDict
from .data_type import DataType


class Property(DataType):
    def __init__(self, prop):

        optional_fields = {
            'description': {'type': basestring},
        }
        DataType.__init__(self, prop, None, optional_fields)


class Properties(SwaggerDict):
    def __init__(self, properties):
        SwaggerDict.__init__(self, properties, Property)
