"""Manage unix groups in shell."""

from shell_executor_lib import CommandManager

from users_groups_lib import Group
from users_groups_lib.managers.eliminators import GroupEliminator
from users_groups_lib.managers.getters import GroupGetter
from users_groups_lib.managers.inserters import GroupInserter


class GroupManager:
    """Manage unix groups in shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupManager.

        Args:
            command_manager: To make commands in the shell.
        """
        self.__group_getter: GroupGetter = GroupGetter(command_manager)
        self.__group_inserter: GroupInserter = GroupInserter(command_manager)
        self.__group_eliminator: GroupEliminator = GroupEliminator(command_manager)

    async def get_groups(self) -> list[Group]:
        """Obtain the groups from the shell in a list.

        Returns:
            A list of the groups in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        return await self.__group_getter.get_groups()

    async def add_group(self, group: Group) -> None:
        """Add a group to the shell.

        Args:
            group: The group to add to the shell.

        Raises:
            GroupPermissionError: If the user does not have permission to add the group.
            GroupExistError: If the group already exists.
            CommandError: If the command return an unknown exit code.
        """
        await self.__group_inserter.add_group(group.name, group.users)

    async def delete_group(self, group: Group) -> None:
        """Delete a group to the shell.

        Args:
            group: The group to add to the shell.

        Raises:
            GroupPermissionError: If the user does not have permission to delete the group.
            GroupNotExistError: If the group does not exist.
            GroupInUseError: If the group is in use.
            CommandError: If the command return an unknown exit code.
        """
        await self.__group_eliminator.delete_group(group.name)
