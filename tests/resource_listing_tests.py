from swagger.resource_listing import ResourceListing

MIN_VALID_RESOURCE_LISTING = {
    "swaggerVersion": "1.2",
    "apis": [{"path": "/boo"}]
}

VALID_RESOURCE_LISTING = {
    "swaggerVersion": "1.2",
    "apis": [{"path": "/boo"}],
    "apiVersion": "v1",
    "info": {"title": "Title",
             "description": "Description"},
    "authorizations": {"basic": {"type": "basicAuth"}}
}

class TestResource(object):
    def test_min_valid_resource(self):
        ResourceListing(MIN_VALID_RESOURCE_LISTING)

    def test_valid_resource(self):
        ResourceListing(VALID_RESOURCE_LISTING)
