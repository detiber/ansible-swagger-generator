from .base import SwaggerBase
from .exceptions import SwaggerTypeError, SwaggerFieldError


class OauthTokenEndpoint(SwaggerBase):
    def __init__(self, endpoint):
        required_fields = {
            'url': {'type': basestring},
        }
        optional_fields = {
            'tokenName': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, endpoint)


class OauthTokenRequestEndpoint(SwaggerBase):
    def __init__(self, endpoint):
        required_fields = {
            'url': {'type': basestring},
        }
        optional_fields = {
            'clientIdName': {'type': basestring},
            'clientSecretName': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, endpoint)


class OauthLoginEndpoint(SwaggerBase):
    def __init__(self, endpoint):
        required_fields = {
            'url': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, {}, endpoint)


class OauthAuthorizationCode(SwaggerBase):
    def __init__(self, auth_code):
        required_fields = {
            'tokenRequestEndpoint': {'type': OauthTokenRequestEndpoint},
            'tokenEndpoint': {'type': OauthTokenEndpoint},
        }
        SwaggerBase.__init__(self, required_fields, {}, auth_code)


class OauthGrantImplicit(SwaggerBase):
    def __init__(self, grant):
        required_fields = {
            'loginEndpoint': {'type': OauthLoginEndpoint}
        }
        optional_fields = {
            'tokenName': {'type': basestring}
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, grant)


class OauthGrantTypes(SwaggerBase):
    def __init__(self, grant_types):
        if not isinstance(grant_types, dict):
            raise SwaggerTypeError("Mapping type was expected for OauthGrantTypes")

        if 'implicit' not in grant_types and 'authorization_code' not in grant_types:
            raise SwaggerFieldError("Either implicit or authorization_code need to be specified for grantTypes")

        optional_fields = {
            'implicit': {'type': OauthGrantImplicit},
            'authorization_code': {'type': OauthAuthorizationCode}
        }
        SwaggerBase.__init__(self, {}, optional_fields, grant_types)


class OauthScope(SwaggerBase):
    def __init__(self, scope):
        required_fields = {
            'scope': {'type': basestring},
        }
        optional_fields = {
            'description': {'type': basestring},
        }
        SwaggerBase.__init__(self, required_fields, optional_fields, scope)


class Authorization(SwaggerBase):
    def __init__(self, auth):
        required_fields = {
            'type': {
                'type': basestring,
                'values': ['basicAuth', 'apiKey', 'oauth2']
            }
        }
        optional_fields = {}

        if 'type' in auth:
            if auth['type'] == 'apiKey':
                required_fields['passAs'] = {
                    'type': basestring,
                    'values': ['header', 'query']
                }
                required_fields['keyName'] = {'type': basestring}
            elif auth['type'] == 'oauth2':
                required_fields['grantTypes'] = {'type': OauthGrantTypes}
                optional_fields['scopes'] = {
                    'type': list,
                    'subtype': OauthScope
                }

        SwaggerBase.__init__(self, required_fields, optional_fields, auth)


class Authorizations(SwaggerBase):
    def __init__(self, authorizations):
        if not isinstance(authorizations, dict):
            raise SwaggerTypeError("Mapping type was expected for Authorizations")

        self.authorizations = {}
        for name, auth in authorizations.iteritems():
            self.authorizations[name] = Authorization(auth)
