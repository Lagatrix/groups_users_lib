"""Test the group manager."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager

from mock_users_groups_lib import mock_command_executor_method
from mock_users_groups_lib.mocks_group_manager import mock_groups_list, mock_groups_entities
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
