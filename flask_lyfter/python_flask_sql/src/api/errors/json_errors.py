class MalformedJSONError(Exception):
    """
    Raised when parsed json is malformed
    """



class EmptyJSONError(Exception):
    """
    Raised when parsed json is empty
    """



class MissingParametersJSONError(Exception):
    """
    Raise when body is missing an expected parameter
    """

