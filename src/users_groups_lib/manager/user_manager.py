"""Manage unix users in shell."""
from shell_executor_lib import CommandManager

from users_groups_lib.entities import User


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
