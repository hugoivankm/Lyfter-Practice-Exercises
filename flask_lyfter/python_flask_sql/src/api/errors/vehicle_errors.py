class VehicleDeletionError(Exception):
    """Raised when database fails to delete a vehicle."""


class VehicleCreationError(Exception):
    """
    Raised when database fails to create a vehicle.
    """


class VehicleUpdateError(Exception):
    """
    Raised when database fails to update a vehicle.
    """


class VehicleDoesNotExistsError(Exception):
    """
    Raised when vehicle does not exist in database
    """


class VehicleEmailAlreadyExistsError(Exception):
    """
    Raised when vehicle email already exists in database
    """
