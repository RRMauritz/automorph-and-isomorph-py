from graph_io import *
import time
from isomorph import *
from color_refinement import *

with open('graphs/bigtrees3.grl') as f:
    G = load_graph(f, read_list=True)

G1 = G[0][0]
G2 = G[0][2]

print(G1.find_center())
print(G2.find_center())
print(tree_isomorphism(G1, G1.find_center(), G2, G2.find_center()))
print(count_isomorphisms(G1, G2, count_isomorphs=False))
with open('graph1.dot', 'w') as f:
    write_dot(G1, f)
with open('graph2.dot', 'w') as f:
    write_dot(G2, f)
