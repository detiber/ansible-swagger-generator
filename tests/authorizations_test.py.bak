from swagger.authorizations import Authorizations, Authorization, \
                                   OauthScope, OauthGrantTypes, \
                                   OauthGrantImplicit, \
                                   OauthAuthorizationCode, \
                                   OauthLoginEndpoint, \
                                   OauthTokenRequestEndpoint, \
                                   OauthTokenEndpoint
from swagger.exceptions import SwaggerFieldError, SwaggerTypeError

from nose.tools import raises, assert_equals, assert_is_instance, \
                       assert_is_none


class TestAuthorizations(object):
    @raises(SwaggerTypeError)
    def test_invalid_authorizations(self):
        Authorizations('blue')

    def test_valid_authorizations(self):
        auth = Authorizations({"basic": {"type": "basicAuth"}})
        assert_is_instance(auth.authorizations, dict)
        assert_equals(auth.authorizations.keys()[0], 'basic')
        assert_is_instance(auth.authorizations['basic'], Authorization)


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


class TestOauthGrantImplicit(object):
    def test_minimal(self):
        implicit = OauthGrantImplicit(
            {
                "loginEndpoint": {
                    "url": "http://example.com/oauth/dialog",
                }
            }
        )
        assert_is_instance(implicit.loginEndpoint, OauthLoginEndpoint)

    def test_full(self):
        implicit = OauthGrantImplicit(
            {
                "loginEndpoint": {
                    "url": "http://example.com/oauth/dialog",
                },
                "tokenName": "access_token"
            }
        )
        assert_is_instance(implicit.loginEndpoint, OauthLoginEndpoint)
        assert_equals(implicit.tokenName, 'access_token')

    @raises(SwaggerFieldError)
    def test_no_request_endpoint(self):
        OauthAuthorizationCode(
            {
                "tokenEndpoint": {
                    "url": "http://example.com/oauth/token",
                }
            }
        )


class TestOauthAuthorizationCode(object):
    def test_valid(self):
        endpoint = OauthAuthorizationCode(
            {
                "tokenRequestEndpoint": {
                    "url": "http://example.com/oauth/requestToken",
                },
                "tokenEndpoint": {
                    "url": "http://example.com/oauth/token",
                }
            }
        )
        assert_is_instance(endpoint.tokenRequestEndpoint,
                          OauthTokenRequestEndpoint)
        assert_is_instance(endpoint.tokenEndpoint, OauthTokenEndpoint)

    @raises(SwaggerFieldError)
    def test_no_request_endpoint(self):
        OauthAuthorizationCode(
            {
                "tokenEndpoint": {
                    "url": "http://example.com/oauth/token",
                }
            }
        )

    @raises(SwaggerFieldError)
    def test_no_token_endpoint(self):
        OauthAuthorizationCode(
            {
                "tokenRequestEndpoint": {
                    "url": "http://example.com/oauth/requestToken",
                }
            }
        )


class TestOauthLoginEndpoint(object):
    def test_valid(self):
        endpoint = OauthLoginEndpoint({'url': 'http://example.com/oauth/dialog'})
        assert_equals(endpoint.url, 'http://example.com/oauth/dialog')

    @raises(SwaggerFieldError)
    def test_no_url(self):
         OauthLoginEndpoint({})


class TestOauthTokenRequestEndpoint(object):
    def test_minimal(self):
        endpoint = OauthTokenRequestEndpoint(
            {
                "url": "http://example.com/oauth/requestToken",
            }
        )
        assert_equals(endpoint.url, "http://example.com/oauth/requestToken")

    def test_full(self):
        endpoint = OauthTokenRequestEndpoint(
            {
                "url": "http://example.com/oauth/requestToken",
                "clientIdName": "client_id",
                "clientSecretName": "client_secret"
            }
        )
        assert_equals(endpoint.url, "http://example.com/oauth/requestToken")
        assert_equals(endpoint.clientIdName, "client_id")
        assert_equals(endpoint.clientSecretName, "client_secret")


class TestOauthTokenEndpoint(object):
    def test_minimal(self):
        endpoint = OauthTokenEndpoint(
            {
                "url": "http://example.com/oauth/token",
            }
        )
        assert_equals(endpoint.url, "http://example.com/oauth/token")

    def test_full(self):
        endpoint = OauthTokenEndpoint(
            {
                "url": "http://example.com/oauth/token",
                "tokenName": "access_code"
            }
        )
        assert_equals(endpoint.url, "http://example.com/oauth/token")
        assert_equals(endpoint.tokenName, "access_code")


class TestOauthGrantTypes(object):
    @raises(SwaggerTypeError)
    def test_invalid_grants(self):
        OauthGrantTypes(9)

    @raises(SwaggerFieldError)
    def test_no_grants(self):
        OauthGrantTypes({})

    def test_implicit(self):
        grants = OauthGrantTypes(
            {
                "implicit": {
                    "loginEndpoint": {
                        "url": "http://example.com/oauth/dialog",
                    }
                }
            }
        )
        assert_is_instance(grants.implicit, OauthGrantImplicit)

    def test_auth_code(self):
        grants = OauthGrantTypes(
            {
                "authorization_code": {
                    "tokenRequestEndpoint": {
                        "url": "http://example.com/oauth/requestToken",
                    },
                    "tokenEndpoint": {
                        "url": "http://example.com/oauth/token",
                    }
                }
            }
        )
        assert_is_instance(grants.authorization_code, OauthAuthorizationCode)

    def test_all(self):
        grants = OauthGrantTypes(
            {
                "implicit": {
                    "loginEndpoint": {
                        "url": "http://example.com/oauth/dialog",
                    }
                },
                "authorization_code": {
                    "tokenRequestEndpoint": {
                        "url": "http://example.com/oauth/requestToken",
                    },
                    "tokenEndpoint": {
                        "url": "http://example.com/oauth/token",
                    }
                }
            }
        )
        assert_is_instance(grants.implicit, OauthGrantImplicit)
        assert_is_instance(grants.authorization_code, OauthAuthorizationCode)


class TestOauthScope(object):
    def test_no_description(self):
        scope = OauthScope({'scope': 'email'})
        assert_equals(scope.scope, 'email')

    def test_with_description(self):
        scope = OauthScope({'scope': 'email', 'description': 'email'})
        assert_equals(scope.description, 'email')

    @raises(SwaggerFieldError)
    def test_no_scope(self):
        OauthScope({'description': 'email'})
