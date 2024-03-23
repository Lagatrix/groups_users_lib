"""This entity represents a unix group."""
from dataclasses import dataclass


@dataclass
class Group:
    """This entity represents a unix group.

    Attributes:
        gid: The identification of group.
        name: The name of the group.
        users: List of users names in group.
    """
    gid: int | None = None
    name: str | None = None
    users: list[str] | None = None
