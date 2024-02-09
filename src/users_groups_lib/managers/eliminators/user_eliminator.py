"""Delete users from the shell."""
from shell_executor_lib import CommandError, CommandManager

from users_groups_lib import UserPermissionError, UserNotExistError, UserInUseError


class UserEliminator:
    """Delete users from the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserManager.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def delete_user(self, name: str) -> None:
        """Delete user of the system.

        Args:
            name: The username of the user to delete.

        Raises:
            UserInUseError: If you try to delete a user in use.
            UserPermissionError: If you don't have sudo privileges to edit user.
            UserNotExistError: If you try to delete nonexistent user.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/userdel {name}", True)
        except CommandError as command_error:
            match command_error.status_code:
                case 1:
                    raise UserPermissionError(name)
                case 6:
                    raise UserNotExistError(name)
                case 8:
                    raise UserInUseError(name)
            raise command_error
