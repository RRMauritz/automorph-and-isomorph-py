from graph_io import *
import time
from isomorph import *
from color_refinement import *

with open('graphs/examplegraph3.grl') as f:
    G = load_graph(f, read_list=True)

G1 = G[0][2]
G2 = G[0][0]


adjacent = [v for v in G1.vertices if v.is_adjacent(G1.find_center()[0])]

tree_count_automorphism(G1, G1.find_center()[0])

with open('graph1.dot', 'w') as f:
    write_dot(G1, f)
with open('graph2.dot', 'w') as f:
    write_dot(G2, f)
