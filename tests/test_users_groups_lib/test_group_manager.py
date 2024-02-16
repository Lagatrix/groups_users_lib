"""Test the group manager."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager

from mock_users_groups_lib import mock_command_executor_method
from mock_users_groups_lib.mocks_group_manager import mock_groups_list, mock_groups_entities, mock_groups_entity, \
    mock_group
from users_groups_lib import GroupNotExistError
from users_groups_lib.managers.group_manager import GroupManager


class MockCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the group manager."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_manager = GroupManager(CommandManager("augusto", "augusto"))

    async def test_get_groups(self) -> None:
        """Test correctly functioning of command managers when get groups."""
        with mock.patch(mock_command_executor_method, return_value=mock_groups_list):
            self.assertEqual(await self.group_manager.get_groups(), mock_groups_entities)

    async def test_add_group(self) -> None:
        """Test correctly functioning of command managers when add group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_manager.add_group(mock_groups_entity)

    async def test_delete_group(self) -> None:
        """Test correctly functioning of command managers when delete group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_manager.delete_group(mock_groups_entity)

    async def test_edit_group(self) -> None:
        """Test correctly functioning of command managers when modify group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.group_manager.edit_group("javier2", mock_groups_entity)

    async def test_add_user_to_group(self) -> None:
        """Test correctly functioning of command managers when add user to group."""
        with mock.patch(mock_command_executor_method, side_effect=(mock_group, [])):
            await self.group_manager.add_user_to_group(mock_groups_entity, "augusto")

    async def test_add_user_to_nonexistent_group(self) -> None:
        """Test correctly functioning of command managers when add user to nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=GroupNotExistError("")):
            with self.assertRaises(GroupNotExistError):
                await self.group_manager.add_user_to_group(mock_groups_entity, "augusto")

    async def test_remove_user_from_group(self) -> None:
        """Test correctly functioning of command managers when delete user from group."""
        with mock.patch(mock_command_executor_method, side_effect=(mock_group, [])):
            await self.group_manager.remove_user_from_group(mock_groups_entity, "augusto")

    async def test_remove_user_from_nonexistent_group(self) -> None:
        """Test correctly functioning of command managers when delete user from nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=GroupNotExistError("")):
            with self.assertRaises(GroupNotExistError):
                await self.group_manager.remove_user_from_group(mock_groups_entity, "augusto")
