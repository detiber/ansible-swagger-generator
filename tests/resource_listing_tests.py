import json

from swagger.resource_listing import ResourceListing, ResourceListingInvalidError, ResourceListingFieldError

from nose.tools import raises

MIN_VALID_JSON_RESOURCE_LISTING = """
{
  "swaggerVersion": "1.2",
  "apis": []
}
"""

INVALID_FIELD_JSON_RESOURCE_LISTING = """
{
  "swaggerVersion": "1.2",
  "apis": [],
  "invalidField": ""
}
"""

VALID_JSON_RESOURCE_LISTING = """
{
  "swaggerVersion": "1.2",
  "apis": [],
  "apiVersion": "v1",
  "info": {
    "title": "Test",
    "description": "Test"
  },
  "authorizations": {
    "basic": {
      "type": "basicAuth"
    }
  }
}
"""

class TestResourceListing(object):

    @raises(ResourceListingInvalidError)
    def test_invalid_resource_listing_doc(self):
        ResourceListing(9)

    def test_min_valid_json_resource_listing(self):
        ResourceListing(MIN_VALID_JSON_RESOURCE_LISTING)

    def test_min_valid_dict_resource_listing(self):
        ResourceListing(json.loads(MIN_VALID_JSON_RESOURCE_LISTING))

    def test_valid_json_resource_listing(self):
        ResourceListing(VALID_JSON_RESOURCE_LISTING)

    def test_min_valid_dict_resource_listing(self):
        ResourceListing(json.loads(VALID_JSON_RESOURCE_LISTING))

    @raises(ResourceListingFieldError)
    def test_invalid_field_resource_listing(self):
        ResourceListing(INVALID_FIELD_JSON_RESOURCE_LISTING)
