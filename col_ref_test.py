import time
from isomorph import *
from graph_io_adj import *
from permv2 import *
from fast_col_ref import color_refinement
import sys

# Use color_refinement on one graph and print the .dot file
#

# print("Automorphisms found: ", count_isomorphisms(G, G))

# start = time.time()
# for i in range(100):
#     count_isomorphisms(G,G)
# print("Finished for loop in: ", time.time()-start)
# print(count_isomorphisms(G,G))
#

#perm1 = permutation(6, mapping=[0, 1, 2, 3, 5, 4])
#perm2 = permutation(6, mapping=[0, 2, 1, 3, 4, 5])
#f = permutation(6, mapping=[0, 2, 1, 3, 5, 4])
#gen_set = list()
#gen_set.append(perm1)
#gen_set.append(perm2)
#
#print(membership_test(gen_set, f))

with open(sys.argv[1]) as f:
    G = load_graph_list(f)
G = G[int(sys.argv[2])]
U = G + G
color_refinement(U)
with open('colored.dot', 'w') as f:
     write_dot(U, f)
