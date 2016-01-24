from .base import SwaggerBase


class Resource(SwaggerBase):
    def __init__(self, resource):
        required_fields = {
            'path': {'type': basestring},
        }
        optional_fields = {
            'description': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, resource)
