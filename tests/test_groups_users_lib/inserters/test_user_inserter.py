"""Test user inserter."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError, CommandManager

from tests.mock_groups_users_lib import mock_command_executor_method
from groups_users_lib import UserExistError, GroupNotExistError
from groups_users_lib.managers.inserters import UserInserter


class TestUserInserter(unittest.IsolatedAsyncioTestCase):
    """Test user inserter."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_inserter = UserInserter(CommandManager("augusto", "augusto"))

    async def test_add_user(self) -> None:
        """Test correctly functioning of command managers when add user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_inserter.add_user("javier", "/home/javier", "/bin/bash")

    async def test_add_user_with_group(self) -> None:
        """Test correctly functioning of command managers when add user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_inserter.add_user("javier", "/home/javier", "/bin/bash", "javier")

    async def test_add_existing_user(self) -> None:
        """Test error when attempting to add an existing user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "User exist")):
            with self.assertRaises(UserExistError):
                await self.user_inserter.add_user("javier", "/home/javier", "/bin/bash", "javier")

    async def test_add_user_on_nonexistent_group(self) -> None:
        """Test error when attempting to add a user into nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=(CommandError(6, "Group not exist"))):
            with self.assertRaises(GroupNotExistError):
                await self.user_inserter.add_user("javier", "/home/javier", "/bin/bash", "javier")

    async def test_add_user_unknown_error(self) -> None:
        """Test error when the add user command returns unexpected error."""
        with mock.patch(mock_command_executor_method, side_effect=(CommandError(10, "Unknown error"))):
            with self.assertRaises(CommandError):
                await self.user_inserter.add_user("javier", "/home/javier", "/bin/bash", "javier")
