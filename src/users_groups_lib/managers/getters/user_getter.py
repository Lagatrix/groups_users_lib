"""Get users from the shell."""
from shell_executor_lib import CommandManager
from users_groups_lib import User, UserNotExistError


class UserGetter:
    """Get users from the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserGetter.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def get_users(self) -> list[User]:
        """Obtain the users from the shell in a list.

        Returns:
            A list of the users in the shell without main group.

        Raises:
            CommandError: If the exit code is not 0.
        """
        user_list: list[User] = []

        data_list: list[str] = await self._command_manager.execute_command(
            "/bin/cat /etc/passwd | /bin/awk -F : '{print $3,$1,$7,$6,$4 }'", False)

        for data_row in data_list:
            data: list[str] = data_row.split(" ")

            user_list.append(User(int(data[0]), data[1], data[2], data[3], data[4]))

        return user_list

    async def get_user(self, user_name: str) -> User:
        """Obtain a user from the shell.

        Returns:
            The user without group name.

        Raises:
            UserExistError: If the user not exist.
            CommandError: If the exit code is not 0.
        """
        data_user: list[str] = await self._command_manager.execute_command(
            "/bin/cat /etc/passwd | /bin/awk -F : '{print $3,$1,$7,$6,$4}'" + f"| grep {user_name}", False)

        if len(data_user) < 1:
            raise UserNotExistError(user_name)

        data: list[str] = data_user[0].split(" ")

        return User(int(data[0]), data[1], data[2], data[3], data[4])
