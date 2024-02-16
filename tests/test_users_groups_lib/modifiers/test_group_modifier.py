"""Test group modifier."""
import unittest
from unittest import mock

from shell_executor_lib import CommandManager, CommandError

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import UserNotExistError, GroupExistError, GroupPermissionError, GroupNotExistError
from users_groups_lib.errors import NoUserInGroupError
from users_groups_lib.managers.modifiers.group_modifier import GroupModifier


class TestGroupModifier(unittest.IsolatedAsyncioTestCase):
    """Test group modifier."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_modifier = GroupModifier(CommandManager("augusto", "augusto"))

    async def test_modify_name(self) -> None:
        """Test correctly functioning when modify name of group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_modifier.modify_name("javier", "javier_new")

    async def test_modify_name_group_not_exist_error(self) -> None:
        """Test error when modify name of group returns group not exist error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "Group not exist")):
            with self.assertRaises(GroupNotExistError):
                await self.group_modifier.modify_name("javier", "javier_new")

    async def test_modify_name_group_exist_error(self) -> None:
        """Test error when modify name of group returns group exist error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "Group exist")):
            with self.assertRaises(GroupExistError):
                await self.group_modifier.modify_name("javier", "javier_new")

    async def test_modify_name_group_without_permission(self) -> None:
        """Test error when modify name of group without permission."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No permission")):
            with self.assertRaises(GroupPermissionError):
                await self.group_modifier.modify_name("javier", "javier2")

    async def test_modify_name_unknown_error(self) -> None:
        """Test error when modify name of group returns non excepted error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(45, "Unknown error")):
            with self.assertRaises(CommandError):
                await self.group_modifier.modify_name("javier", "javier_new")

    async def test_add_user_to_group(self) -> None:
        """Test correctly functioning when add user to group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_modifier.add_user_to_group("javier", "juan")

    async def test_add_user_to_group_user_not_exist_error(self) -> None:
        """Test error when add user to group returns user not exist error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "User not exist")):
            with self.assertRaises(UserNotExistError):
                await self.group_modifier.add_user_to_group("javier", "juan")

    async def test_add_user_to_group_unknown_error(self) -> None:
        """Test error when add user to group returns non excepted error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "Unknown error")):
            with self.assertRaises(CommandError):
                await self.group_modifier.add_user_to_group("javier", "juan")

    async def test_add_user_without_permission(self) -> None:
        """Test error when add user to group without permission."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No permission")):
            with self.assertRaises(GroupPermissionError):
                await self.group_modifier.add_user_to_group("javier", "juan")

    async def test_remove_user_from_group(self) -> None:
        """Test correctly functioning when remove user from group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_modifier.remove_user_from_group("javier", "juan")

    async def test_remove_user_who_is_not_in_group(self) -> None:
        """Test error when remove user from group returns user not in group error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(3, "User not in group")):
            with self.assertRaises(NoUserInGroupError):
                await self.group_modifier.remove_user_from_group("javier", "juan")

    async def test_remove_user_from_group_unknown_error(self) -> None:
        """Test error when remove user from group returns non excepted error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "Unknown error")):
            with self.assertRaises(CommandError):
                await self.group_modifier.remove_user_from_group("javier", "juan")

    async def test_remove_user_without_permission(self) -> None:
        """Test error when remove user from group without permission."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No permission")):
            with self.assertRaises(GroupPermissionError):
                await self.group_modifier.remove_user_from_group("javier", "juan")
