"""Test the user manager."""

import unittest
from unittest import mock

from mock_users_groups_lib import mock_users_list, mock_group_name_list
from users_groups_lib import UserManager, User


class MockCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the user manager."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_manager = UserManager("augusto", "augusto")

    async def test_get_users(self) -> None:
        """Test correctly functioning of command manager."""
        with mock.patch('shell_executor_lib.CommandManager.execute_command',
                        side_effect=(mock_users_list, mock_group_name_list, mock_group_name_list)):
            self.assertEqual(await self.user_manager.get_users(), [
                User(1000, "javier", "/bin/bash", "/home/javier", "javier"),
                User(1001, "pepe", "/bin/bash", "/home/pepe", "javier")])
