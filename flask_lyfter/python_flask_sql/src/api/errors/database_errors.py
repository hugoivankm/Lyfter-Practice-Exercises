class DbRetrievalError(Exception):
    """
    Raised when unable to retrieve data from the database
    """

    pass


class InvalidStatusError(Exception):
    """
    Raised when an invalid status is received for an entity
    """

    pass


class InvalidFilterError(Exception):
    """
    Raised when an invalid filter is received for an entity
    """

    pass
