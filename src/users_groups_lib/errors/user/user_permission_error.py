"""Represents an error if you add a new user and this user exist."""


class UserPermissionError(Exception):
    """Represents an error if the user who add new user don't have sudo permissions."""

    def __init__(self, user: str):
        """Initialize the UserPermissionError exception.

        Args:
            user: Username of the user who manage.
        """
        self.message = f"You can't manage the user {user} because you don't have sudo permissions"
        super().__init__(self.message)
