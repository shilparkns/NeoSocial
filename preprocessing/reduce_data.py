import csv
import random
from collections import Counter

INPUT = "data/twitter_combined.txt"
EDGES_OUT = "data/follows.csv"
USERS_OUT = "data/users.csv"

# 1. Read a chunk of edges from the big file
edges = []
with open(INPUT, "r") as f:
    for i, line in enumerate(f):
        if i >= 200000:  # read first 200k edges (tweak if needed)
            break
        a, b = line.strip().split()
        edges.append((a, b))

deg = Counter()
for a, b in edges:
    deg[a] += 1
    deg[b] += 1

# 3. Pick top 1000 high-degree nodes
top_nodes = [n for n, _ in deg.most_common(1200)]
top_nodes_set = set(top_nodes)

# 4. Keep only edges where both ends are in top_nodes
sub_edges = [(a, b) for (a, b) in edges if a in top_nodes_set and b in top_nodes_set]

# 5. If too many edges, downsample to 5000
if len(sub_edges) > 10000:
    sub_edges = random.sample(sub_edges, 6000)

# print(f"Nodes: {len(top_nodes_set)}, Edges: {len(sub_edges)}")

# 6. Write follows.csv
with open(EDGES_OUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fromId", "toId"])
    writer.writerows(sub_edges)