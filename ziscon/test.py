#!/usr/bin/env python3

from cdag import *
graph = Graph()
load_data(graph)
# user = graph.find_one_node('User', naam='LVOS13')
# groups = graph.groups_for_user(user)
# for group in groups:
#     print(f"\tgroup: {group}")
# for role in graph.roles_for_user(user):
#     print(f"\trole: {role}")
#     for nb in role.adjacent('ismemberof'):
#         print(f"\t\t{nb}")