from .base import SwaggerBase


class OauthScope(SwaggerBase):
    def __init__(self, scope):
        required_fields = {
            'scope': {'type': basestring},
        }
        optional_fields = {
            'description': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, scope)
