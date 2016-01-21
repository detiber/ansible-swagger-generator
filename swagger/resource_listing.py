import json
from swagger.info import Info
from swagger.authorizations import Authorizations
from swagger.resource_list import ResourceList

class ResourceListingInvalidError(Exception):
    pass

class ResourceListingFieldError(Exception):
    pass

class ResourceListing(object):

    _required_fields = {
        'swaggerVersion': {'type': basestring},
        'apis': {'type': ResourceList}
    }
    _optional_fields = {
        'apiVersion': {'type': basestring},
        'info': {'type': Info},
        'authorizations': {'type': Authorizations}
    }

    def __init__(self, resource_listing_doc):
        if isinstance(resource_listing_doc, basestring):
            self._raw = json.loads(resource_listing_doc)
        elif isinstance(resource_listing_doc, dict):
            self._raw = resource_listing_doc
        else:
            raise ResourceListingInvalidError("Could not parse ResourceListing Object")

        self._known_fields = self._required_fields.copy()
        self._known_fields.update(self._optional_fields)

        self._set_fields()
        self._validate_resource_listing()

    def _set_fields(self):
        required_keys = self._required_fields.keys()
        if set(self._required_fields.keys()).issubset(self._raw.keys()):
            unknown_keys = set(self._raw.keys()).difference(self._known_fields.keys())
            if unknown_keys:
                raise ResourceListingFieldError("Unexpected fields {0} found".format(", ".join(unknown_keys)))

            for k, v in self._raw.iteritems():
                if self._known_fields[k]['type'] == Info:
                    setattr(self, k, Info(v))
                elif self._known_fields[k]['type'] == Authorizations:
                    setattr(self, k, Authorizations(v))
                elif self._known_fields[k]['type'] == ResourceList:
                    setattr(self, k, ResourceList(v))
                else:
                    setattr(self, k, v)
        else:
            missing_keys = set(self._required_fields.keys()).difference(self.raw.keys())
            raise ResourceListingInvalidError("Required fields {0} not found".format(", ".join(missing_keys)))


    def _validate_resource_listing(self):
        for k, v in self._known_fields.iteritems():
            field_value = getattr(self, k, None)
            if field_value is not None:
                expected_type = v['type']
                if not isinstance(field_value, expected_type):
                    raise TypeError("Expected type of field {0} to be {1}".format(k, expected_type.__name__))

