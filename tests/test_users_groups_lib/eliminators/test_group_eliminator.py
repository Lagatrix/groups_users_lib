"""Test user eliminator."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import GroupNotExistError
from users_groups_lib.errors import GroupPermissionError, GroupInUseError
from users_groups_lib.managers.eliminators.group_eliminator import GroupEliminator


class GroupEliminatorTest(unittest.IsolatedAsyncioTestCase):
    """Test group eliminator."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_eliminator = GroupEliminator(CommandManager("augusto", "augusto"))

    async def test_delete_existing_group(self) -> None:
        """Test correctly functioning of command managers when delete group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_eliminator.delete_group("javier")

    async def test_delete_group_without_sudo(self) -> None:
        """Test error when attempting to delete group without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(GroupPermissionError):
                await self.group_eliminator.delete_group("javier")

    async def test_delete_nonexistent_group(self) -> None:
        """Test error when attempting to delete a nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "group not exist")):
            with self.assertRaises(GroupNotExistError):
                await self.group_eliminator.delete_group("javier")

    async def test_delete_group_in_use(self) -> None:
        """Test error when attempting to delete group in use."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(8, "group in use")):
            with self.assertRaises(GroupInUseError):
                await self.group_eliminator.delete_group("javier")

    async def test_delete_group_unknown_exit(self) -> None:
        """Test error when the command return unknown exit."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(978, "¿?")):
            with self.assertRaises(CommandError):
                await self.group_eliminator.delete_group("javier")
