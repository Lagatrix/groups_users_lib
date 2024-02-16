"""Represents an error where a user is not in a group."""


class NoUserInGroupError(Exception):
    """Represents an error where a user is not in a group."""
    def __init__(self, group: str, user: str) -> None:
        """Initialize the NoUserInGroupError.

        Args:
            group: The group that the user is not in.
            user: The user that is not in the group.
        """
        self.group = group
        self.message = f"The user {user} is not in the group {group}."
        super().__init__(self.message)
