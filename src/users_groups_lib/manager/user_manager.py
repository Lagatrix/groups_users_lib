"""Manage unix users in shell."""
from typing import Optional

from shell_executor_lib import CommandManager, CommandError

from users_groups_lib.entities import User
from users_groups_lib.errors import UserPermissionError, GroupNotExistError, UserExistError, UserNotExistError


class UserManager:
    """Manage unix users in shell."""

    def __init__(self, user: str, password: str) -> None:
        """Initialize the UserManager.

        Args:
            user: The user of the shell who execute command.
            password: The password of the user.
        """
        self.command_manager = CommandManager(user, password)

    async def get_users(self) -> list[User]:
        """Obtain the users from the shell in a list.

        Returns:
            A list of the users in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        user_list: list[User] = []

        data_list: list[str] = await self.command_manager.execute_command(
            "/bin/cat /etc/passwd | /bin/awk -F : '{print $3,$1,$7,$6,$4 }'", False)

        for data_row in data_list:
            data: list[str] = data_row.split(" ")

            user_list.append(User(int(data[0]), data[1], data[2], data[3], (await self.command_manager.execute_command(
                f"/bin/cat /etc/group | /bin/grep {data[4]} | /bin/cut -d: -f1", False))[0]))

        return user_list

    async def add_user(self, name: str, home: str, shell: str, password: str, main_group: Optional[str] = None) -> None:
        """Add a user to the system.

        Args:
            name: The username of the new user.
            home: The home directory.
            shell: The sell witch user use.
            password: The password of the new user.
            main_group: The main group of the new user, is optional.

        Raises:
            UserExistError: If the user already exist.
            UserPermissionError: If you don't have sudo privileges to add user.
            GroupNotExistError: If you try to add the new user in nonexistent group.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self.command_manager.execute_command(f"/sbin/useradd {name} -m -d {home} -s {shell}"
                                                       f"{main_group if f' -g {main_group}' else ''}", True)
            await self._change_password(name, password)
        except CommandError as command_error:
            match command_error.status_code:
                case 1:
                    raise UserPermissionError(name)
                case 6:
                    raise GroupNotExistError(name)
                case 9:
                    raise UserExistError(name)
            raise command_error

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
        """
        params: dict[str, str | None] = {"l": new_name, "d": home, "s": shell, "g": main_group}
        command: str = f"/sbin/usermod {name}"

        for param, value in params.items():
            if value is not None:
                command += f" -{param} {value}"

        try:
            await self.command_manager.execute_command(command, True)

            if password is not None:
                await self._change_password(name, password)
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

    async def _change_password(self, name: str, password: str) -> None:
        """Change the password of user.

        Args:
            name: The username of the user to change password.
            password: The new password.

        Raises:
            UserPermissionError: If you don't have sudo privileges to manage user.
            CommandError: If the exit code is not unexpected.
        """
        try:
            await self.command_manager.execute_command(f"/bin/passwd {name}", True, password, password)
        except CommandError as command_error:
            if command_error.status_code == 1:
                raise UserPermissionError(name)
            raise command_error
