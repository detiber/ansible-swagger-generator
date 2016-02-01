class SwaggerError(Exception):
    pass


class SwaggerInvalidError(SwaggerError):
    pass


class SwaggerFieldError(SwaggerError):
    pass


class SwaggerTypeError(SwaggerError):
    pass


class SwaggerNotImplimented(SwaggerError):
    pass


class SwaggerValueError(SwaggerError):
    pass
