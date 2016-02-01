from swagger.resource import Resource

MIN_VALID_RESOURCE = {
    "path": "/boo",
}

VALID_RESOURCE = {
    "path": "/boo",
    "description": "Description",
}

class TestResource(object):
    def test_min_valid_resource(self):
        Resource(MIN_VALID_RESOURCE)

    def test_valid_resource(self):
        Resource(VALID_RESOURCE)
