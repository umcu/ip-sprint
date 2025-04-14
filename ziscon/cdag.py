"""CDAG: colored directed acyclic graph"""

from csv import DictReader
from collections import defaultdict
from itertools import chain

"""Actual classes and functions for the DAG"""
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_number = 0
        self.edge_number = 0
    def add_node(self, node):
        self.node_number += 1
        node.nodeid = self.node_number
        self.nodes[node.nodeid] = node
    def add_edge(self, edge):
        self.edge_number += 1
        edge.edgeid = self.edge_number
        self.edges[edge.edgeid] = edge
    def connect(self, nodea, kind, nodeb):
        edge = Edge(nodea, kind, nodeb)
        nodea.add_edge(edge)
        self.add_edge(edge)
    def adjacent(self, node, kind):
        edges = [edge for edge in node.edges if edge.kind == kind]
        return [edge.end for edge in edges]
    def find_nodes(self, kind, **kwarg):
        """
        search nodes of kind `kind` with key == value or key.lower()== value,
        where (key, value) form the first element of `kwarg`
        """
        key = list(kwarg.keys())[0]
        value = list(kwarg.values())[0]
        selection = [node for node in self.nodes.values() if node.kind == kind]
        result = [node for node in selection
                  if getattr(node, key) == value or getattr(node, key.lower()) == value]
        for r in result:
            print(r)
        return result
    def find_one_node(self, kind, **kwarg):
        result = self.find_nodes(kind, **kwarg)
        if len(result) == 0:
            print(f"No {kind} found with {kwarg}")
            return
        elif len(result) == 1:
            return result[0]
        else:
            print(f"Multiple {kind}s found with {kwarg}")
            return
    def ancestors_of_group(self, group, visited=None, distance=1):
        if visited is None:
            visited = defaultdict(int)
        result = []
        for parent in self.adjacent(group, 'ischild'):
            if visited[parent.nodeid]: continue
            visited[parent.nodeid] = 1
            parent._distance = distance
            result.append(parent)
            result.extend(self.ancestors_of_group(parent, visited, distance+1))
        return result

    def groups_for_user(self, user):
        return self.adjacent(user, 'ismember')

    def roles_for_user(self, user):
        return self.adjacent(user, 'hasrole')

    def effective_groups_for_user(self, user):
        parents = self.groups_for_user(user)
        all_groups = list(chain.from_iterable(self.ancestors_of_group(g) for g in parents))
        for p in parents:
            p._distance = 0
            all_groups.append(p)
        all_groups.sort(key=lambda g: g._distance)
        return all_groups
class Node:
    def __init__(self, **kwarg):
        self.kind = 'Node'
        self.edges = []
        self.nodeid = 0
        for key, value in kwarg.items():
            setattr(self, key, value)
    def __str__(self):
        return f"Node {self.nodeid}"
    def add_edge(self, edge):
        self.edges.append(edge)

class User(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'User'
    def __str__(self):
        return f"{self.naam} {self.omschr}"

class Role(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Role'
    def __str__(self):
        return f"{self.naam} {self.omschr}"

class Group(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Group'
    def __str__(self):
        return f"{self.code} {self.searchcode} {self.omschr}"

class Right(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Right'
    def __str__(self):
        return f"{self.settingid} {self.segmentclassid} {self.segmentid}"

class Edge:
    def __init__(self, begin: Node, kind: str, end: Node):
        self.edgeid = 0
        self.kind = kind
        self.begin = begin
        self.end = end
    def __str__(self):
        return f"{self.begin} {self.kind} {self.end}"

"""Data handling"""
def read_table(filename, cast=True):
    with open(filename) as csvfile:
        reader = DictReader(csvfile, delimiter=',')
        result = []
        if cast:
            for k, row in enumerate(reader):
                # strip() is necessary because some cells have leading or trailing whitespace
                result.append({key.lower(): value.strip() for key, value in row.items()})
        else:
            for k, row in enumerate(reader):
                result.append({key: value.strip() for key, value in row.items()})
    return result

def load_data(graph):
    """
    Future version: load the following tables from the database
    - tables ziscon_groepen, ziscon_groepusr, ziscon_groeplnk, ziscon_user
    - tables config_workcontext, config_wcsegments
    - join config_workcontext and config_wcsegments on wc.id = wcs.configuredworkcontextid

    For now: use CSV exports (raw for ziscon, pre-joined for config)
    """
    error_log = open('error.log', 'w')
    user_index, role_index = {}, {}
    for elt in read_table('ziscon_user.csv'):
        if elt['inloggroep'] == '1':
            new_node = Role(**elt)
            role_index[elt['naam']] = new_node
        else:
            new_node = User(**elt)
            user_index[elt['naam']] = new_node
        graph.add_node(new_node)

    group_index = {}
    for elt in read_table('ziscon_groepen.csv'):
        new_group = Group(**elt)
        group_index[elt['code']] = new_group
        graph.add_node(new_group)

    for elt in read_table('ziscon_groeplnk.csv'):
        linkcode, groupcode = elt['linkcode'], elt['groepcode']
        if linkcode.isalnum():
            # most users are alphanumeric, some are numeric \d{8} however
            if linkcode in user_index:
                user = user_index[linkcode]
                if groupcode in group_index:
                    group = group_index[groupcode]
                    graph.connect(user, 'ismember', group)
                else:
                    print(f"user-group: group {groupcode} not in group index, user linkcode={linkcode}")
            elif linkcode in role_index:
                role = role_index[linkcode]
                if groupcode in group_index:
                    group = group_index[groupcode]
                    graph.connect(role, 'ismember', group)
                else:
                    print(f"user-group: group {groupcode} not in group index, role={linkcode}")
            else:
                print(f"user-group: user {linkcode} not in user or role index, group={groupcode}")
        elif linkcode[0] == '@':
            parentcode = groupcode
            childcode = linkcode[2:]
            if parentcode in group_index:
                parent = group_index[parentcode]
                if childcode in group_index:
                    child = group_index[childcode]
                    graph.connect(child, 'ischild', parent)
                else:
                    print(f"group-group: child {childcode} not in group index, parent={parentcode}")
            else:
                print(f"group-group: parent {parentcode} not in group index, child={childcode}")

    for elt in read_table('ziscon_groepusr.csv'):
        grpusrcode, usercode = elt['grpusrcode'], elt['usercode']
        if usercode in user_index:
            user = user_index[usercode]
            if grpusrcode == 'CHIPSOFT': continue
            if grpusrcode in role_index:
                role = role_index[grpusrcode]
                graph.connect(user, 'hasrole', role)
            else:
                print(f"user-role: role {grpusrcode} not in role index, user={user}")
        else:  # mostly Chipsoft-related users
            pass

    for k, elt in enumerate(read_table('workcontext.csv')):
        new_right = Right(**elt)
        graph.add_node(new_right)
        ownerid = elt['ownerid']
        if ownerid in group_index:
            group = group_index[ownerid]
            graph.connect(group, 'hasright', new_right)
        else:
            print(f"group-workcontext: group {ownerid} not in group index, record={k}", file=error_log)
