"""Test group getter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager

from mock_users_groups_lib import mock_command_executor_method
from mock_users_groups_lib.mocks_group_manager import mock_groups_list, mock_groups_entities, mock_groups_entity, \
    mock_group
from users_groups_lib.managers.getters.group_getter import GroupGetter


class TestUserGetter(unittest.IsolatedAsyncioTestCase):
    """Test group getter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_getter = GroupGetter(CommandManager("augusto", "augusto"))

    async def test_get_groups(self) -> None:
        """Test correctly functioning of command managers when get groups."""
        with mock.patch(mock_command_executor_method, return_value=mock_groups_list):
            self.assertEqual(await self.group_getter.get_groups(), mock_groups_entities)

    async def test_get_group(self) -> None:
        """Test correctly functioning of command managers when get a group."""
        with mock.patch(mock_command_executor_method, return_value=mock_group):
            self.assertEqual(await self.group_getter.get_group(1000), mock_groups_entity)
