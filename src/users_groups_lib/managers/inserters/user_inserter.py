"""Insert user in the shell."""
from typing import Optional

from shell_executor_lib import CommandManager, CommandError

from users_groups_lib import UserPermissionError, GroupNotExistError, UserExistError


class UserInserter:
    """Insert user in the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserInserter.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def add_user(self, name: str, home: str, shell: str, main_group: Optional[str] = None) -> None:
        """Add a user to the system.

        Args:
            name: The username of the new user.
            home: The home directory.
            shell: The sell witch user use.
            main_group: The main group of the new user, is optional.

        Raises:
            UserExistError: If the user already exist.
            UserPermissionError: If you don't have sudo privileges to add user.
            GroupNotExistError: If you try to add the new user in nonexistent group.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/useradd {name} -m -d {home} -s {shell}"
                                                        f"{main_group if f' -g {main_group}' else ''}", True)
        except CommandError as command_error:
            match command_error.status_code:
                case 1:
                    raise UserPermissionError(name)
                case 6:
                    raise GroupNotExistError(name)
                case 9:
                    raise UserExistError(name)
            raise command_error
