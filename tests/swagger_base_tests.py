import json
from six import itervalues

from swagger.exceptions import SwaggerError, SwaggerInvalidError, \
                               SwaggerFieldError, SwaggerTypeError, \
                               SwaggerNotImplimented
from swagger.base import SwaggerBase, SwaggerDict, SwaggerList, \
                         SwaggerField, SwaggerValueError, SwaggerObject

from nose.tools import raises, assert_equals, assert_is_instance, \
                       assert_true, assert_in, assert_not_in


class TestSwaggerList(object):
    @staticmethod
    @raises(SwaggerValueError)
    def test_invalid_subtype():
        SwaggerList(['blue'], int)

    @staticmethod
    def test_empty_list():
        for empty_val in ([], None):
            sl = SwaggerList(empty_val, int)
            assert_equals(len(sl), 0)

    @staticmethod
    def test_valid_list():
        test_list=[1, 2, 3]
        sl = SwaggerList(test_list, int)
        assert_equals(len(sl), len(test_list))
        for item in sl:
            assert_is_instance(item, int)


class TestSwaggerDict(object):
    @staticmethod
    @raises(SwaggerValueError)
    def test_invalid_subtype():
        SwaggerDict({'green': 'blue'}, int)

    @staticmethod
    def test_empty_dict():
        for empty_val in ({}, None):
            sd = SwaggerDict(empty_val, int)
            assert_equals(len(sd), 0)

    @staticmethod
    def test_valid_dict():
        test_dict={'a': 1, 'b': 2, 'c': 3}
        sd = SwaggerDict(test_dict, int)
        assert_equals(len(sd), len(test_dict))
        for val in itervalues(sd):
            assert_is_instance(val, int)


class TestSwaggerField(object):
    @staticmethod
    @raises(SwaggerTypeError)
    def check_missing_subtype(iter_type):
        SwaggerField(iter_type)

    def test_missing_subtypes(self):
        for i in (SwaggerList, SwaggerDict):
            yield self.check_missing_subtype, i

    @staticmethod
    @raises(SwaggerValueError)
    def test_invalid_cast_value():
        field = SwaggerField(int)
        field.cast_value('blue')

    def test_valid_subtypes(self):
        for iter_type in (SwaggerList, SwaggerDict):
            sf = SwaggerField(iter_type, subtype=int)
            assert_true(issubclass(sf.type, iter_type))
            assert_true(issubclass(sf.subtype, int))

    @staticmethod
    def test_valid_cast_value():
        field = SwaggerField(int)
        value = field.cast_value('9')
        assert_equals(value, 9)

class TestSwaggerObject(object):

    @staticmethod
    @raises(SwaggerFieldError)
    def check_for_field_error(data, fields):
        SwaggerObject(data, fields)

    def test_field_errors(self):
        self.check_for_field_error({}, {'a': SwaggerField(int, required=True)})
        self.check_for_field_error({'a': 9}, {})

    @staticmethod
    @raises(SwaggerFieldError)
    def test_invalid_set():
        so = SwaggerObject({},{})
        so['a'] = 9

    @staticmethod
    @raises(SwaggerFieldError)
    def test_invalid_del():
        so = SwaggerObject({'a': 1},{'a': SwaggerField(int, required=True)})
        del so['a']

    @staticmethod
    def test_valid_requires():
        data = {'a': 1, 'b': '2'}
        fields = {'a': SwaggerField(int, required=True),
                  'b': SwaggerField(int, required=True)}
        so = SwaggerObject(data, fields)
        for key in data:
            assert_in(key, so)
            assert_is_instance(so[key], fields[key].type)

    @staticmethod
    def test_missing_optional():
        data = {'a': 1}
        fields = {'a': SwaggerField(int, required=True),
                  'b': SwaggerField(int)}
        so = SwaggerObject(data, fields)
        for key in data:
            assert_in(key, so)
            assert_is_instance(so[key], fields[key].type)

    @staticmethod
    def test_json_data():
        so = SwaggerObject('{"a": 1}', {'a': SwaggerField(int)})
        assert_in('a', so)
        assert_is_instance(so['a'], int)

    @staticmethod
    def test_set():
        so = SwaggerObject({}, {'a': SwaggerField(int)})
        so['a'] = '9'
        assert_in('a', so)
        assert_is_instance(so['a'], int)
        assert_equals(so['a'], 9)

    @staticmethod
    def test_del():
        so = SwaggerObject({'a': 9}, {'a': SwaggerField(int)})
        del so['a']
        assert_not_in('a', so)
