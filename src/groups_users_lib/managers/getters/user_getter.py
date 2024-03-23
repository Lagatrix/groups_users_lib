"""Get users from the shell."""
from typing import AsyncIterable

from shell_executor_lib import CommandManager, CommandError
from groups_users_lib import UserNotExistError


class UserGetter:
    """Get users from the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserGetter.

        Args:
            command_manager: To make commands in the shell.
        """
        self._command_manager = command_manager

    async def get_users(self) -> AsyncIterable[tuple[int, str, str, str, int]]:
        """Obtain the users from the shell in a list.

        Returns:
            A tuple with the user id, name, shell, home and group id.

        Raises:
            CommandError: If the exit code is not 0.
        """
        data_list: list[str] = await self._command_manager.execute_command(
            "/bin/cat /etc/passwd | /bin/awk -F : '{print \\$3,\\$1,\\$7,\\$6,\\$4}'", False)

        for data_row in data_list:
            data: list[str] = data_row.split(" ")

            yield int(data[0]), data[1], data[2], data[3], int(data[4])

    async def get_user(self, user_name: str) -> tuple[int, str, str, str, int]:
        """Obtain a user from the shell.

        Returns:
            A tuple with the user id, name, shell, home and group id.

        Raises:
            UserExistError: If the user not exist.
            CommandError: If the error is not excepted.
        """
        try:
            data_user: list[str] = await self._command_manager.execute_command(
                "/bin/cat /etc/passwd | /bin/awk -F : '{print \\$3,\\$1,\\$7,\\$6,\\$4}'" + f"| grep {user_name}",
                False)

            if len(data_user) > 0:
                data: list[str] = data_user[0].split(" ")
                if len(data) > 2:
                    return int(data[0]), data[1], data[2], data[3], int(data[4])

        except CommandError as error:
            if error.status_code != 1:
                raise error

        raise UserNotExistError(user_name)
