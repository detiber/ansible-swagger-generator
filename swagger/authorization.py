from .base import SwaggerBase
from .oauth_grant_types import OauthGrantTypes
from .oauth_scope import OauthScope

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
