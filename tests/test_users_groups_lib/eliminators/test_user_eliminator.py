"""Test user eliminator."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import UserPermissionError, UserNotExistError, UserInUseError
from users_groups_lib.managers.eliminators import UserEliminator


class TestUserEliminator(unittest.IsolatedAsyncioTestCase):
    """Test user eliminator."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_eliminator = UserEliminator(CommandManager("augusto", "augusto"))

    async def test_delete_existing_user(self) -> None:
        """Test correctly functioning of command managers when delte user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_eliminator.delete_user("javier")

    async def test_delete_user_without_sudo(self) -> None:
        """Test error when attempting to delete user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
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
