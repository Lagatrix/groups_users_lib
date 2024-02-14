"""Represents an error if the user who manage a group don't have sudo permissions."""


class GroupPermissionError(Exception):
    """Represents an error if the user who manage a group don't have sudo permissions."""

    def __init__(self, group: str):
        """Initialize the GroupPermissionError exception.

        Args:
            group: Name of group which manage.
        """
        self.message = f"You can't manage the group {group} because you don't have sudo permissions"
        super().__init__(self.message)
