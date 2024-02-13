"""Get groups from the shell."""
from shell_executor_lib import CommandManager

from users_groups_lib.entities import Group


class GroupGetter:
    """Get groups from the shell."""
    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupGetter.

        Args:
            command_manager: To make commands in the shell.
        """
        self._command_manager: CommandManager = command_manager

    async def get_groups(self) -> list[Group]:
        """Obtain the groups from the shell in a list.

        Returns:
            A map of groups and names of users.

        Raises:
            CommandError: If the exit code is not 0.
        """
        group_list: list[Group] = []

        data_list: list[str] = await self._command_manager.execute_command(
            "/bin/cat /etc/group | /bin/awk -F : '{print $1,$3,$4}'", False)

        for data_row in data_list:
            data: list[str] = data_row.split(" ")

            group_list.append(Group(int(data[1]), data[0], data[2].split(",")))

        return group_list

    async def get_group(self, gid: int) -> Group:
        """Obtain the groups from the shell in a list.

        Args:
            gid: The GID of the group.

        Returns:
            The group.

        Raises:
            CommandError: If the exit code is not 0.
        """
        data: list[str] = (await self._command_manager.execute_command(
            "/bin/cat /etc/group | /bin/awk -F : '{print $1,$3,$4}'" + f" | grep {gid}", False))[0].split(" ")

        return Group(int(data[1]), data[0], data[2].split(","))
