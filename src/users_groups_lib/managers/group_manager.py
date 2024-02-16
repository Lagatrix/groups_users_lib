"""Manage unix groups in shell."""

from shell_executor_lib import CommandManager

from users_groups_lib import Group
from users_groups_lib.managers.eliminators import GroupEliminator
from users_groups_lib.managers.getters import GroupGetter
from users_groups_lib.managers.inserters import GroupInserter
from users_groups_lib.managers.modifiers.group_modifier import GroupModifier


class GroupManager:
    """Manage unix groups in shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupManager.

        Args:
            command_manager: To make commands in the shell.
        """
        self.__group_getter: GroupGetter = GroupGetter(command_manager)
        self.__group_inserter: GroupInserter = GroupInserter(command_manager)
        self.__group_modifier: GroupModifier = GroupModifier(command_manager)
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

    async def edit_group(self, group: str, new_group: Group) -> None:
        """Edit the name of a group in the shell.

        Args:
            group: The group to edit.
            new_group: Changes to apply to the group.

        Raises:
            GroupExistError: If the new name of the group already exists.
            GroupNotExistError: If the group to modify doesn't exist.
            CommandError:  If the command return an unknown exit code.
        """
        await self.__group_modifier.modify_name(group, new_group.name)

    async def add_user_to_group(self, group: Group, username: str) -> None:
        """Add a user to a group.

        Args:
            group: The group to add the user to.
            username: The user to add to the group.

        Raises:
            UserNotExistError: If the user doesn't exist.
            GroupNotExistError: If the group doesn't exist.
            CommandError:  If the command return an unknown exit code.
        """
        await self.__group_getter.get_group(group.name)
        await self.__group_modifier.add_user_to_group(username, group.name)

    async def remove_user_from_group(self, group: Group, username: str) -> None:
        """Remove a user from a group.

        Args:
            group: The group to remove the user from.
            username: The user to remove from the group.

        Raises:
            UserNotExistError: If the user doesn't exist.
            GroupNotExistError: If the group doesn't exist.
            CommandError:  If the command return an unknown exit code.
        """
        await self.__group_getter.get_group(group.name)
        await self.__group_modifier.remove_user_from_group(username, group.name)

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
