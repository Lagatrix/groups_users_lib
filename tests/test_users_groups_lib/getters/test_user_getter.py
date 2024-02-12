"""Test user getter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager

from mock_users_groups_lib import mock_users_list, mock_group_name_list, mock_user, mock_command_executor_method
from users_groups_lib import User, UserNotExistError
from users_groups_lib.managers.getters import UserGetter


class TestUserGetter(unittest.IsolatedAsyncioTestCase):
    """Test user getter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_getter = UserGetter(CommandManager("augusto", "augusto"))

    async def test_get_users(self) -> None:
        """Test correctly functioning of command managers when get users."""
        with mock.patch(mock_command_executor_method,
                        side_effect=(mock_users_list, mock_group_name_list, mock_group_name_list)):
            self.assertEqual(await self.user_getter.get_users(), [
                User(1000, "javier", "/bin/bash", "/home/javier", "1000"),
                User(1001, "pepe", "/bin/bash", "/home/pepe", "1000")])

    async def test_get_user(self) -> None:
        """Test correctly functioning of command managers when get a user."""
        with mock.patch(mock_command_executor_method,
                        side_effect=(mock_users_list, mock_group_name_list, mock_user)):
            self.assertEqual(await self.user_getter.get_user("javier"),
                             User(1000, "javier", "/bin/bash", "/home/javier", "1000"))

    async def test_get_nonexistent_user(self) -> None:
        """Test error when try getting nonexistent user."""
        with mock.patch(mock_command_executor_method,
                        return_value=[]):
            with self.assertRaises(UserNotExistError):
                self.assertEqual(await self.user_getter.get_user("javier"),
                                 User(1000, "javier", "/bin/bash", "/home/javier", "1000"))
