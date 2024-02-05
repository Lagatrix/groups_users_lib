"""Represents an error when attempting to manage a nonexistent group."""


class GroupNotExistError(Exception):
    """Represents an error when attempting to manage a nonexistent group."""

    def __init__(self, group: str):
        """Initialize the GroupNotExistError exception.

        Args:
            group: Username of the user who manage.
        """
        self.message = f"You can't manage the group {group} because it doesn't exist."
        super().__init__(self.message)
