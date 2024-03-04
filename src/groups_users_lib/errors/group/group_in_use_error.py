"""Represents an error when attempting to delete a group in use."""


class GroupInUseError(Exception):
    """Represents an error when attempting to delete a group in use."""

    def __init__(self, group_name: str) -> None:
        """Initialize the GroupInUseError exception.

        Args:
            group_name: The name of the group in use.
        """
        self.message: str = f"Group {group_name} is in use and cannot be deleted."
        super().__init__(self.message)
