
class InfoInvalidError(Exception):
    pass

class InfoFieldError(Exception):
    pass

class Info(object):

    _required_fields = {
        'title': {'type': basestring},
        'description': {'type': basestring}
    }
    _optional_fields = {
        'termsOfServiceUrl': {'type': basestring},
        'contact': {'type': basestring},
        'license': {'type': basestring},
        'licenseUrl': {'type': basestring}
    }

    def __init__(self, info):
        if isinstance(info, dict):
            self._raw = info
        else:
            raise InfoInvalidError("Could not parse Info Object")

        self._known_fields = self._required_fields.copy()
        self._known_fields.update(self._optional_fields)

        self._set_fields()
        self._validate_info()

    def _set_fields(self):
        required_keys = self._required_fields.keys()
        if set(self._required_fields.keys()).issubset(self._raw.keys()):
            unknown_keys = set(self._raw.keys()).difference(self._known_fields.keys())
            if unknown_keys:
                raise InfoFieldError("Unexpected fields {0} found".format(", ".join(unknown_keys)))

            for k, v in self._raw.iteritems():
                setattr(self, k, v)
        else:
            missing_keys = set(self._required_fields.keys()).difference(self.raw.keys())
            raise InfoInvalidError("Required fields {0} not found".format(", ".join(missing_keys)))


    def _validate_info(self):
        for k, v in self._known_fields.iteritems():
            field_value = getattr(self, k, None)
            if field_value is not None:
                expected_type = v['type']
                if not isinstance(field_value, expected_type):
                    raise TypeError("Expected type of field {0} to be {1}".format(k, expected_type.__name__))
