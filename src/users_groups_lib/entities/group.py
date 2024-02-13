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
    gid: int
    name: str
    users: list[str]
