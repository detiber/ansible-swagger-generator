import json
from six import itervalues
from datetime import date, datetime
from pyrfc3339 import generate
from distutils.util import strtobool
import pytz

from swagger.exceptions import SwaggerError, SwaggerInvalidError, \
                               SwaggerFieldError, SwaggerTypeError, \
                               SwaggerNotImplimented, SwaggerValueError
from swagger.data_type import SwaggerString, SwaggerInteger, SwaggerNumber, \
                              SwaggerPrimitive, SwaggerBool, Items, \
                              PRIMITIVES, DataType

from nose.tools import raises, assert_equals, assert_is_instance, \
                       assert_true, assert_in, assert_not_in


class TestDataType(object):

    @raises(SwaggerValueError)
    def test_no_ref_no_type(self):
        DataType({})

    def test_valid_primitives(self):
        for t in PRIMITIVES:
            type_props = PRIMITIVES[t]
            dt = DataType({'type': t})
            assert_equals(dt['type'], t)
            for f in type_props['type'].FORMATS:
                dtf = DataType({'type': t, 'format': f})
                assert_equals(dtf['type'], t)
                assert_equals(dtf['format'], f)

    @raises(SwaggerValueError)
    def test_invalid_primitive(self):
        dt = DataType({'type': 'string', 'format': 'blue'})

    def test_ref(self):
        dt = DataType({'$ref': 'MyModel'})
        assert_equals(dt['$ref'], 'MyModel')

    @raises(SwaggerValueError)
    def test_invalid_default_enum(self):
        DataType({'type': 'string', 'enum': ['blue', 'green'], 'defaultValue': 'orange'})

    @raises(SwaggerValueError)
    def test_invalid_type_enum(self):
        DataType({'type': 'integer', 'enum': [1, 2]})

    def test_enum(self):
        dt = DataType({'type': 'string', 'enum': ['blue', 'green']})
        assert_equals(dt['type'], 'string')
        assert_equals(dt['enum'], ['blue', 'green'])

    @raises(SwaggerValueError)
    def test_invalid_default(self):
        DataType({'type': 'integer', 'defaultValue': 'blue', 'format': 'int32'})

    def test_default_values(self):
        dv_tests = {'integer': 9, 'number': 3.5, 'string': 'blue', 'boolean': True}
        for t in dv_tests:
            dv = dv_tests[t]
            f = None
            if t == 'integer':
                f = 'int32'
            elif t == 'number':
                f = 'float'
            dt = DataType({'type': t, 'defaultValue': dv, 'format': f})
            assert_equals(dt['type'], t)
            assert_equals(PRIMITIVES[t]['schema_type'](dt['defaultValue']), dv)

    def test_min_max_with_default(self):
        dv_tests = {'integer': {'format': 'int32', 'max': '10', 'min': '5', 'default': 7},
                    'number': {'format': 'float', 'max': '30.5', 'min': '10.2', 'default': 20.5}}
        for t in dv_tests:
            values = dv_tests[t]
            dt = DataType({'type': t, 'format': values['format'],
                           'minimum': values['min'],
                           'maximum': values['max'],
                           'defaultValue': values['default']})

    @raises(SwaggerTypeError)
    def test_invalid_default_min_int(self):
        DataType({'type': 'integer', 'minimum': '5', 'defaultValue': 4})

    @raises(SwaggerTypeError)
    def test_invalid_default_max_int(self):
        DataType({'type': 'integer', 'maximum': '5', 'defaultValue': 6})

    @raises(SwaggerTypeError)
    def test_invalid_default_min_num(self):
        DataType({'type': 'number', 'minimum': '5.5', 'defaultValue': 5.3})

    @raises(SwaggerTypeError)
    def test_invalid_default_max_num(self):
        DataType({'type': 'number', 'maximum': '5.5', 'defaultValue': 5.7})

    @raises(SwaggerValueError)
    def test_array_no_items(self):
        DataType({'type': 'array'})

    def test_array(self):
        dt = DataType({'type': 'array', 'items': {'type': 'string'}})
        assert_equals(dt['type'], 'array')
        assert_is_instance(dt['items'], Items)

        dt = DataType({'type': 'array', 'items': {'type': 'string'}, 'uniqueItems': True})
        assert_is_instance(dt['uniqueItems'], bool)
        assert_equals(dt['uniqueItems'], True)


class TestItems(object):
    @raises(SwaggerValueError)
    def test_no_ref_no_type(self):
        Items({})

    def test_valid_primitives(self):
        for t in PRIMITIVES:
            items = Items({'type': t})
            assert_equals(items['type'], t)
            for f in PRIMITIVES[t]['type'].FORMATS:
                items = Items({'type': t, 'format': f})
                assert_equals(items['type'], t)
                assert_equals(items['format'], f)

    @raises(SwaggerValueError)
    def test_invalid_model_type(self):
        Items({'type': 'myModel', 'format': 'int32'})

    def test_ref(self):
        dt = Items({'$ref': 'MyModel'})
        assert_equals(dt['$ref'], 'MyModel')

    @raises(SwaggerValueError)
    def test_invalid_type(self):
        Items({'type': 'array'})


class TestSwaggerString(object):

    @staticmethod
    @raises(SwaggerTypeError)
    def test_invalid_format():
        SwaggerString(u'hi', 'blue')

    @staticmethod
    @raises(SwaggerValueError)
    def check_invalid_value(value, s_format):
        SwaggerString(value, s_format)

    def test_invalid_valuess(self):
        self.check_invalid_value(u'hi', 'date')
        self.check_invalid_value(u'hi', 'date-time')
        self.check_invalid_value(u'hi', 'byte')
        self.check_invalid_value(b'hi', None)

    def test_valid_values(self):
        curr_datetime = datetime.now(pytz.utc)
        curr_date = curr_datetime.date()
        value_tests = [
            ( curr_date.isoformat(), 'date' ),
            ( generate(curr_datetime), 'date-time' ),
            ( b'blue', 'byte'),
            ( u'hi', None),
        ]
        for val, f in value_tests:
            s = SwaggerString(val, f)
            assert_equals(s.format_str, f)
            assert_equals(s.data, val)


class TestSwaggerInteger(object):

    @staticmethod
    @raises(SwaggerTypeError)
    def test_invalid_format():
        SwaggerInteger(u'9', 'blue')

    @staticmethod
    @raises(SwaggerValueError)
    def check_invalid_value(value, i_format):
        SwaggerInteger(value, i_format)

    def test_invalid_values(self):
        self.check_invalid_value(str(2**32+1), 'int32')
        self.check_invalid_value(-(2**32+2), 'int32')
        self.check_invalid_value(2**64+1, 'int64')
        self.check_invalid_value(str(-(2**64+2)), 'int64')

    def test_valid_values(self):
        curr_datetime = datetime.now(pytz.utc)
        curr_date = curr_datetime.date()
        value_tests = [
            ( 2**32, 'int32' ),
            ( 2**64, 'int64' ),
            ( -(2**32+1), 'int32' ),
            ( -(2**64+1), 'int64' ),
        ]
        for val, f in value_tests:
            s = SwaggerInteger(val, f)
            assert_equals(s.format_str, f)
            assert_equals(s.data, val)

class TestSwaggerNumber(object):
    @staticmethod
    @raises(SwaggerTypeError)
    def check_invalid_format(f):
        SwaggerNumber(u'9', f)

    def test_invalid_formats(self):
        for f in ['blue', None]:
            self.check_invalid_format(f)

    @staticmethod
    @raises(SwaggerValueError)
    def check_invalid_value(value, n_format):
        SwaggerNumber(value, n_format)

    def test_invalid_values(self):
        self.check_invalid_value('blue', 'float')

    def test_valid_values(self):
        curr_datetime = datetime.now(pytz.utc)
        curr_date = curr_datetime.date()
        value_tests = [
            ( 3.5, 'float', 3.5 ),
            ( '2.3333', 'double', 2.3333 ),
            ( -10, 'double', -10 ),
            ( '-12.15', 'float', -12.15 ),
        ]
        for val, f, comp in value_tests:
            s = SwaggerNumber(val, f)
            assert_equals(s.format_str, f)
            assert_equals(s.data, comp)


class TestSwaggerBool(object):
    @staticmethod
    @raises(SwaggerTypeError)
    def test_invalid_format():
        SwaggerBool(u'true', 'blue')

    @staticmethod
    @raises(SwaggerValueError)
    def check_invalid_value(value):
        SwaggerBool(value)

    def test_invalid_values(self):
        self.check_invalid_value('green')
        self.check_invalid_value(9)

    def test_valid_values(self):
        curr_datetime = datetime.now(pytz.utc)
        curr_date = curr_datetime.date()
        value_tests = [
            True,
            False,
            'true',
            'false',
        ]
        for val in value_tests:
            b = SwaggerBool(val)
            assert_equals(b.data, strtobool(str(val)))
