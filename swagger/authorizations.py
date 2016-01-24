from .base import SwaggerBase
from .authorization import Authorization
from .exceptions import SwaggerTypeError


class Authorizations(SwaggerBase):
    def __init__(self, authorizations):
        if not isinstance(authorizations, dict):
            raise SwaggerTypeError("Mapping type was expected for Authorizations")

        self.authorizations = {}
        for name, auth in authorizations.iteritems():
            self.authorizations[name] = Authorization(auth)
