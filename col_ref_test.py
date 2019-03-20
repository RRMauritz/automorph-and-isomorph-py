import time
from isomorph import count_isomorphisms
from graph_io import *
from fast_col_ref import color_refinement
import sys

# Use color_refinement on one graph and print the .dot file
with open('./examplegraph.gr') as f:
    G = load_graph(f)

print("Automorphisms found: ", count_isomorphisms(G, G))

# start = time.time()
# for i in range(100):
#     count_isomorphisms(G,G)
# print("Finished for loop in: ", time.time()-start)
# print(count_isomorphisms(G,G))
#
for v in G.vertices:
    v.colornum = v.color

with open('colored.dot', 'w') as f:
     write_dot(G, f)


