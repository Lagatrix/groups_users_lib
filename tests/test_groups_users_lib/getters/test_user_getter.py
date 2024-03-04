"""Test user getter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager

from tests.mock_groups_users_lib import (mock_users_list, mock_group_name_list, mock_user,
                                         mock_command_executor_method, mock_users_list_entities_without_group_name,
                                         mock_user_entity_group_name)
from groups_users_lib import UserNotExistError
from groups_users_lib.managers.getters import UserGetter


class TestUserGetter(unittest.IsolatedAsyncioTestCase):
    """Test user getter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_getter = UserGetter(CommandManager("augusto", "augusto"))

    async def test_get_users(self) -> None:
        """Test correctly functioning of command managers when get users."""
        with mock.patch(mock_command_executor_method,
                        side_effect=(mock_users_list, mock_group_name_list, mock_group_name_list)):
            self.assertEqual(await self.user_getter.get_users(), mock_users_list_entities_without_group_name)

    async def test_get_user(self) -> None:
        """Test correctly functioning of command managers when get a user."""
        with mock.patch(mock_command_executor_method,
                        side_effect=(mock_users_list, mock_group_name_list, mock_user)):
            self.assertEqual(await self.user_getter.get_user("javier"), mock_user_entity_group_name)

    async def test_get_nonexistent_user(self) -> None:
        """Test error when try getting nonexistent user."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            with self.assertRaises(UserNotExistError):
                await self.user_getter.get_user("javier")
