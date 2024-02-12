"""Test user modifier."""
import unittest
from unittest import mock

from shell_executor_lib import CommandManager, CommandError

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import GroupNotExistError
from users_groups_lib.managers.modifiers import UserModifier


class TestUserModifier(unittest.IsolatedAsyncioTestCase):
    """Test user modifier."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_modifier = UserModifier(CommandManager("augusto", "augusto"))

    async def test_modify_username(self) -> None:
        """Test correctly functioning when modify username of user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_modifier.modify_username("javier", "javier_new")

    async def test_modify_home(self) -> None:
        """Test correctly functioning when modify home of user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_modifier.modify_home("javier", "/home/javier")

    async def test_modify_shell(self) -> None:
        """Test correctly functioning when modify shell of user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_modifier.modify_shell("javier", "/bin/sh")

    async def test_modify_password(self) -> None:
        """Test correctly functioning when modify password of user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_modifier.modify_password("javier", "pass")

    async def test_modify_main_group(self) -> None:
        """Test correctly functioning when modify main group of user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_modifier.modify_main_group("javier", "juan")

    async def test_modify_nonexistent_main_group_in_user(self) -> None:
        """Test error when change the main group of user in nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "Group not exist")):
            with self.assertRaises(GroupNotExistError):
                await self.user_modifier.modify_main_group("javier", "juan")

    async def test_modify_main_group_in_user_unknown_error(self) -> None:
        """Test error when de change main group returns non excepted error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "Unknown error")):
            with self.assertRaises(CommandError):
                await self.user_modifier.modify_main_group("javier", "juan")
