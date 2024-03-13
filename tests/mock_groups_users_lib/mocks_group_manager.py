"""Mocks of the groups."""
from groups_users_lib.entities import Group

mock_groups_list = ["javier 1000 javier,juan,pepe", "pepe 1001 pepe"]

mock_group = ["javier 1000 javier,juan,pepe,ros,pep"]

mock_group_tuple = (1000, "javier", ["javier", "juan", "pepe", "ros", "pep"])

mock_group_tuple_list = [(1000, "javier", ["javier", "juan", "pepe"]), (1001, "pepe", ["pepe"])]

mock_groups_entities = [Group(1000, "javier", ["javier", "juan", "pepe"]),
                        Group(1001, "pepe", ["pepe"])]

mock_groups_entity = Group(1000, "javier", ["javier", "juan", "pepe", "ros", "pep"])
