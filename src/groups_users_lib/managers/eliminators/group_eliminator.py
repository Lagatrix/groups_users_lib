"""Delete groups from the shell."""
from shell_executor_lib import CommandManager, CommandError

from groups_users_lib import GroupNotExistError
from groups_users_lib.errors import GroupInUseError


class GroupEliminator:
    """Delete groups from the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupEliminator.

        Args:
            command_manager: To make commands in the shell.
        """
        self._command_manager = command_manager

    async def delete_group(self, name: str) -> None:
        """Delete group of the system.

        Args:
            name: The name of the group to delete.

        Raises:
            GroupNotExistError: If you try to delete nonexistent group.
            GroupInUseError: If the group is in use by a user.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/groupdel {name}", True)
        except CommandError as command_error:
            if command_error.status_code == 6:
                raise GroupNotExistError(name)
            elif command_error.status_code == 8:
                raise GroupInUseError(name)
            raise command_error
