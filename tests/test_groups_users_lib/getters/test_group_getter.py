"""Test group getter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager, CommandError

from tests.mock_groups_users_lib import mock_command_executor_method
from tests.mock_groups_users_lib.mocks_group_manager import (mock_groups_list, mock_group, mock_group_tuple_list,
                                                             mock_group_tuple)
from groups_users_lib import GroupNotExistError
from groups_users_lib.managers.getters.group_getter import GroupGetter


class TestUserGetter(unittest.IsolatedAsyncioTestCase):
    """Test group getter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.group_getter = GroupGetter(CommandManager("augusto", "augusto"))

    async def test_get_groups(self) -> None:
        """Test correctly functioning of command managers when get groups."""
        with mock.patch(mock_command_executor_method, return_value=mock_groups_list):
            group_tuples = [group async for group in self.group_getter.get_groups()]
            self.assertEqual(group_tuples, mock_group_tuple_list)

    async def test_get_group(self) -> None:
        """Test correctly functioning of command managers when get a group."""
        with mock.patch(mock_command_executor_method, return_value=mock_group):
            self.assertEqual(await self.group_getter.get_group(1000), mock_group_tuple)

    async def test_get_empty_group(self) -> None:
        """Test error when trying to get empty group."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            with self.assertRaises(GroupNotExistError):
                await self.group_getter.get_group("javier2")

    async def test_get_nonexistent_group(self) -> None:
        """Test error when trying to get nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "exit code 1")):
            with self.assertRaises(GroupNotExistError):
                await self.group_getter.get_group("javier2")

    async def test_get_group_unknown_error(self) -> None:
        """Test error when trying to get group with unknown error."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(2, "exit code 2")):
            with self.assertRaises(CommandError):
                await self.group_getter.get_group("javier2")
