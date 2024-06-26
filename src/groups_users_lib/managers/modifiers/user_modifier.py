"""Modify user in the shell."""
from shell_executor_lib import CommandManager, CommandError
from groups_users_lib import GroupNotExistError, UserExistError


class UserModifier:
    """Modify user in the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserModifier.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def modify_username(self, name: str, new_name: str) -> None:
        """Modify the username of user.

        Args:
            name: Name of user.
            new_name: New username of user.

        Raises:
            PrivilegesError: If the user doesn't have sudo privileges.
            UserExistError: If the new username already exist.
            CommandError: If the command fails.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/usermod {name} -l {new_name}", True)
        except CommandError as command_error:
            if command_error.status_code == 9:
                raise UserExistError(name)
            raise command_error

    async def modify_home(self, name: str, home: str) -> None:
        """Modify shell with user use in the shell.

        Args:
            name: Name of user.
            home: New home directory.

        Raises:
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the command fails.
        """
        await self._command_manager.execute_command(f"/sbin/usermod {name} -d {home}", True)

    async def modify_shell(self, name: str, shell: str) -> None:
        """Modify shell with user use in the shell.

        Args:
            name: Name of user.
            shell: New shell witch user use.

        Raises:
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the command fails.
        """
        await self._command_manager.execute_command(f"/sbin/usermod {name} -s {shell}", True)

    async def modify_main_group(self, name: str, main_group: str) -> None:
        """Modify main group of user in the shell.

        Args:
            name: Name of user.
            main_group: New main group.

        Raises:
            GroupNotExistError: If you try to add the user in nonexistent group.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/usermod -g {main_group} {name}", True)
        except CommandError as command_error:
            if command_error.status_code == 6:
                raise GroupNotExistError(main_group)
            raise command_error

    async def modify_password(self, name: str, password: str) -> None:
        """Change the password of user.

        Args:
            name: The username of the user to change password.
            password: The new password.

        Raises:
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the exit code is not unexpected.
        """
        await self._command_manager.execute_command(f"/bin/passwd {name}", True, password, password)
