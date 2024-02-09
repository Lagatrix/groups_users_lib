"""Modify user in the shell."""
from typing import Optional
from shell_executor_lib import CommandManager, CommandError
from users_groups_lib import UserPermissionError, GroupNotExistError, UserNotExistError, UserExistError


class UserModifier:
    """Modify user in the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserModifier.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def edit_user(self, name: str, new_name: Optional[str] = None, home: Optional[str] = None,
                        shell: Optional[str] = None, password: Optional[str] = None,
                        main_group: Optional[str] = None) -> None:
        """Edit user of the system.

        Args:
            name: The username of the user to modify.
            new_name: New username.
            home: New home directory.
            shell: New sell witch user use.
            password: New password of the user.
            main_group: New main group of the new user.

        Raises:
            UserExistError: If you put a username of existent user.
            UserPermissionError: If you don't have sudo privileges to edit user.
            GroupNotExistError: If you try to add the user in nonexistent group.
            UserNotExistError: If you try to edit nonexistent user.
            CommandError: If the exit code is not unexpected.
        """
        params: dict[str, str | None] = {"l": new_name, "d": home, "s": shell, "g": main_group}
        command: str = f"/sbin/usermod {name}"

        for param, value in params.items():
            if value is not None:
                command += f" -{param} {value}"

        try:
            await self._command_manager.execute_command(command, True)

            if password is not None:
                await self.change_password(name, password)
        except CommandError as command_error:
            match command_error.status_code:
                case 1:
                    raise UserPermissionError(name)
                case 6:
                    if command_error.response.find("gr") != -1:
                        raise GroupNotExistError(name)
                    raise UserNotExistError(name)
                case 9:
                    raise UserExistError(new_name if new_name is not None else name)
            raise command_error

    async def change_password(self, name: str, password: str) -> None:
        """Change the password of user.

        Args:
            name: The username of the user to change password.
            password: The new password.

        Raises:
            UserPermissionError: If you don't have sudo privileges to manage user.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/bin/passwd {name}", True, password, password)
        except CommandError as command_error:
            if command_error.status_code == 1:
                raise UserPermissionError(name)
            raise command_error
