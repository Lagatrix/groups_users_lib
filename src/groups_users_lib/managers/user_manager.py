"""Manage unix users in shell."""
from typing import Optional

from shell_executor_lib import CommandManager

from groups_users_lib.entities import User
from groups_users_lib.managers.eliminators import UserEliminator
from groups_users_lib.managers.getters import UserGetter
from groups_users_lib.managers.getters import GroupGetter
from groups_users_lib.managers.inserters import UserInserter
from groups_users_lib.managers.modifiers.user_modifier import UserModifier


class UserManager:
    """Manage unix users in shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the UserManager.

        Args:
            command_manager: To make commands in the shell.
        """
        self.__user_getter: UserGetter = UserGetter(command_manager)
        self.__user_inserter: UserInserter = UserInserter(command_manager)
        self.__user_eliminator: UserEliminator = UserEliminator(command_manager)
        self.__user_modifier: UserModifier = UserModifier(command_manager)
        self.__group_getter: GroupGetter = GroupGetter(command_manager)

    async def get_users(self) -> list[User]:
        """Obtain the users from the shell in a list.

        Returns:
            A list of the users in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        user_list: list[User] = []

        async for user_tuple in self.__user_getter.get_users():
            user_list.append(User(
                uid=user_tuple[0],
                name=user_tuple[1],
                shell=user_tuple[2],  # noqa
                home=user_tuple[3],
                main_group=(await self.__group_getter.get_group(user_tuple[0]))[1]
            ))

        return user_list

    async def get_user(self, user_name: str) -> User:
        """Obtain a user from the shell.

        Returns:
            The user.

        Raises:
            UserNotExistError: If the user not exist.
            CommandError: If the exit code is not 0.
        """
        user_tuple: tuple[int, str, str, str, int] = await self.__user_getter.get_user(user_name)

        return User(
                uid=user_tuple[0],
                name=user_tuple[1],
                shell=user_tuple[2], # noqa
                home=user_tuple[3],
                main_group=(await self.__group_getter.get_group(user_tuple[0]))[1]
            )

    async def add_user(self, user: User) -> None:
        """Add a user to the system.

        Args:
            user: The new user.

        Raises:
            UserExistError: If the user already exist.
            GroupNotExistError: If you try to add the new user in nonexistent group.
            CommandError: If the exit code is not unexpected.
            PrivilegesError: If the user doesn't have sudo privileges.
            ValueError: If the user don't have name, home and shell.
        """
        if user.name and user.home and user.shell and user.password is not None:
            await self.__user_inserter.add_user(user.name, user.home, user.shell, user.main_group)
            await self.__user_modifier.modify_password(user.name, user.password)
        else:
            raise ValueError("The user must have name, home, password and shell")

    async def edit_user(self, name: str, modify_user: User, password: Optional[str] = None) -> None:
        """Edit a user to the system.

        Args:
            name: Username of user to edit.
            modify_user: The changes of the user.
            password: New password of the user.

        Raises:
            UserExistError: If you put a username of existent user.
            GroupNotExistError: If you try to add the user in nonexistent group.
            UserNotExistError: If you try to edit nonexistent user.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the exit code is not unexpected.
        """
        await self.__user_getter.get_user(name)

        if modify_user.main_group is not None:
            await self.__user_modifier.modify_main_group(name, modify_user.main_group)

        if modify_user.name is not None:
            await self.__user_modifier.modify_username(name, modify_user.name)

        if modify_user.home is not None:
            await self.__user_modifier.modify_home(name, modify_user.home)

        if modify_user.shell is not None:
            await self.__user_modifier.modify_shell(name, modify_user.shell)

        if password is not None:
            await self.__user_modifier.modify_password(modify_user.name if modify_user.name else name, password)

    async def delete_user(self, username: str) -> None:
        """Delete user of the system.

        Args:
            username: The username of user to delete.

        Raises:
            UserInUseError: If you try to delete a user in use.
            UserNotExistError: If you try to delete nonexistent user.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError: If the exit code is not unexpected.
        """
        await self.__user_eliminator.delete_user(username)
