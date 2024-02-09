"""Test user modifier."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import UserPermissionError, UserExistError, GroupNotExistError, UserNotExistError
from users_groups_lib.managers.modifiers import UserModifier


class TestUserModifier(unittest.IsolatedAsyncioTestCase):
    """Test user modifier."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_modifier = UserModifier(CommandManager("augusto", "augusto"))

    async def test_edit_existing_user(self) -> None:
        """Test correctly functioning of command managers when edit user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_edit_user_without_sudo(self) -> None:
        """Test error when attempting to edit user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
                await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe")

        with mock.patch(mock_command_executor_method, side_effect=([], CommandError(1, "No sudo"))):
            with self.assertRaises(UserPermissionError):
                await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe", password="")

    async def test_edit_nonexistent_user(self) -> None:
        """Test error when attempting to edit a nonexistent user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "user not exist")):
            with self.assertRaises(UserNotExistError):
                await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_edit_nonexistent_main_group_in_user(self) -> None:
        """Test error when attempting to put user in nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "group not exist")):
            with self.assertRaises(GroupNotExistError):
                await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_put_name_of_existent_user(self) -> None:
        """Test error when attempting to change name of user and put existing name."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "group not exist")):
            with self.assertRaises(UserExistError):
                await self.user_modifier.edit_user("javier", home="/home/javier", main_group="pepe")
