from .base import SwaggerBase
from .resource import Resource
from .info import Info
from .authorizations import Authorizations


class ResourceListing(SwaggerBase):
    def __init__(self, resource_list):
        required_fields = {
            'swaggerVersion': {'type': basestring},
            'apis': {'type': list, 'subtype': Resource}
        }
        optional_fields = {
            'apiVersion': {'type': basestring},
            'info': {'type': Info},
            'authorizations': {'type': Authorizations}
        }
        SwaggerBase.__init__(self, required_fields, optional_fields,
                             resource_list)
