"""Mocks of the users."""
from groups_users_lib import User

mock_users_list = ["1000 javier /bin/bash /home/javier 1000", "1001 pepe /bin/bash /home/pepe 1000"]

mock_user = ["1000 javier /bin/bash /home/javier 1000"]

mock_user_tuple = (1000, "javier", "/bin/bash", "/home/javier", 1000)

mock_user_tuples_list = [(1000, "javier", "/bin/bash", "/home/javier", 1000),
                         (1001, "pepe", "/bin/bash", "/home/pepe", 1000)]

mock_users_list_entities = [User(1000, "javier", "/bin/bash", "/home/javier", "javier"),
                            User(1001, "pepe", "/bin/bash", "/home/pepe", "javier")]

mock_user_entity = User(1000, "javier", "/bin/bash", "/home/javier", "javier")
mock_user_entity_with_password = User(1000, "javier", "/bin/bash", "/home/javier", "javier", "pass")

mock_group_name_list = ["javier"]
