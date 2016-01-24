import json

from swagger.exceptions import SwaggerError, SwaggerInvalidError, \
                               SwaggerFieldError, SwaggerTypeError, \
                               SwaggerNotImplimented
from swagger.base import SwaggerBase

from nose.tools import raises

BASIC_FIELD_DEF = {'a': {'type': basestring},
                   'b': {'type': list, 'subtype': basestring}}

FIELD_DEF_WITH_VALUES = {'a': {'type': basestring, 'values': ['a', 'b', 'c']}}

class TestSwaggerBase(object):

    @raises(SwaggerTypeError)
    def test_invalid_value(self):
        sb = SwaggerBase(FIELD_DEF_WITH_VALUES, [], {'a': 'invalid'})

    @raises(SwaggerInvalidError)
    def test_invalid_swagger_doc(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, [], 0)

    @raises(SwaggerFieldError)
    def test_missing_required_key(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, None, {'a': 'hi'})

    @raises(SwaggerFieldError)
    def test_invalid_field(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, None, {'a': 'hi', 'b':[], 'c': "blue"})

    @raises(SwaggerTypeError)
    def test_wrong_type(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, None, {'a': 'hi', 'b':' orange'})

    @raises(SwaggerTypeError)
    def test_wrong_type_list(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, None, {'a': 'hi', 'b':[9]})

    def test_json_parse(self):
        sb = SwaggerBase(BASIC_FIELD_DEF, None, '{"a": "hi", "b": []}')
        assert sb.a == "hi"
        assert sb.b == []

    def test_valid_values(self):
        sb = SwaggerBase(FIELD_DEF_WITH_VALUES, [], {'a': 'a'})
        assert sb.a == 'a'
        sb = SwaggerBase(FIELD_DEF_WITH_VALUES, [], {'a': 'b'})
        assert sb.a == 'b'
        sb = SwaggerBase(FIELD_DEF_WITH_VALUES, [], {'a': 'c'})
        assert sb.a == 'c'

    def test_nested_def(self):
        class SwaggerCls1(SwaggerBase):
            def __init__(self, swagger_doc):
                SwaggerBase.__init__(self, BASIC_FIELD_DEF, {}, swagger_doc)

        class SwaggerCls2(SwaggerBase):
            def __init__(self, swagger_doc):
                SwaggerBase.__init__(self, BASIC_FIELD_DEF, {}, swagger_doc)

        field_def = {'c': {'type': SwaggerCls1},
                     'd': {'type': list, 'subtype': SwaggerCls2},
                     'e': {'type': basestring}}

        nested_doc = {'c': {'a': 'hi', 'b': []},
                      'd': [{'a': 'bye', 'b': ['green']},
                            {'a': 'fly', 'b': []}],
                      'e': 'orange'}
        sb = SwaggerBase(field_def, {}, nested_doc)

        print sb
        assert isinstance(sb.c, SwaggerCls1)
        assert sb.c.a == 'hi'
        assert sb.c.b == []
        assert isinstance(sb.d, list)
        for inst in sb.d:
            assert isinstance(inst, SwaggerCls2)
        assert sb.d[0].a == 'bye'
        assert sb.d[0].b == ['green']
        assert sb.d[1].a == 'fly'
        assert sb.d[1].b == []
        assert sb.e == 'orange'

