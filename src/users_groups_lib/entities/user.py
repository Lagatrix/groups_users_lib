"""This entity represents a unix user."""
from dataclasses import dataclass


@dataclass
class User:
    """This entity represents a unix user.

    Attributes:
        uid: The identification of user.
        name: The name of the user.
        shell: The shell which user use.
        home: The home directory of the user.
        main_group: The main group of the user.
    """
    uid: int
    name: str
    shell: str
    home: str
    main_group: str
