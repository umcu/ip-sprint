"""CDAG: colored directed acyclic graph"""

from csv import DictReader

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
    def search_nodes(self, kind, **kwarg):
        """
        search nodes of kind `kind` with key == value or key.lower()== value,
        where (key, value) form the first element of `kwarg`
        """
        key = list(kwarg.keys())[0]
        value = list(kwarg.values())[0]
        selection = [node for node in self.nodes.values() if node.kind == kind]
        result = [node for node in selection
                  if getattr(node, key) == value or getattr(node, key.lower()) == value]
        #for r in result:
        #    print(r)
        return result

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

class Group(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'Group'
    def __str__(self):
        return f"{self.code} {self.searchcode} {self.omschr}"

class WorkContext(Node):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.kind = 'WorkContext'

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
            for row in reader:
                # strip() is necessary because some cells have trailing whitespace
                result.append({key.lower(): value.strip() for key, value in row.items()})
        else:
            for row in reader:
                result.append(row)
    return result

def find_single_node(kind, key, value):
    kwarg = {key: value}
    result = graph.search_nodes(kind, **kwarg)
    if len(result) == 0:
        raise ValueError(f"No {kind} found with {key}={value}")
    elif len(result) == 1:
        return result[0]
    else:
        raise ValueError(f"Multiple {kind}s found with {key}={value}")

def load_data():
    """
    Future version: load the following tables from the database
    - tables ziscon_groepen, ziscon_groepusr, ziscon_groeplnk, ziscon_user
    - tables config_workcontext, config_wcsegments
    - join config_workcontext and config_wcsegments on wc.id = wcs.configuredworkcontextid

    For now: use CSV exports (raw for ziscon, pre-joined for config)
    """
    global users, groups, graph, user_index, group_index
    graph = Graph()
    users = read_table('ziscon_user.csv')
    user_index = {}
    for elt in users:
        new_user = User(**elt)
        user_index[elt['naam']] = new_user
        graph.add_node(new_user)
    groups = read_table('ziscon_groepen.csv')
    group_index = {}
    for elt in groups:
        new_group = Group(**elt)
        if elt['code'] == 'ZH1288':
            print(new_group)
        group_index[elt['code']] = new_group
        graph.add_node(new_group)
    group_links = read_table('ziscon_groeplnk.csv')
    for elt in group_links:
        linkcode, groupcode = elt['linkcode'], elt['groepcode']
        if linkcode.isalpha():
            if linkcode in user_index:
                user = user_index[linkcode]
                if groupcode in group_index:
                    group = group_index[groupcode]
                    graph.connect(user, 'ismember', group)
                else:
                    print(f"user-group: group {groupcode} not in group index")
            else:
                print(f"user-group: user {linkcode} not in user index")
        elif linkcode[0] == '@':
            parentcode = groupcode
            childcode = linkcode[2:]
            if parentcode in group_index:
                parent = group_index[parentcode]
                if childcode in group_index:
                    child = group_index[childcode]
                    graph.connect(child, 'ischild', parent)
                else:
                    print(f"group-group: child {childcode} not in group index")
            else:
                print(f"group-group: parent {parentcode} not in group index")

    # worksetting = read_table('config_workcontext.csv')
