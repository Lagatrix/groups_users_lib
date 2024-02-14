"""Test group inserter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from mock_users_groups_lib import mock_command_executor_method
from users_groups_lib import GroupExistError, UserNotExistError
from users_groups_lib.errors import GroupPermissionError
from users_groups_lib.managers.inserters.group_inserter import GroupInserter


class TestGroupInserter(unittest.IsolatedAsyncioTestCase):
    """Test group inserter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_inserter = GroupInserter(CommandManager("augusto", "augusto"))

    async def test_add_user(self) -> None:
        """Test correctly functioning of command managers when add group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_inserter.add_group("javier", ["juan", "javier"])

    async def test_add_group(self) -> None:
        """Test correctly functioning of command managers when add group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_inserter.add_group("javier")

    async def test_add_user_with_group(self) -> None:
        """Test correctly functioning of command managers when add group with users."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_inserter.add_group("javier", ["juan", "javier"])

    async def test_add_group_without_sudo(self) -> None:
        """Test error when attempting to add group without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(GroupPermissionError):
                await self.group_inserter.add_group("javier")

    async def test_add_existing_group(self) -> None:
        """Test error when attempting to add an existing group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "Group exist")):
            with self.assertRaises(GroupExistError):
                await self.group_inserter.add_group("javier")

    async def test_add_nonexistent_user_on_group(self) -> None:
        """Test error when attempting to add a nonexistent user into group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(10, "Invalid member username juan")):
            with self.assertRaises(UserNotExistError):
                await self.group_inserter.add_group("javier", ["juan", "javier"])

    async def test_add_group_unknown_error(self) -> None:
        """Test error when the add group command returns unexpected error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(14, "Unknown error")):
            with self.assertRaises(CommandError):
                await self.group_inserter.add_group("javier")
