"""Mocks of the users."""
from users_groups_lib import User

mock_command_executor_method = "shell_executor_lib.CommandManager.execute_command"

mock_users_list = ["1000 javier /bin/bash /home/javier 1000", "1001 pepe /bin/bash /home/pepe 1000"]

mock_user = ["1000 javier /bin/bash /home/javier 1000"]

mock_group_name_list = ["javier"]

mock_user_entity = User(1000, "javier", "/bin/bash", "/home/javier", "javier")
