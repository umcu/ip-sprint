"""CDAG: colored directed acyclic graph"""

import csv, re, sys
from collections import defaultdict, deque
from itertools import chain

csv.field_size_limit(sys.maxsize)

"""Actual classes and functions for the DAG"""
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_number = 0
        self.edge_number = 0
        self.guid_map = {}
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
    def primary_groups(self):
        return [node for node in self.nodes.values()
                if node.kind == 'Group' and node.primary]
    def ancestors_of_group(self, group, visited=None, distance=1):
        if visited is None:
            visited = defaultdict(int)
        result = []
        for parent in group.adjacent('ischildof'):
            if visited[parent.nodeid]: continue
            visited[parent.nodeid] = 1
            parent._distance = distance
            result.append(parent)
            result.extend(self.ancestors_of_group(parent, visited, distance+1))
        return result
    def groups_for_user(self, user):
        return user.adjacent('ismemberof')
    def roles_for_user(self, user):
        return user.adjacent('hasrole')
    def effective_groups_for_user(self, user):
        parents = self.groups_for_user(user)
        all_groups = list(chain.from_iterable(self.ancestors_of_group(g) for g in parents))
        for p in parents:
            p._distance = 0
            all_groups.append(p)
        all_groups.sort(key=lambda g: g._distance)
        return all_groups
class Node:
    nodecount = 0
    def __init__(self, **kwarg):
        self.kind = 'Node'
        self.edges = []
        self.nodecount += 1
        self.nodeid = self.nodecount
        for key, value in kwarg.items():
            setattr(self, key, value)
    def __str__(self):
        return f"Node {self.nodeid}"
    def add_edge(self, edge):
        self.edges.append(edge)
    def adjacent(self, kind):
        edges = [edge for edge in self.edges if edge.kind == kind]
        return [edge.end for edge in edges]

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
        self.primary = True
        self.rights = []
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

"""Traversal"""
def breadth_first_traversal(node: Node):
    """Perform breadth-first traversal (BFS) on the graph.
    The traversal starts from vertex `node`.

    Arguments:
       * node (Item): starting point of traversal
    """
    # create a queue for doing BFS, and lookup tables for visited persons and families
    queue = deque()
    visited_nodes = defaultdict(bool)
    # add start node to the queue
    visited_nodes[node.nodeid] = True
    queue.append(node)
    while queue:
        # de-queue node
        node = queue.popleft()
        yield node
        neighbours = node.adjacent('haschild')
        for neighbour in neighbours:
            nid = neighbour.nodeid
            # ignore neighbour if it was already visited, otherwise add to queue
            if visited_nodes[nid]:
                continue
            else:
                visited_nodes[nid] = True
                queue.append(neighbour)

"""Data handling"""
def read_table(filename, cast=True, sep=','):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=sep)
        try:
            if cast:
                for k, row in enumerate(reader):
                    # strip() is necessary because some cells have leading or trailing whitespace
                    yield {key.lower(): value.strip() for key, value in row.items()}
            else:
                for k, row in enumerate(reader):
                    yield {key: value.strip() for key, value in row.items()}
        except Exception as e:
            print(f"{filename}.{k}: {e}\n{row}")

def load_data(graph):
    """
    Future version: load the tables from the database
    - tables ziscon_groepen, ziscon_groepusr, ziscon_groeplnk, ziscon_user
    - tables config_workcontext, config_wcsegments
    For now: use CSV exports (raw for ziscon, pre-joined for config)
    """
    error_log = open('error.log', 'w')
    user_index, role_index = {}, {}
    for elt in read_table('ziscon_user.csv'):
        if elt['inloggroep'] == 'True':
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
        groupcode, linkcode = elt['groepcode'], elt['linkcode']
        if linkcode.isalnum():
            # most users are alphanumeric, some are numeric \d{8} however
            if linkcode in user_index:
                user = user_index[linkcode]
                if groupcode in group_index:
                    group = group_index[groupcode]
                    graph.connect(user, 'ismemberof', group)
                else:
                    print(f"user-group: group {groupcode} not in group index, user linkcode={linkcode}")
            elif linkcode in role_index:
                role = role_index[linkcode]
                if groupcode in group_index:
                    group = group_index[groupcode]
                    graph.connect(role, 'ismemberof', group)
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
                    child.primary = False
                    graph.connect(child, 'ischildof', parent)
                    graph.connect(parent, 'haschild', child)
                else:
                    print(f"group-group: child {childcode} not in group index, parent={parentcode}")
            else:
                print(f"group-group: parent {parentcode} not in group index, child={childcode}")

    for elt in read_table('ziscon_groepusr.csv'):
        grpusrcode, usercode = elt['grpusrcode'], elt['usercode']
        if usercode in user_index:
            user = user_index[usercode]
            if grpusrcode == 'CHIPSOFT':
                continue
            if grpusrcode in role_index:
                role = role_index[grpusrcode]
                graph.connect(user, 'hasrole', role)
            else:
                print(f"user-role: role {grpusrcode} not in role index, user={user}")
        else:  # mostly Chipsoft-related users
            pass

    wcs_index = defaultdict(list)
    for k, elt in enumerate(read_table('config_wcsegments.csv')):
        if elt['disabled'] == 'True':
            continue
        wcid = elt['configuredworkcontextid']
        wcs_index[wcid].append(elt['segmentid'])

    for k, elt in enumerate(read_table('config_workcontext.csv')):
        if elt['ownertype'] == 'U':
            continue
        wcid, groupcode = elt['id'], elt['ownerid']
        if groupcode in group_index:
            segments = wcs_index[wcid]
            record = {
                'settingid':      elt['settingid'],
                'settingsubid':   elt['settingsubid'],
                'segmentclassid': elt['segmentclassid'],
                'segmentid':      segments,
                'contexttype':    elt['contexttype'],
                'inverted':       elt['inverted']
            }
            group = group_index[groupcode]
            group.rights.append(record)
        else:  # occurs too often, but referential incompleteness is not our problem atm
            pass

    for k, elt in enumerate(read_table('config_instvars.csv')):
        owner = elt['owner']
        if not owner.startswith('@G'):
            continue
        groupcode = owner[2:]
        if groupcode in group_index:
            record = {
                'settingid':      elt['naam'],
                'settingsubid':   elt['speccode'],
                'segmentclassid': parse(elt['value']),
                'segmentid':      [],
                'contexttype':    '',
                'inverted':       ''
            }
            group = group_index[groupcode]
            group.rights.append(record)
        else:  # occurs too often, but referential incompleteness is not our problem atm
            pass

# read reference table guid -> table name
table_name = {}
for elt in read_table('chipsoft_logic_table_guids.csv', sep=';'):
    table_name[elt['classguid']] = elt['classid']

# Unicode dingbats, open and closed circled digits
OD1, CD1 = '\u2780', '\u2776'
OD2, CD2 = '\u2781', '\u2777'
OD3, CD3 = '\u2782', '\u2778'
level1_rx = re.compile(r'"([\u2782\u2778\u2781\u2777\x20\x21\x23-\x7E]+?)"')
level2_rx = re.compile(r'""([\u2782\u2778\x20\x21\x23-\x7E]+?)""')
level3_rx = re.compile(r'""""([\x20\x21\x23-\x7E]+?)""""')
guid_rx = re.compile(r'\{[A-Z0-9-]+?\}')

def resolve_guid(match):
    return table_name.get(match.group(0), '<unknown>')

def tokenize(s):
    if s.startswith('C'):
        s3 = level3_rx.sub('\u2782\g<1>\u2778', s)
        s2 = level2_rx.sub('\u2781\g<1>\u2777', s3)
        s1 = level1_rx.sub('\u2780\g<1>\u2776', s2)
        return s1
    else:
        return s

def parse(s):
    value = s.rstrip('\x01\u00a9')
    if value[0] == 'C':
        if value[1:] == 'T':
            return value.split()
        else:
            tokens = tokenize(guid_rx.sub(resolve_guid, value))
            if tokens.startswith('C\u2780') and tokens.endswith('\u2776'):
                # TODO: handle levels 2 and 3
                return tokens[1:-1].split('\u2776,\u2780')
            else:
                # print(f"{tokens}: begin={tokens[0]} end={tokens[-1]}")
                return value
    elif value[0] == 'L':
      if value[1:] in ('T', 'T'*6):
          return value.split()
      else:
        return value


