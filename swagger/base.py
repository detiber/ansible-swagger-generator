import json

from.exceptions import SwaggerInvalidError, SwaggerFieldError, SwaggerTypeError


class SwaggerBase(object):

    def __init__(self, required_fields, optional_fields, swagger_doc):
        self.required_fields = required_fields if required_fields is not None else {}
        self.optional_fields = optional_fields if optional_fields is not None else {}
        self.parse(swagger_doc)

    def parse(self, swagger_doc):
        if isinstance(swagger_doc, basestring):
            self.raw = json.loads(swagger_doc)
        elif isinstance(swagger_doc, dict):
            self.raw = swagger_doc
        else:
            raise SwaggerInvalidError("Could not parse Swagger Object")

        self.known_fields = self.required_fields.copy()
        self.known_fields.update(self.optional_fields)
        self.set_fields()

    def set_fields(self):
        if set(self.required_fields.keys()).issubset(self.raw.keys()):
            unknown_keys = set(self.raw.keys()).difference(self.known_fields.keys())
            if unknown_keys:
                raise SwaggerFieldError("Unexpected fields {0} found".format(", ".join(unknown_keys)))

            for key, val in self.raw.iteritems():
                expected_type = self.known_fields[key]['type']
                if issubclass(expected_type, SwaggerBase):
                    sub = expected_type(val)
                    setattr(self, key, sub)
                elif isinstance(val, expected_type):
                    if isinstance(val, list):
                        expected_subtype = self.known_fields[key]['subtype']
                        if issubclass(expected_subtype, SwaggerBase):
                            setattr(self, key, [expected_subtype(item) for item in val])
                        else:
                            for item in val:
                                if not isinstance(item, expected_subtype):
                                    raise SwaggerTypeError(
                                        "Expected field {0} to be: [{1}]".format(key, expected_subtype)
                                    )
                            setattr(self, key, val)
                    else:
                        if 'values' in self.known_fields[key]:
                            valid_values = self.known_fields[key]['values']
                            if val not in valid_values:
                                raise SwaggerTypeError(
                                    "{0} not a valid value for field: {1} expected on of: {2}".format(
                                        val, key, ",".join(valid_values)
                                    )
                                )
                        setattr(self, key, val)

                else:
                    raise SwaggerTypeError("Expected field {0} to be: {1}".format(key, expected_type))
        else:
            missing_keys = set(self.required_fields.keys()).difference(self.raw.keys())
            raise SwaggerFieldError("Required fields {0} not found".format(", ".join(missing_keys)))
