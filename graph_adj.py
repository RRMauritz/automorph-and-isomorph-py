from typing import List
from copy import deepcopy

class Edge:
    def __init__(self, head: "int", tail: "int"):
        self.head = head
        self.tail = tail


class Vertex:
    def __init__(self, graph: "Graph", index: "int"):
        self.index = index
        self._graph = graph

    def is_adjacent(self, other: "Vertex") -> bool:
        return G.is_adjacent(self, other)

    @property
    def neighbors(self) -> List["Vertex"]:
        verts = list()
        for i, v in enumerate(self._graph.adj_matrix[self.index]):
            if v:
                verts.append(Vertex(self._graph, i))
        return verts

    @property
    def degree(self) -> int:
        return [1 for x in self._graph.adj_matrix[self.index] if x].count(1)

    @property
    def color(self) -> int:
        return self._graph.colors[self.index]

    def change_color(self, c):
        self._graph.colors[self.index] = c


class Graph:
    def __init__(self, n: "int" = 0):

        self.size = n
        self.abs_size = n
        # Init matrix
        self.adj_matrix = [[]] * self.size
        for i in range(self.size):
            self.adj_matrix[i] = [False] * self.size

        self.colors = [0] * self.size
        self.dsu = False

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

    def __add__(self, other: "Graph") -> "Graph":
        if self.dsu:
            raise Exception("Graph is already a DSU")

        new = Graph(self.size)
        new.dsu = True
        new.abs_size = new.size + other.size
        new.adj_matrix = self.adj_matrix.copy()
        new.colors = self.colors.copy()
        new.colors.extend(other.colors)

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

        for i, c in enumerate(self.adj_matrix[:self.size]):
            A.adj_matrix[i] = c[:self.size]

        for i, c in enumerate(self.adj_matrix[self.size:]):
            B.adj_matrix[i] = c[self.size:]

        return A, B

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        if u.index >= self.size or v.index >= self.size:
            return False

        return self.adj_matrix[u.index][v.index]

    @property
    def max_color(self):
        return max(self.colors)
