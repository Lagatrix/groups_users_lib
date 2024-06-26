"""Modify group in the shell."""
from shell_executor_lib import CommandManager, CommandError

from groups_users_lib import UserNotExistError, GroupExistError, GroupNotExistError
from groups_users_lib.errors import NoUserInGroupError


class GroupModifier:
    """Modify group in the shell."""

    def __init__(self, command_manager: CommandManager) -> None:
        """Initialize the GroupModifier.

        Args:
            command_manager: To make  commands in the shell.
        """
        self._command_manager = command_manager

    async def modify_name(self, old_name: str, new_name: str) -> None:
        """Modify the name of a group.

        Args:
            old_name: The old name of the group.
            new_name: The new name of the group.

        Raises:
            GroupPermissionError: If the user doesn't have permission to modify the group.
            GroupExistError: If the new name of the group already exists.
            GroupNotExistError: If the group to modify doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        try:
            await self._command_manager.execute_command(f"/usr/sbin/groupmod -n {new_name} {old_name}", True)
        except CommandError as command_error:
            if command_error.status_code == 6:
                raise GroupNotExistError(old_name)
            elif command_error.status_code == 9:
                raise GroupExistError(new_name)
            raise command_error

    async def modify_users(self, group: str, users: list[str]) -> None:
        """Modify the users of a group.

        Args:
            group: The group to modify.
            users: The new users of the group.

        Raises:
            GroupPermissionError: If the user doesn't have permission to modify the group.
            GroupNotExistError: If the group to modify doesn't exist.
            UserNotExistError: If a user doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        try:
            await self._command_manager.execute_command(f"/bin/gpasswd -M {','.join(users)} {group}", True)
        except CommandError as command_error:
            if command_error.status_code == 3:
                if "/etc/group" in command_error.response:
                    raise GroupNotExistError(group)
                else:
                    raise UserNotExistError(command_error.response[command_error.response.find("«") + 1:
                                                                   command_error.response.find("»")])
            raise command_error

    async def add_user_to_group(self, user: str, group: str) -> None:
        """Add a user to a group.

        Args:
            user: The user to add to the group.
            group: The group to add the user to.

        Raises:
            GroupPermissionError: If the user doesn't have permission to add users in the group.
            UserNotExistError: If the user doesn't exist.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        try:
            await self._command_manager.execute_command(f"/sbin/usermod -a -G {group} {user}", True)
        except CommandError as command_error:
            if command_error.status_code == 6:
                raise UserNotExistError(user)
            raise command_error

    async def remove_user_from_group(self, user: str, group: str) -> None:
        """Remove a user from a group.

        Args:
            user: The user to remove from the group.
            group: The group to remove the user from.

        Raises:
            GroupPermissionError: If the user doesn't have permission to delete users in the group.
            NoUserInGroupError: If the user is not in the group.
            PrivilegesError: If the user doesn't have sudo privileges.
            CommandError:  If the command return an unknown exit code.
        """
        try:
            await self._command_manager.execute_command(f"/bin/gpasswd -d {user} {group}", True)
        except CommandError as command_error:
            if command_error.status_code == 3:
                raise NoUserInGroupError(group, user)
            raise command_error
