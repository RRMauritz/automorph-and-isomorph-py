from typing import List
from collections import deque
from enum import Enum
from math import inf


class Twin(Enum):
    none = 0
    false = 1
    true = 2


class Edge:
    def __init__(self, head: "int", tail: "int"):
        self.head = head
        self.tail = tail


class Vertex:
    def __init__(self, graph: "Graph", i: "int"):
        self.i = i
        self._graph = graph

    def is_adjacent(self, other: "Vertex") -> bool:
        return self._graph.is_adjacent(self, other)

    @property
    def neighbors(self) -> List["Vertex"]:
        verts = list()
        for i, v in enumerate(self._graph.adj_matrix[self.i]):
            if v:
                verts.append(Vertex(self._graph, i))
        return verts

    @property
    def degree(self) -> int:
        return [1 for x in self._graph.adj_matrix[self.i] if x].count(1)

    @property
    def color(self) -> int:
        return self._graph.colors[self.i]

    def change_color(self, c):
        self._graph.colors[self.i] = c

    def twins(self, other: "Vertex"):
        nb1 = {v.i for v in self.neighbors}
        nb2 = {v.i for v in other.neighbors}

        if self.is_adjacent(other):
            nb1.remove(other.i)
            nb2.remove(self.i)

            if nb1 == nb2:
                return Twin.true
            else:
                return Twin.none
        else:
            if nb1 == nb2:
                return Twin.false
            else:
                return Twin.none

    def __eq__(self, other: "Vertex"):
        return self.i == other.i and self._graph == other._graph


class Graph:
    def __init__(self, n: "int" = 0):

        self.size = n
        self.abs_size = n
        # Init matrix
        self.adj_matrix = [[] for _ in range(self.size)]
        for i in range(self.size):
            self.adj_matrix[i] = [False] * self.size

        self.colors = [0] * self.size
        self.dsu = False
        self.neighbors = [[] for _ in range(self.size)]

    @property
    def vertices(self) -> List["Vertex"]:
        return [Vertex(self, i) for i in range(self.abs_size)]

    @property
    def edges(self) -> List["Edge"]:
        edges = list()
        for i, v in enumerate(self.adj_matrix):
            for j, e in enumerate(v[:i]):
                if e:
                    edges.append(Edge(i, j))

        return edges

    def is_connected(self):
        return len(self.edges) == (self.abs_size * (self.abs_size - 1)) // 2

    def add_edge(self, edge: "Edge"):
        if edge.head >= self.abs_size or edge.tail >= self.abs_size:
            return

        self.adj_matrix[edge.head][edge.tail] = True
        self.adj_matrix[edge.tail][edge.head] = True
        self.neighbors[edge.head].append(edge.tail)
        self.neighbors[edge.tail].append(edge.head)

    def __add__(self, other: "Graph") -> "Graph":
        if self.dsu:
            raise Exception("Graph is already a DSU")

        new = Graph(self.size)
        new.dsu = True
        new.abs_size = new.size + other.size
        new.adj_matrix = self.adj_matrix.copy()
        new.colors = self.colors.copy()
        new.colors.extend(other.colors)
        new.neighbors = self.neighbors.copy()
        new.neighbors.extend([[] for _ in range(other.size)])

        for _ in range(other.size):
            new.adj_matrix.append([False] * new.size)
        for c in new.adj_matrix:
            c.extend([False] * other.size)

        for e in other.edges:
            new.add_edge(Edge(e.head + self.size, e.tail + self.size))

        return new

    def split_disjoint(self):
        if not self.dsu:
            raise Exception("Graph is not a DSU")

        other_size = self.abs_size - self.size
        A = Graph(self.size)
        B = Graph(other_size)

        A.colors = self.colors[:self.size]
        B.colors = self.colors[self.size:]

        A.neighbors = self.neighbors[:self.size]
        B.neighbors = self.neighbors[self.size:]

        for i, c in enumerate(self.adj_matrix[:self.size]):
            A.adj_matrix[i] = c[:self.size]

        for i, c in enumerate(self.adj_matrix[self.size:]):
            B.adj_matrix[i] = c[self.size:]

        return A, B

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        if u.i >= self.size or v.i >= self.size:
            return False

        return self.adj_matrix[u.i][v.i]

    @property
    def max_color(self):
        return max(self.colors)

    def twins(self):
        checked_verts = list()
        passed = list()
        true_twins = list()
        false_twins = list()

        for v in self.vertices:
            passed.append(v)
            for u in [d for d in self.vertices if d not in passed]:
                check = v.twins(u)
                if check == Twin.true:
                    true_twins.append((u, v))
                elif check == Twin.false:
                    false_twins.append((u, v))

        return true_twins, false_twins

    def degree_of_color(self, b):
        for i, c in enumerate(self.colors):
            if c == b:
                return self.vertices[i].degree
        return 0

    # TODO test everything here
    def graph_search(self, s: "Vertex"):
        k = 1
        flag = {v.i: False for v in self.vertices}
        checked = {}
        pred = {v.i: -1 for v in self.vertices}
        label = {}
        d = {v.i: inf for v in self.vertices}

        Q = deque()
        flag[s.i] = True
        d[s.i] = 0
        label[s.i] = k
        Q.append(s)

        while Q:
            v = Q.popleft()
            for w in self.neighbors[v.i]:
                if flag[w] == False:
                    flag[w] = True
                    pred[w] = v.i
                    k += 1
                    label[w] = k
                    d[w] = d[v.i] + 1
                    Q.append(Vertex(self, w))

        return label, pred, d

    @property
    def is_connected(self):
        if self.dsu:
            return False
        label, parent, dist = self.graph_search(self.vertices[0])
        return self.size == max(label.values())

    def is_tree(self):
        return self.is_connected and len(self.edges) == self.size - 1

    def find_center(self):
        root = self.vertices[0]  # take 'random' root
        _, _, d1 = self.graph_search(root)
        v1 = Vertex(self, max(d1, key=d1.get))
        _, parent2, d2 = self.graph_search(v1)
        # parent2 stores all the parents when we
        # go from v1 to all the other vertices
        #print("Parent2", parent2)

        v2 = max(d2, key=d2.get)
        diam = d2[v2]  # the length of the path from v1 to v2
        #print(diam)
        k = 0
        child = v2
        if diam % 2 == 0:
            mid = diam / 2
            while k != mid:
                parent = parent2[child]
                child = parent
                k += 1
            return [self.vertices[child]]
        else:
            mid = ((diam - 1) / 2)
            while k != mid:
                parent = parent2[child]
                child = parent
                k += 1
            return [self.vertices[child], self.vertices[parent2[child]]]

    def induced_subgraph(self, verts: "List"):
        subgraph = Graph(len(verts))
        indices = [k.i for k in verts]

        for i, v in enumerate(indices):
            nb = set(self.neighbors[v]).intersection(indices)
            subgraph.colors[i] = self.colors[v]
            for n in nb:
                subgraph.add_edge(Edge(i, indices.index(n)))

        return subgraph

    def induced_subtree(self, root: "Vertex", parent: "Vertex"):
        from graph_io_adj import write_dot
        verts = list()
        verts.append(root.i)
        s = list()
        s.append(root)
        while s:
            v = s.pop()
            for n in v.neighbors:
                if n == parent:
                    continue
                if not n.i in verts:
                    verts.append(n.i)
                    s.append(n)

        subtree = self.induced_subgraph([Vertex(self, v) for v in verts])
        return subtree


# Test function
if __name__ == "__main__":
    from graph_io_adj import write_dot, load_graph_list
    import sys
    from fast_col_ref import color_refinement
    with open(sys.argv[1]) as f:
        G = load_graph_list(f)[int(sys.argv[2])]

    print(G.is_tree())

    with open("colored.dot", "w") as f:
        write_dot(G, f)
