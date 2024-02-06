"""Represents an error when attempting to delete a user in use."""


class UserInUseError(Exception):
    """Represents an error when attempting to delete a user in use."""

    def __init__(self, name: str):
        """Initialize the UserInUseError exception.

        Args:
            name: The name of the user in use.
        """
        self.message = f"You can't delete the user {name} because is in use."
        super().__init__(self.message)
