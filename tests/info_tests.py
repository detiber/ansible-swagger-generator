import json

from swagger.info import Info, InfoInvalidError, InfoFieldError

from nose.tools import raises

MIN_VALID_INFO = {
    "title": "Title",
    "description": "Description"
}


INVALID_FIELD_INFO = {
    "title": "Title",
    "description": "Description",
    "invalidField": ""
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

    @raises(InfoInvalidError)
    def test_invalid_info_doc(self):
        Info(9)

    def test_min_valid_info(self):
        Info(MIN_VALID_INFO)

    def test_valid_info(self):
        Info(VALID_INFO)

    @raises(InfoFieldError)
    def test_invalid_field_info(self):
        Info(INVALID_FIELD_INFO)
