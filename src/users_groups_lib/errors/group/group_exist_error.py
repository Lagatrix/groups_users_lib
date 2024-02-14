"""Represents an error if you add a new group and this group exist."""


class GroupExistError(Exception):
    """Represents an error if you add a new group and this group exist."""
    def __init__(self, group: str):
        """Initialize the UserExistError exception.

        Args:
            group: Name of existing group.
        """
        self.message = f"The group {group} already exist in the system"
        super().__init__(self.message)
