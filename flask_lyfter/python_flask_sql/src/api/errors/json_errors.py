class MalformedJSONError(Exception):
    """
    Raised when parsed json is malformed
    """

    pass


class EmptyJSONError(Exception):
    """
    Raised when parsed json is empty
    """

    pass


class MissingParametersJSONError(Exception):
    """
    Raise when body is missing an expected parameter
    """

    pass
