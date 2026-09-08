class UserCreationError(Exception):
    """
    Raised when database fails to create a user.
    """


class UserUpdateError(Exception):
    """
    Raised when database fails to update a user.
    """


class UserDeletionError(Exception):
    """
    Raised when database fails to create a user.
    """


class UserDoesNotExistsError(Exception):
    """
    Raised when user does not exist in database
    """


class AlreadyExistsError(Exception):
    """
    Raised when user email or username already exists in database
    """
