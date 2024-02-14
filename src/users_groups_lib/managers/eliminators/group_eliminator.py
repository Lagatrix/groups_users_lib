"""Delete groups from the shell."""
from shell_executor_lib import CommandManager, CommandError

from users_groups_lib import GroupNotExistError
from users_groups_lib.errors import GroupPermissionError, GroupInUseError


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
            GroupPermissionError: If you don't have sudo privileges to delete group.
            GroupNotExistError: If you try to delete nonexistent group.
            GroupInUseError: If the group is in use by a user.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/groupdel {name}", True)
        except CommandError as command_error:
            match command_error.status_code:
                case 1:
                    raise GroupPermissionError(name)
                case 6:
                    raise GroupNotExistError(name)
                case 8:
                    raise GroupInUseError(name)
            raise command_error
