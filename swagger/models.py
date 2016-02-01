from .base import SwaggerDict
from .data_type import DataType
from .properties import Properties
from .exceptions import SwaggerFieldError


class Model(DataType):
    def __init__(self, model):

        required_fields = {
            'id': {'type': basestring},
            'properties': {'type': Properties},
        }
        optional_fields = {
            'description': {'type': basestring},
            'required': {'type': list, 'subtype': basestring},
            'subTypes': {'type': list, 'subtype': basestring},
        }
        if 'subTypes' in model:
            required_fields['descriminator'] = {'type': basestring}

        DataType.__init__(self, model, required_fields, optional_fields)

        if hasattr(self, 'subTypes') and not hasattr(self, 'descriminator'):
            raise SwaggerFieldError("Expected value of descriminator to be in subTypes")
        # TODO: validations
        #       - all values in required are names of properties in property
        #       - value of descriminator is the name of a property in properties


class Models(SwaggerDict):
    def __init__(self, models):
        SwaggerDict.__init__(self, models, Model)
        # TODO: validations
        #       - each model defined has a unique id
        #       - for each model the model ids in subTypes are also in models
        #       - test for cyclic dependencies in subTypes of each model
