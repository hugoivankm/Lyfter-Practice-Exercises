class UserCreationError(Exception):
    """
    Raised when database fails to create a user.
    """

    pass


class UserUpdateError(Exception):
    """
    Raised when database fails to update a user.
    """

    pass


class UserDeletionError(Exception):
    """
    Raised when database fails to create a user.
    """

    pass



class UserDoesNotExistsError(Exception):
    """
    Raised when user does not exist in database
    """

    pass


class AlreadyExistsError(Exception):
    """
    Raised when user email or username already exists in database
    """

    pass
