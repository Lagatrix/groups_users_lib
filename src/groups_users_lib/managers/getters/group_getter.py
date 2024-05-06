"""Get groups from the shell."""
from typing import AsyncIterable

from shell_executor_lib import CommandManager, CommandError

from groups_users_lib import GroupNotExistError


class GroupGetter:
    """Get groups from the shell."""
    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupGetter.

        Args:
            command_manager: To make commands in the shell.
        """
        self._command_manager: CommandManager = command_manager

    async def get_groups(self) -> AsyncIterable[tuple[int, str, list[str]]]:
        """Obtain the groups from the shell in a list.

        Returns:
            A map of groups and names of users.

        Raises:
            CommandError: If the exit code is not 0.
        """
        data_list: list[str] = await self._command_manager.execute_command(
            "/bin/cat /etc/group | /bin/awk -F : '{print \\$1,\\$3,\\$4}'", False)

        for data_row in data_list:
            data: list[str] = data_row.split(" ")

            if len(data) > 2:
                yield int(data[1]), data[0], data[2].split(",") if data[2] != '' else []
            else:
                yield int(data[1]), data[0], []

    async def get_group(self, identification: int | str) -> tuple[int, str, list[str]]:
        """Obtain the groups from the shell in a list.

        Args:
            identification: Name or GID of the group.

        Returns:
            A tuple with the group id, name and list of users.

        Raises:
            GroupNotExistError: If the group not exist.
            CommandError:  If the error is not excepted.
        """
        try:
            data_group: list[str] = (await self._command_manager.execute_command(
                "/bin/cat /etc/group | /bin/awk -F : '{print \\$1,\\$3,\\$4}'" + f" | grep {identification}", False))

            if len(data_group) > 0:
                data: list[str] = data_group[0].split(" ")
                if len(data) > 1:
                    return int(data[1]), data[0], data[2].split(",") if len(data) > 2 else []

        except CommandError as error:
            if error.status_code != 1:
                raise error

        raise GroupNotExistError(identification)
