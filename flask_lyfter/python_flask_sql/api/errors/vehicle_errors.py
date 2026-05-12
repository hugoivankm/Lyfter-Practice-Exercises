class VehicleDeletionError(Exception):
    """Raised when database fails to delete a vehicle."""

    pass


class VehicleCreationError(Exception):
    """
    Raised when database fails to create a vehicle.
    """

    pass


class VehicleUpdateError(Exception):
    """
    Raised when database fails to update a vehicle.
    """

    pass


class VehicleDoesNotExistsError(Exception):
    """
    Raised when vehicle does not exist in database
    """

    pass


class VehicleEmailAlreadyExistsError(Exception):
    """
    Raised when vehicle email already exists in database
    """

    pass