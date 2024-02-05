"""Represents an error if you add a new user and this user exist."""


class UserExistError(Exception):
    """Represents an error if you add a new user and this user exist."""
    def __init__(self, user: str):
        """Initialize the UserExistError exception.

        Args:
            user: Username of existing user.
        """
        self.message = f"The user {user} already exist in the system"
        super().__init__(self.message)
