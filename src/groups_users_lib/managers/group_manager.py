"""Manage unix groups in shell."""

from shell_executor_lib import CommandManager

from groups_users_lib import Group
from groups_users_lib.managers.eliminators import GroupEliminator
from groups_users_lib.managers.getters import GroupGetter
from groups_users_lib.managers.inserters import GroupInserter
from groups_users_lib.managers.modifiers.group_modifier import GroupModifier


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
        group_list: list[Group] = []

        async for group_tuple in self.__group_getter.get_groups():
            group_list.append(Group(
                gid=group_tuple[0],
                name=group_tuple[1],
                users=group_tuple[2],
            ))

        return group_list

    async def get_group(self, group_name: str) -> Group:
        """Obtain a group from the shell.

        Returns:
            The group.

        Raises:
            GroupNotExistError: If the group not exist.
            CommandError: If the exit code is not 0.
        """
        group_tuple: tuple[int, str, list[str]] = await self.__group_getter.get_group(group_name)
        return Group(
            gid=group_tuple[0],
            name=group_tuple[1],
            users=group_tuple[2],
        )

    async def add_group(self, group: Group) -> None:
        """Add a group to the shell.

        Args:
            group: The group to add to the shell.

        Raises:
            GroupExistError: If the group already exists.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the command return an unknown exit code.
        """
        if group.name and group.users is not None:
            await self.__group_inserter.add_group(group.name, group.users)
        else:
            raise ValueError("The new group must have a name and user list.")

    async def edit_group(self, group: str, new_group: Group) -> None:
        """Edit the name of a group in the shell.

        Args:
            group: The group to edit.
            new_group: Changes to apply to the group.

        Raises:
            GroupNotExistError: If the group to modify doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            ValueError: If the new group doesn't have a name.
            CommandError:  If the command return an unknown exit code.
        """
        if new_group.users is not None:
            await self.__group_modifier.modify_users(group, new_group.users)

        if new_group.name is not None:
            await self.__group_modifier.modify_name(group, new_group.name)
        else:
            raise ValueError("The new group must have a name.")

    async def add_user_to_group(self, group_name: str, username: str) -> None:
        """Add a user to a group.

        Args:
            group_name: The group to add the user to.
            username: The user to add to the group.

        Raises:
            UserNotExistError: If the user doesn't exist.
            GroupNotExistError: If the group doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        await self.__group_getter.get_group(group_name)
        await self.__group_modifier.add_user_to_group(username, group_name)

    async def remove_user_from_group(self, group_name: str, username: str) -> None:
        """Remove a user from a group.

        Args:
            group_name: The group to remove the user from.
            username: The user to remove from the group.

        Raises:
            UserNotExistError: If the user doesn't exist.
            GroupNotExistError: If the group doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        await self.__group_getter.get_group(group_name)
        await self.__group_modifier.remove_user_from_group(username, group_name)

    async def delete_group(self, group_name: str) -> None:
        """Delete a group to the shell.

        Args:
            group_name: The group to add to the shell.

        Raises:
            GroupNotExistError: If the group does not exist.
            GroupInUseError: If the group is in use.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the command return an unknown exit code.
        """
        await self.__group_eliminator.delete_group(group_name)
