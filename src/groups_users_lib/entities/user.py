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
    uid: int | None = None
    name: str | None = None
    shell: str | None = None
    home: str | None = None
    main_group: str | None = None
