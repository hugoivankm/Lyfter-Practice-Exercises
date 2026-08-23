class RentalCreationError(Exception):
    """
    Raised when database fails to create a rental.
    """

    pass


class FatalRentalCreationError(Exception):
    """
    Raised when database fails to create a
    rental with internal error from database.
    """

    pass


class RentalDoesNotExistsError(Exception):
    """
    Raised when rental does not exist in database
    """

    pass


class RentalUpdateError(Exception):
    """
    Raised when database fails to update a rental.
    """

    pass
