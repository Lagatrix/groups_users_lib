"""Represents an error when attempting to manage a nonexistent user."""


class UserNotExistError(Exception):
    """Represents an error when attempting to manage a nonexistent user."""

    def __init__(self, group: str):
        """Initialize the UserNotExistError exception.

        Args:
            group: Username of the user who manage.
        """
        self.message = f"You can't manage the user {group} because it doesn't exist."
        super().__init__(self.message)
