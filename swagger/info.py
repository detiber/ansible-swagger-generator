from .base import SwaggerBase


class Info(SwaggerBase):
    def __init__(self, info):
        required_fields = {
            'title': {'type': basestring},
            'description': {'type': basestring}
        }
        optional_fields = {
            'termsOfServiceUrl': {'type': basestring},
            'contact': {'type': basestring},
            'license': {'type': basestring},
            'licenseUrl': {'type': basestring}
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, info)
