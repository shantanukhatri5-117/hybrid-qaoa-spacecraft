import itertools
import networkx as nx
import csv
import time

def maxcut_bruteforce(G):
    best_cut = 0
    best_partition = None
    nodes = list(G.nodes)

    for assignment in itertools.product([0, 1], repeat=len(nodes)):
        cut_value = 0
        for u, v in G.edges():
            if assignment[nodes.index(u)] != assignment[nodes.index(v)]:
                cut_value += G[u][v].get("weight", 1)
        if cut_value > best_cut:
            best_cut = cut_value
            best_partition = assignment

    return best_cut, best_partition


N = 8
G = nx.complete_graph(N)

best_cut, _ = maxcut_bruteforce(G)

with open("results/qaoa_results.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        time.strftime("%Y-%m-%d %H:%M:%S"),
        "classical_maxcut",
        N,
        best_cut
    ])

print(f"Classical Max-Cut (N={N}):", best_cut)
