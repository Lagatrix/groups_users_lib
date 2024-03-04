"""Insert group in the shell."""
from typing import Optional

from shell_executor_lib import CommandManager, CommandError

from groups_users_lib import GroupExistError, UserNotExistError


class GroupInserter:
    """Insert group in the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupInserter.

        Args:
            command_manager: To make commands in the shell.
        """
        self._command_manager = command_manager

    async def add_group(self, name: str, usernames: Optional[list[str]] = None) -> None:
        """Add a group to the system.

        Args:
            name: The name of the new group.
            usernames: The names of the news users in the group.

        Raises:
            GroupExistError: If the group already exist.
            UserNotExistError: If you try to add a nonexistent user in the group.
            CommandError: If the exit code is not unexpected.
        """
        command: str = f"/sbin/groupadd {name}"

        if usernames is not None:
            command += f" -U {','.join(usernames)}"

        try:
            await self._command_manager.execute_command(command, True)
        except CommandError as command_error:
            if command_error.status_code == 9:
                raise GroupExistError(name)
            elif command_error.status_code == 10:
                raise UserNotExistError(command_error.response.split(" ")[3])

            raise command_error
