"""Manage unix users in shell."""
from shell_executor_lib import CommandManager

from users_groups_lib.entities import User
from users_groups_lib.managers.eliminators import UserEliminator
from users_groups_lib.managers.getters import UserGetter
from users_groups_lib.managers.getters.group_getter import GroupGetter
from users_groups_lib.managers.inserters import UserInserter
from users_groups_lib.managers.modifiers.user_modifier import UserModifier


class UserManager:
    """Manage unix users in shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserManager.

        Args:
            command_manager: To make  commands in the shell.
        """
        self.user_getter: UserGetter = UserGetter(command_manager)
        self.user_inserter: UserInserter = UserInserter(command_manager)
        self.user_eliminator: UserEliminator = UserEliminator(command_manager)
        self.user_modifier: UserModifier = UserModifier(command_manager)
        self.group_getter: GroupGetter = GroupGetter(command_manager)

    async def get_users(self) -> list[User]:
        """Obtain the users from the shell in a list.

        Returns:
            A list of the users in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        user_list: list[User] = await self.user_getter.get_users()

        for user in user_list:
            user.main_group = (await self.group_getter.get_group(int(user.main_group))).name

        return user_list

    async def get_user(self, user_name: str) -> User:
        """Obtain a user from the shell.

        Returns:
            The user.

        Raises:
            UserExistError: If the user not exist.
            CommandError: If the exit code is not 0.
        """
        user: User = await self.user_getter.get_user(user_name)

        user.main_group = (await self.group_getter.get_group(int(user.main_group))).name

        return user

    async def add_user(self, user: User, password: str) -> None:
        """Add a user to the system.

        Args:
            user: The new user.
            password: The password of the new user.

        Raises:
            UserExistError: If the user already exist.
            UserPermissionError: If you don't have sudo privileges to add user.
            GroupNotExistError: If you try to add the new user in nonexistent group.
            CommandError: If the exit code is not unexpected.
        """
        await self.user_inserter.add_user(user.name, user.home, user.shell, user.main_group)
        await self.user_modifier.change_password(user.name, password)

    async def edit_user(self, name: str, modify_user: User, password: str) -> None:
        """Edit a user to the system.

        Args:
            name: Username of user to edit.
            modify_user: The changes of the user.
            password: New password of the user.

        Raises:
            UserExistError: If you put a username of existent user.
            UserPermissionError: If you don't have sudo privileges to edit user.
            GroupNotExistError: If you try to add the user in nonexistent group.
            UserNotExistError: If you try to edit nonexistent user.
            CommandError: If the exit code is not unexpected.
        """
        await self.user_modifier.edit_user(name, modify_user.name, modify_user.home, modify_user.shell,
                                           modify_user.main_group)
        await self.user_modifier.change_password(modify_user.name, password)

    async def delete_user(self, user: User) -> None:
        """Delete user of the system.

        Args:
            user: The User to delete.

        Raises:
            UserInUseError: If you try to delete a user in use.
            UserPermissionError: If you don't have sudo privileges to edit user.
            UserNotExistError: If you try to delete nonexistent user.
            CommandError: If the exit code is not unexpected.
        """
        await self.user_eliminator.delete_user(user.name)