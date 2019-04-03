import sys
from graph_adj import *
from typing import List, IO

NUM_COLORS = 12
DEFAULT_COLOR_SCHEME = "paired12"


def read_line(f: IO[str]) -> str:
    line = f.readline()

    while len(line) > 0 and line[0] == '#':
        line = f.readline()

    return line


def read_graph(f: IO[str]) -> Graph:
    while True:
        try:
            line = read_line(f)
            n = int(line)
            graph = Graph(n)
            break
        except ValueError:
            pass

    line = read_line(f)
    edges = []

    try:
        while True:
            comma = line.find(',')
            if ':' in line:
                colon = line.find(':')
                edges.append((int(line[:comma]), int(line[comma + 1:colon]),
                              int(line[colon + 1:])))
            else:
                edges.append((int(line[:comma]), int(line[comma + 1:]), None))
            line = read_line(f)
    except Exception:
        pass

    for edge in edges:
        graph.add_edge(Edge(edge[0], edge[1]))

    if line != '' and line[0] == '-':
        return graph, True
    else:
        return graph, False


def read_graph_list(f: IO[str]) -> List[Graph]:
    graphs = list()

    cont = True
    while cont:
        graph, cont = read_graph(f)
        graphs.append(graph)
    return graphs


def load_graph_list(f: IO[str]) -> List[Graph]:
    return read_graph_list(f)


def write_dot(graph: Graph, f: IO[str]):
    f.write('graph G {\n')

    for v in graph.vertices:
        options = 'penwidth=3,'

        col = v.color
        options += 'color=' + str(col % NUM_COLORS +
                                  1) + ', colorscheme=' + DEFAULT_COLOR_SCHEME

        f.write(str(v.index) + ' [' + options + ']\n')
    f.write('\n')

    for e in graph.edges:
        options = 'penwidth=2'
        print(e.head, e.tail)
        f.write(
            str(e.tail) + ' -- ' + str(e.head) + ' [' + options + ']' + '\n')

    f.write('}')
