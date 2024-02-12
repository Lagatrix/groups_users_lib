"""Test the user manager."""

import unittest
from unittest import mock

from shell_executor_lib import CommandManager, CommandError

from mock_users_groups_lib import mock_command_executor_method, mock_user_entity, mock_user, mock_users_list, \
    mock_group
from users_groups_lib import UserManager, UserPermissionError, UserNotExistError, UserExistError, \
    User


class MockCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the user manager."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_manager = UserManager(CommandManager("augusto", "augusto"))

    async def test_get_users(self) -> None:
        """Test correctly functioning of command managers when get all users of the system."""
        with mock.patch(mock_command_executor_method, side_effect=(mock_users_list, mock_group, mock_group)):
            self.assertEqual(await self.user_manager.get_users(), [
                User(1000, "javier", "/bin/bash", "/home/javier", "javier"),
                User(1001, "pepe", "/bin/bash", "/home/pepe", "javier")])

    async def test_get_user(self) -> None:
        """Test correctly functioning of command managers when get a user of the system."""
        with mock.patch(mock_command_executor_method, side_effect=(mock_user, mock_group)):
            self.assertEqual(await self.user_manager.get_user("javier"), mock_user_entity)

    async def test_edit_existing_user(self) -> None:
        """Test correctly functioning of command managers when edit user."""
        with mock.patch(mock_command_executor_method, side_effect=(mock_user, [], [], [], [], [])):
            await self.user_manager.edit_user("javier", mock_user_entity, "pass")

    async def test_edit_user_without_sudo(self) -> None:
        """Test error when attempting to edit user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.edit_user("javier", mock_user_entity, "pass")

    async def test_edit_nonexistent_user(self) -> None:
        """Test error when attempting to edit a nonexistent user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "user not exist")):
            with self.assertRaises(UserNotExistError):
                await self.user_manager.edit_user("javier", mock_user_entity, "pass")

    async def test_edit_nonexistent_main_group_in_user(self) -> None:
        """Test error when attempting to put add in nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=([], CommandError(6, "group not exist"))):
            with self.assertRaises(UserNotExistError):
                await self.user_manager.edit_user("javier", mock_user_entity, "pass")

    async def test_put_name_of_existent_user(self) -> None:
        """Test error when attempting to change name of user and put existing name."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "group not exist")):
            with self.assertRaises(UserExistError):
                await self.user_manager.edit_user("javier", mock_user_entity, "pass")

    async def test_delete_user(self) -> None:
        """Test correctly functioning of command managers when delete a user of the system."""
        with mock.patch(mock_command_executor_method, return_value=[]):
            await self.user_manager.delete_user(mock_user_entity)
