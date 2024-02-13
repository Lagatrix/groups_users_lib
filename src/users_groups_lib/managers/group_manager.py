"""Manage unix groups in shell."""

from shell_executor_lib import CommandManager

from users_groups_lib import Group
from users_groups_lib.managers.getters import GroupGetter


class GroupManager:
    """Manage unix groups in shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupManager.

        Args:
            command_manager: To make commands in the shell.
        """
        self.__group_getter: GroupGetter = GroupGetter(command_manager)

    async def get_groups(self) -> list[Group]:
        """Obtain the groups from the shell in a list.

        Returns:
            A list of the groups in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        return await self.__group_getter.get_groups()
