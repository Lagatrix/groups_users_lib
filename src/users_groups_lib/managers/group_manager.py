"""Manage unix groups in shell."""

from shell_executor_lib import CommandManager


class GroupManager:
    """Manage unix groups in shell."""

    def __init__(self, user: str, password: str) -> None:
        """Initialize the GroupManager.

        Args:
            user: The user of the shell who execute command.
            password: The password of the user.
        """
        self._command_manager = CommandManager(user, password)

    async def get_groups(self) -> None:
        """Obtain the groups from the shell in a list.

        Returns:
            A list of the groups in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        pass

    async def get_group(self) -> None:
        """Obtain the groups from the shell in a list.

        Returns:
            A list of the groups in the shell.

        Raises:
            CommandError: If the exit code is not 0.
        """
        pass
