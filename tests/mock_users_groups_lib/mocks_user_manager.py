"""Mocks of the users."""
from users_groups_lib import User

mock_users_list = ["1000 javier /bin/bash /home/javier 1000", "1001 pepe /bin/bash /home/pepe 1000"]

mock_user = ["1000 javier /bin/bash /home/javier 1000"]

mock_users_list_entities_without_group_name = [User(1000, "javier", "/bin/bash", "/home/javier", "1000"),
                                               User(1001, "pepe", "/bin/bash", "/home/pepe", "1000")]

mock_users_list_entities = [User(1000, "javier", "/bin/bash", "/home/javier", "javier"),
                            User(1001, "pepe", "/bin/bash", "/home/pepe", "javier")]

mock_user_entity = User(1000, "javier", "/bin/bash", "/home/javier", "javier")

mock_user_entity_group_name = User(1000, "javier", "/bin/bash", "/home/javier", "1000")

mock_group_name_list = ["javier"]
