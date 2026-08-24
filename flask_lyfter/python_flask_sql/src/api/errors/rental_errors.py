class RentalCreationError(Exception):
    """
    Raised when database fails to create a rental.
    """



class FatalRentalCreationError(Exception):
    """
    Raised when database fails to create a
    rental with internal error from database.
    """



class RentalDoesNotExistsError(Exception):
    """
    Raised when rental does not exist in database
    """



class RentalUpdateError(Exception):
    """
    Raised when database fails to update a rental.
    """

