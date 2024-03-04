"""Test user eliminator."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from tests.mock_groups_users_lib import mock_command_executor_method
from groups_users_lib import UserNotExistError, UserInUseError
from groups_users_lib.managers.eliminators import UserEliminator


class TestUserEliminator(unittest.IsolatedAsyncioTestCase):
    """Test user eliminator."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_eliminator = UserEliminator(CommandManager("augusto", "augusto"))

    async def test_delete_existing_user(self) -> None:
        """Test correctly functioning of command managers when delete user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_eliminator.delete_user("javier")

    async def test_delete_nonexistent_user(self) -> None:
        """Test error when attempting to delete a nonexistent user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "user not exist")):
            with self.assertRaises(UserNotExistError):
                await self.user_eliminator.delete_user("javier")

    async def test_delete_user_in_use(self) -> None:
        """Test error when attempting to delete user in use."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(8, "user in use")):
            with self.assertRaises(UserInUseError):
                await self.user_eliminator.delete_user("javier")

    async def test_delete_user_unknown_exit(self) -> None:
        """Test error when the command return unknown exit."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(978, "¿?")):
            with self.assertRaises(CommandError):
                await self.user_eliminator.delete_user("javier")
