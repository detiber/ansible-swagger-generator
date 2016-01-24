from swagger.authorization import Authorization
from swagger.exceptions import SwaggerFieldError, SwaggerTypeError
from swagger.oauth_grant_types import OauthGrantTypes
from swagger.oauth_scope import OauthScope

from nose.tools import raises, assert_equals, assert_is_instance, \
                       assert_is_none

OAUTH_DOC_NO_SCOPES = {
    "type": "oauth2",
    "grantTypes": {
        "implicit": {
            "loginEndpoint": {"url": "http://example.com/oauth/dialog"}
        }
    }
}

class TestAuthorization(object):
    @raises(SwaggerTypeError)
    def test_invalid_auth_type(self):
        auth = Authorization({'type': 'myAuthType'})

    @raises(SwaggerFieldError)
    def test_invalid_oauth1(self):
        auth_doc = OAUTH_DOC_NO_SCOPES.copy()
        auth_doc['passAs'] = 'header'
        Authorization(auth_doc)

    @raises(SwaggerFieldError)
    def test_invalid_oauth2(self):
        auth_doc = OAUTH_DOC_NO_SCOPES.copy()
        auth_doc['keyName'] = 'blue'
        Authorization(auth_doc)

    @raises(SwaggerFieldError)
    def test_invalid_oauth3(self):
        auth_doc = OAUTH_DOC_NO_SCOPES.copy()
        del auth_doc['grantTypes']
        Authorization(auth_doc)

    def test_valid_oauth_no_scopes(self):
        auth = Authorization(OAUTH_DOC_NO_SCOPES)
        assert_equals(auth.type, 'oauth2')
        assert_is_instance(auth.grantTypes, OauthGrantTypes)
        assert_is_none(getattr(auth, 'scopes', None))

    def test_valid_oauth_with_scopes(self):
        oauth_doc = OAUTH_DOC_NO_SCOPES.copy()
        oauth_doc['scopes'] = [{"scope": "email",
                                "description": "Email Address"}]
        auth = Authorization(oauth_doc)
        assert_equals(auth.type, 'oauth2')
        assert_is_instance(auth.grantTypes, OauthGrantTypes)
        assert_is_instance(auth.scopes, list)
        assert_is_instance(auth.scopes[0], OauthScope)

    def test_valid_api_key_header(self):
        auth = Authorization({'type': 'apiKey', 'keyName': 'green',
                              'passAs': 'header'})
        assert_equals(auth.type, 'apiKey')
        assert_equals(auth.passAs, 'header')
        assert_equals(auth.keyName, 'green')

    def test_valid_api_key_query(self):
        auth = Authorization({'type': 'apiKey', 'keyName': 'green',
                              'passAs': 'query'})
        assert_equals(auth.type, 'apiKey')
        assert_equals(auth.passAs, 'query')
        assert_equals(auth.keyName, 'green')

    @raises(SwaggerFieldError)
    def test_invalid_api_key1(self):
        auth = Authorization({'type': 'apiKey', 'keyName': 'green'})

    @raises(SwaggerFieldError)
    def test_invalid_api_key2(self):
        auth = Authorization({'type': 'apiKey', 'passAs': 'query'})

    @raises(SwaggerFieldError)
    def test_invalid_api_key3(self):
        auth = Authorization({'type': 'apiKey', 'keyName': 'green',
                              'passAs': 'query', 'grantTypes': 'teal'})

    @raises(SwaggerFieldError)
    def test_invalid_api_key3(self):
        auth = Authorization({'type': 'apiKey', 'keyName': 'green',
                              'passAs': 'query', 'scopes': []})

    def test_valid_basic(self):
        auth = Authorization({'type': 'basicAuth'})
        assert_equals(auth.type, 'basicAuth')

    @raises(SwaggerFieldError)
    def test_invalid_basic1(self):
        auth = Authorization({'type': 'basicAuth', 'passAs': 'header'})

    @raises(SwaggerFieldError)
    def test_invalid_basic2(self):
        auth = Authorization({'type': 'basicAuth', 'keyName': 'grey'})

    @raises(SwaggerFieldError)
    def test_invalid_basic3(self):
        auth = Authorization({'type': 'basicAuth', 'scopes': []})

    @raises(SwaggerFieldError)
    def test_invalid_basic4(self):
        auth = Authorization({'type': 'basicAuth', 'grantTypes': 'blue'})
