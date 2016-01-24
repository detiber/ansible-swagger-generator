from swagger.authorization_oauth import OauthScope, OauthGrantTypes, \
                                        OauthGrantImplicit, \
                                        OauthAuthorizationCode, \
                                        OauthLoginEndpoint, \
                                        OauthTokenRequestEndpoint, \
                                        OauthTokenEndpoint
from swagger.exceptions import SwaggerFieldError, SwaggerTypeError

from nose.tools import raises, assert_equals, assert_is_instance, \
                       assert_is_none

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

