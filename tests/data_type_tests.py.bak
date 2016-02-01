from swagger.data_type import DataType, Items, PRIMITIVES
from swagger.exceptions import SwaggerFieldError, SwaggerTypeError

from nose.tools import raises, assert_equals, assert_is_instance


class TestItems(object):
    @raises(SwaggerFieldError)
    def test_no_ref_no_type(self):
        Items({})

    def test_valid_primitives(self):
        for t, type_props in PRIMITIVES.iteritems():
            items = Items({'type': t})
            assert_equals(items.type, t)
            for f in type_props['formats']:
                items = Items({'type': t, 'format': f})
                assert_equals(items.type, t)
                assert_equals(items.format, f)

    def test_ref(self):
        dt = Items({'$ref': 'MyModel'})
        assert_equals(getattr(dt, '$ref'), 'MyModel')

    @raises(SwaggerTypeError)
    def test_invalid_type(self):
        Items({'type': 'array'})


class TestDataType(object):

    @raises(SwaggerFieldError)
    def test_no_ref_no_type(self):
        DataType({}, {}, {})

    def test_valid_primitives(self):
        for t, type_props in PRIMITIVES.iteritems():
            dt = DataType({'type': t}, {}, {})
            assert_equals(dt.type, t)
            for f in type_props['formats']:
                dtf = DataType({'type': t, 'format': f}, {}, {})
                assert_equals(dtf.type, t)
                assert_equals(dtf.format, f)

    @raises(SwaggerTypeError)
    def test_invalid_primitive(self):
        dt = DataType({'type': 'string', 'format': 'blue'}, {}, {})

    def test_ref(self):
        dt = DataType({'$ref': 'MyModel'}, {}, {})
        assert_equals(getattr(dt, '$ref'), 'MyModel')

    @raises(SwaggerTypeError)
    def test_invalid_default_enum(self):
        DataType({'type': 'string', 'enum': ['blue', 'green'], 'defaultValue': 'orange'}, {}, {})

    @raises(SwaggerFieldError)
    def test_invalid_type_enum(self):
        DataType({'type': 'integer', 'enum': [1, 2]}, {}, {})

    def test_enum(self):
        dt = DataType({'type': 'string', 'enum': ['blue', 'green']}, {}, {})
        assert_equals(dt.type, 'string')
        assert_equals(dt.enum, ['blue', 'green'])

    @raises(SwaggerTypeError)
    def test_invalid_default(self):
        DataType({'type': 'string', 'defaultValue': 3}, {}, {})

    def test_default_values(self):
        dv_tests = {'integer': 9, 'number': 3.5, 'string': 'blue', 'boolean': True}
        for t, dv in dv_tests.iteritems():
            dt = DataType({'type': t, 'defaultValue': dv}, {}, {})
            assert_equals(dt.type, t)
            assert_equals(dt.defaultValue, dv)

    def test_min_max_with_default(self):
        dv_tests = {'integer': {'max': '10', 'min': '5', 'default': 7},
                    'number': {'max': '30.5', 'min': '10.2', 'default': 20.5}}
        for t, values in dv_tests.iteritems():
            dt = DataType({'type': t, 'minimum': values['min'],
                           'maximum': values['max'],
                           'defaultValue': values['default']}, {}, {})

    @raises(SwaggerTypeError)
    def test_invalid_default_min_int(self):
        DataType({'type': 'integer', 'minimum': '5', 'defaultValue': 4}, {}, {})

    @raises(SwaggerTypeError)
    def test_invalid_default_max_int(self):
        DataType({'type': 'integer', 'maximum': '5', 'defaultValue': 6}, {}, {})

    @raises(SwaggerTypeError)
    def test_invalid_default_min_num(self):
        DataType({'type': 'number', 'minimum': '5.5', 'defaultValue': 5.3}, {}, {})

    @raises(SwaggerTypeError)
    def test_invalid_default_max_num(self):
        DataType({'type': 'number', 'maximum': '5.5', 'defaultValue': 5.7}, {}, {})

    @raises(SwaggerFieldError)
    def test_array_no_items(self):
        DataType({'type': 'array'}, {}, {})

    def test_array(self):
        dt = DataType({'type': 'array', 'items': {'type': 'string'}}, {}, {})
        assert_equals(dt.type, 'array')
        assert_is_instance(dt.items, Items)

        dt = DataType({'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True}, {}, {})
        assert_is_instance(dt.uniqueItems, bool)
        assert_equals(dt.uniqueItems, True)
