"""Test the user manager."""

import unittest
from unittest import mock

from shell_executor_lib import CommandError

from mock_users_groups_lib import mock_users_list, mock_group_name_list, mock_command_executor_method
from users_groups_lib import UserManager, User, UserPermissionError, UserExistError, GroupNotExistError, UserInUseError
from users_groups_lib.errors import UserNotExistError


class MockCommandManager(unittest.IsolatedAsyncioTestCase):
    """Test the user manager."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_manager = UserManager("augusto", "augusto")

    async def test_get_users(self) -> None:
        """Test correctly functioning of command manager when get users."""
        with mock.patch('shell_executor_lib.CommandManager.execute_command',
                        side_effect=(mock_users_list, mock_group_name_list, mock_group_name_list)):
            self.assertEqual(await self.user_manager.get_users(), [
                User(1000, "javier", "/bin/bash", "/home/javier", "javier"),
                User(1001, "pepe", "/bin/bash", "/home/pepe", "javier")])

    async def test_add_user(self) -> None:
        """Test correctly functioning of command manager when add user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier")

    async def test_add_user_with_group(self) -> None:
        """Test correctly functioning of command manager when add user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier",
                                             "dev")

    async def test_add_user_without_sudo(self) -> None:
        """Test error when attempting to add user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier")

        with mock.patch(mock_command_executor_method, side_effect=([], CommandError(1, "No sudo"))):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier")

    async def test_add_existing_user(self) -> None:
        """Test error when attempting to add an existing user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "User exist")):
            with self.assertRaises(UserExistError):
                await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier")

    async def test_add_user_on_nonexistent_group(self) -> None:
        """Test error when attempting to add a user into nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=(CommandError(6, "Group not exist"))):
            with self.assertRaises(GroupNotExistError):
                await self.user_manager.add_user("javier", "/bin/bash", "/home/javier", "javier", "qa")

    async def test_edit_existing_user(self) -> None:
        """Test correctly functioning of command manager when edit user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_edit_user_without_sudo(self) -> None:
        """Test error when attempting to edit user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe")

        with mock.patch(mock_command_executor_method, side_effect=([], CommandError(1, "No sudo"))):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe", password="")

    async def test_edit_nonexistent_user(self) -> None:
        """Test error when attempting to edit a nonexistent user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "user not exist")):
            with self.assertRaises(UserNotExistError):
                await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_edit_nonexistent_main_group_in_user(self) -> None:
        """Test error when attempting to put user in nonexistent group."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "group not exist")):
            with self.assertRaises(GroupNotExistError):
                await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_put_name_of_existent_user(self) -> None:
        """Test error when attempting to change name of user and put existing name."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(9, "group not exist")):
            with self.assertRaises(UserExistError):
                await self.user_manager.edit_user("javier", home="/home/javier", main_group="pepe")

    async def test_delete_existing_user(self) -> None:
        """Test correctly functioning of command manager when delte user."""
        with mock.patch(mock_command_executor_method, side_effect=([], [])):
            await self.user_manager.delete_user("javier")

    async def test_delete_user_without_sudo(self) -> None:
        """Test error when attempting to delete user without sudo."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(1, "No sudo")):
            with self.assertRaises(UserPermissionError):
                await self.user_manager.delete_user("javier")

    async def test_delete_nonexistent_user(self) -> None:
        """Test error when attempting to delete a nonexistent user."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(6, "user not exist")):
            with self.assertRaises(UserNotExistError):
                await self.user_manager.delete_user("javier")

    async def test_delete_user_in_use(self) -> None:
        """Test error when attempting to delete user in use."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(8, "user in use")):
            with self.assertRaises(UserInUseError):
                await self.user_manager.delete_user("javier")

    async def test_delete_user_unknown_exit(self) -> None:
        """Test error when the command return unknown exit."""
        with mock.patch(mock_command_executor_method, side_effect=CommandError(978, "¿?")):
            with self.assertRaises(CommandError):
                await self.user_manager.delete_user("javier")
