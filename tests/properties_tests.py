from swagger.properties import Property, Properties

from nose.tools import raises, assert_equals, assert_is_instance


class TestProperties(object):
    def test_properties(self):
        props = Properties({'id': {'type': 'integer', 'format': 'int64'},
                            'name': {'type': 'string', 'description': 'Name'}})
        assert_is_instance(props, Properties)
        for key, value in props.properties.iteritems():
            assert_is_instance(value, Property)

        assert_equals(props.properties['name'].description, 'Name')
