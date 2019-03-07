"""
This is a module for working with directed and undirected multigraphs.
"""
# version: 29-01-2015, Paul Bonsma
# version: 01-02-2017, Pieter Bos, Tariq Bontekoe

from typing import List, Union, Set
import itertools as it
import copy as cp
import heapq as queue


class GraphError(Exception):
    """
    An error that occurs while manipulating a `Graph`
    """

    def __init__(self, message: str):
        """
        Constructor
        :param message: The error message
        :type message: str
        """
        super(GraphError, self).__init__(message)


class Vertex(object):
    """
    `Vertex` objects have a property `graph` pointing to the graph they are part of,
    and an attribute `label` which can be anything: it is not used for any methods,
    except for `__str__`.
    """

    def __init__(self, graph: "Graph", label=None):
        """
        Creates a vertex, part of `graph`, with optional label `label`.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        :param graph: The graph that this `Vertex` is a part of
        :param label: Optional parameter to specify a label for the
        """
        if label is None:
            label = graph._next_label()

        self._graph = graph
        self.label = label
        self.parent = "A"
        self.color = 0
        self._incidence = {}

    def __repr__(self):
        """
        A programmer-friendly representation of the vertex.
        :return: The string to approximate the constructor arguments of the `Vertex'
        """
        return 'Vertex(label={}, #incident={})'.format(self.label,
                                                       len(self._incidence))

    def __str__(self) -> str:
        """
        A user-friendly representation of the vertex, that is, its label.
        :return: The string representation of the label.
        """
        return str(self.label)

    def is_adjacent(self, other: "Vertex") -> bool:
        """
        Returns True iff `self` is adjacent to `other` vertex.
        :param other: The other vertex
        """
        return other in self._incidence

    def _add_incidence(self, edge: "Edge"):
        """
        For internal use only; adds an edge to the incidence map
        :param edge: The edge that is used to add the incidence
        """
        other = edge.other_end(self)

        if other not in self._incidence:
            self._incidence[other] = set()

        self._incidence[other].add(edge)

    @property
    def graph(self) -> "Graph":
        """
        The graph of this vertex
        :return: The graph of this vertex
        """
        return self._graph

    @property
    def incidence(self) -> List["Edge"]:
        """
        Returns the list of edges incident with the vertex.
        :return: The list of edges incident with the vertex
        """
        result = set()

        for edge_set in self._incidence.values():
            result |= edge_set

        return list(result)

    @property
    def neighbours(self) -> List["Vertex"]:
        """
        Returns the list of neighbors of the vertex.
        """
        return list(self._incidence.keys())

    @property
    def degree(self) -> int:
        """
        Returns the degree of the vertex
        """
        return sum(map(len, self._incidence.values()))


class Edge(object):
    """
    Edges have properties `tail` and `head` which point to the end vertices
    (`Vertex` objects). The order of these matters when the graph is directed.
    """

    def __init__(self, tail: Vertex, head: Vertex, weight=None):
        """
        Creates an edge between vertices `tail` and `head`
        :param tail: In case the graph is directed, this is the tail of the arrow.
        :param head: In case the graph is directed, this is the head of the arrow.
        :param weight: Optional weight of the vertex, which can be any type, but usually is a number.
        """
        if tail.graph != head.graph:
            raise GraphError(
                "Can only add edges between vertices of the same graph")

        self._tail = tail
        self._head = head
        self._weight = weight

    def __repr__(self):
        """
        A programmer-friendly representation of the edge.
        :return: The string to approximate the constructor arguments of the `Edge'
        """
        return 'Edge(head={}, tail={}, weight={})'.format(
            self.head.label, self.tail.label, self.weight)

    def __str__(self) -> str:
        """
        A user friendly representation of this edge
        :return: A user friendly representation of this edge
        """
        return '({}, {})'.format(str(self.tail), str(self.head))

    @property
    def tail(self) -> "Vertex":
        """
        In case the graph is directed, this represents the tail of the arrow.
        :return: The tail of this edge
        """
        return self._tail

    @property
    def head(self) -> "Vertex":
        """
        In case the graph is directed, this represents the head of the arrow.
        :return: The head of this edge
        """
        return self._head

    @property
    def weight(self):
        """
        The weight of this edge, which can also just be used as a generic label.
        :return: The weight of this edge
        """
        return self._weight

    def other_end(self, vertex: Vertex) -> Vertex:
        """
        Given one end `vertex` of the edge, this returns
        the other end vertex.
        :param vertex: One end
        :return: The other end
        """
        if self.tail == vertex:
            return self.head
        elif self.head == vertex:
            return self.tail

        raise GraphError(
            'edge.other_end(vertex): vertex must be head or tail of edge')

    def incident(self, vertex: Vertex) -> bool:
        """
        Returns True iff the edge is incident with the
        vertex.
        :param vertex: The vertex
        :return: Whether the vertex is incident with the edge.
        """
        return self.head == vertex or self.tail == vertex


class Graph(object):
    def __init__(self, directed: bool, n: int = 0, simple: bool = False):
        """
        Creates a graph.
        :param directed: Whether the graph should behave as a directed graph.
        :param simple: Whether the graph should be a simple graph, that is, not have multi-edges or loops.
        :param n: Optional, the number of vertices the graph should create immediately
        """
        self._v = list()
        self._e = list()
        self._simple = simple
        self._directed = directed
        self._next_label_value = 0

        for i in range(n):
            self.add_vertex(Vertex(self))

    def __repr__(self):
        """
        A programmer-friendly representation of the Graph.
        :return: The string to approximate the constructor arguments of the `Graph'
        """
        return 'Graph(directed={}, simple={}, #edges={n_edges}, #vertices={n_vertices})'.format(
            self._directed,
            self._simple,
            n_edges=len(self._e),
            n_vertices=len(self._v))

    def __str__(self) -> str:
        """
        A user-friendly representation of this graph
        :return: A textual representation of the vertices and edges of this graph
        """
        return 'V=[' + ", ".join(map(str, self._v)) + ']\nE=[' + ", ".join(
            map(str, self._e)) + ']'

    def _next_label(self) -> int:
        """
        Generates unique labels for vertices within the graph
        :return: A unique label
        """
        result = self._next_label_value
        self._next_label_value += 1
        return result

    @property
    def simple(self) -> bool:
        """
        Whether the graph is a simple graph, that is, it does not have multi-edges or loops.
        :return: Whether the graph is simple
        """
        return self._simple

    @property
    def directed(self) -> bool:
        """
        Whether the graph behaves as a directed graph
        :return: Whether the graph is directed
        """
        return self._directed

    @property
    def vertices(self) -> List["Vertex"]:
        """
        :return: The `set` of vertices of the graph
        """
        return list(self._v)

    @property
    def edges(self) -> List["Edge"]:
        """
        :return: The `set` of edges of the graph
        """
        return list(self._e)

    def __iter__(self):
        """
        :return: Returns an iterator for the vertices of the graph
        """
        return iter(self._v)

    def __len__(self) -> int:
        """
        :return: The number of vertices of the graph
        """
        return len(self._v)

    def add_vertex(self, vertex: "Vertex"):
        """
        Add a vertex to the graph.
        :param vertex: The vertex to be added.
        """
        if vertex.graph != self:
            raise GraphError(
                "A vertex must belong to the graph it is added to")

        self._v.append(vertex)

    def del_vertex(self, vertex: "Vertex"):
        """
        Delete a vertex from the graph.
        :param vertex: The vertex to be removed.
        """

        if vertex in self._v:
            for e in vertex.incidence:
                self.del_edge(e)
            self._v.remove(vertex)

    def add_edge(self, edge: "Edge"):
        """
        Add an edge to the graph. And if necessary also the vertices.
        Includes some checks in case the graph should stay simple.
        :param edge: The edge to be added
        """

        if self._simple:
            if edge.tail == edge.head:
                raise GraphError('No loops allowed in simple graphs')

            if self.is_adjacent(edge.tail, edge.head):
                raise GraphError('No multiedges allowed in simple graphs')

        if edge.tail not in self._v:
            self.add_vertex(edge.tail)
        if edge.head not in self._v:
            self.add_vertex(edge.head)

        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def del_edge(self, edge: "Edge"):
        """
        Remove an edge from the graph.
        :param edge: The edge to be removed
        """

        if edge in self._e:
            edge.head._incidence = {
                k: v
                for k, v in edge.head._incidence.items() if edge not in v
            }
            edge.tail._incidence = {
                k: v
                for k, v in edge.tail._incidence.items() if edge not in v
            }
            self._e.remove(edge)

    def __add__(self, other: "Graph") -> "Graph":
        """
        Make a disjoint union of two graphs.
        :param other: Graph to add to `self'.
        :return: New graph which is a disjoint union of `self' and `other'.
        """

        res = cp.deepcopy(self)
        temp = cp.deepcopy(other)

        alpha = self.__len__()
        for v in temp.vertices:
            v.label += alpha
            v.parent = "B"
            v._graph = res
            res.add_vertex(v)
        for e in temp.edges:
            res.add_edge(e)
        return res

    def create_dsu(self, graphs: 'list'):

        if len(graphs) == 0:
            return self
        else:
            temp = graphs[0]
            graphs.remove(temp)
            self = self + temp
            return self.create_dsu(graphs)

    def split_disjoint(self):
        """"
        Split a graph into sub-graphs based on the parent-label
        :return sub-graphs which formed the original graph
        """
        G1 = Graph(self.directed, 0, self.simple)
        G2 = Graph(self.directed, 0, self.simple)

        temp = cp.deepcopy(self)
        for v in temp.vertices:
            if v.parent == "A":
                v._graph = G1
                G1.add_vertex(v)
            else:
                v._graph = G2
                # v.parent = "A"
                G2.add_vertex(v)

        for e in temp.edges:
            if e.tail.parent == "A":
                G1.add_edge(e)
            else:
                G2.add_edge(e)

        for v in G2.vertices:
            v.parent = "A"
        return G1, G2

    def __iadd__(self, other: Union[Edge, Vertex]) -> "Graph":
        """
        Add either an `Edge` or `Vertex` with the += syntax.
        :param other: The object to be added
        :return: The modified graph
        """
        if isinstance(other, Vertex):
            self.add_vertex(other)

        if isinstance(other, Edge):
            self.add_edge(other)

        return self

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        """
        Tries to find edges between two vertices.
        :param u: One vertex
        :param v: The other vertex
        :return: The set of edges incident with both `u` and `v`
        """
        result = u._incidence.get(v, set())

        if not self._directed:
            result |= v._incidence.get(u, set())

        return set(result)

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        """
        Returns True iff vertices `u` and `v` are adjacent. If the graph is directed, the direction of the edges is
        respected.
        :param u: One vertex
        :param v: The other vertex
        :return: Whether the vertices are adjacent
        """
        return v in u.neighbours and (not self.directed
                                      or any(e.head == v for e in u.incidence))

    def _isCyclicUtil(self, v, visited, parent):

        # Mark current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent
        # for this vertex
        for i in v.neighbours:
            # If an adjacent is not visited,
            # then recur for that adjacent
            if i not in visited:
                if self._isCyclicUtil(i, visited, v) == True:
                    return True

            # If an adjacent is visited and not
            # parent of current vertex, then there
            # is a cycle.
            elif i != parent:
                return True

        return False

    def is_tree(self):
        # Mark all the vertices as not visited
        # and not part of recursion stack
        visited = {}
        # The call to isCyclicUtil serves multiple
        # purposes. It returns true if graph reachable
        # from vertex 0 is cyclcic. It also marks
        # all vertices reachable from 0.
        if self._isCyclicUtil(self.vertices[0], visited, None):
            return False

        # If we find a vertex which is not reachable
        # from 0 (not marked by isCyclicUtil(),
        # then we return false
        for i in self.vertices:
            if visited[i] == False:
                return False

        return True

    @property
    def max_color(self) -> int:
        return max([v.color for v in self.vertices])

    def degree_of_color(self, c) -> int:
        return max([v.degree for v in self.vertices if v.color == c],
                   default=0)


class UnsafeGraph(Graph):
    @property
    def vertices(self) -> List["Vertex"]:
        return self._v

    @property
    def edges(self) -> List["Edge"]:
        return self._e

    def add_vertex(self, vertex: "Vertex"):
        self._v.append(vertex)

    def add_edge(self, edge: "Edge"):
        self._e.append(edge)

        edge.head._add_incidence(edge)
        edge.tail._add_incidence(edge)

    def find_edge(self, u: "Vertex", v: "Vertex") -> Set["Edge"]:
        left = u._incidence.get(v, None)
        right = None

        if not self._directed:
            right = v._incidence.get(u, None)

        if left is None and right is None:
            return set()

        if left is None:
            return right

        if right is None:
            return left

        return left | right

    def is_adjacent(self, u: "Vertex", v: "Vertex") -> bool:
        return v in u._incidence or (not self._directed and u in v._incidence)
