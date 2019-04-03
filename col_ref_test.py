from graph_io import *
import time
from isomorph import *

with open('graphs/bigtrees1.grl') as f:
    G = load_graph(f, read_list=True)

start = time.time()
print("Conclusion by AHU:", AHU(G[0][0], G[0][2]))
count_isomorphisms(G[0][0], G[0][2], count_isomorphs=False)
end = time.time()

print("Elapsed time in seconds:", end - start)

with open('colored.dot', 'w') as f:
    write_dot(G[0][0], f)
