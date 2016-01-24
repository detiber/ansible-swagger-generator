from swagger.authorizations import Authorizations
from swagger.authorization import Authorization
from swagger.exceptions import SwaggerTypeError

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

