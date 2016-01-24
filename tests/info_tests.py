from swagger.info import Info

MIN_VALID_INFO = {
    "title": "Title",
    "description": "Description"
}


VALID_INFO = {
    "title": "Title",
    "description": "Description",
    "termsOfServiceUrl": "TosURL",
    "contact": "Contact",
    "license": "License",
    "licenseUrl": "LicenseURL"
}

class TestInfo(object):
    def test_min_valid_info(self):
        Info(MIN_VALID_INFO)

    def test_valid_info(self):
        Info(VALID_INFO)
