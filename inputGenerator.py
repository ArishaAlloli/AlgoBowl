import networkx as nx
import matplotlib.pyplot as plt
from random import sample, randint
import scipy as sp


def generate_graph(vertices=10000, max_edges_per_vertex=5999, total_edges_limit=100000):
    G = nx.DiGraph()
    G.add_nodes_from(range(vertices))
    edges_count = 0
    for node in G.nodes():
        edges = randint(1, min(max_edges_per_vertex, vertices - 1))
        if edges_count + edges <= total_edges_limit:
            targets = sample([n for n in G.nodes() if n != node], edges)
            for target in targets:
                G.add_edge(node, target)
                edges_count += 1
        else:
            break

    return G
G = generate_graph()
num_vertices = G.number_of_nodes()
num_edges = G.number_of_edges()

num_vertices, num_edges

with open("input.txt", 'w') as file:

    file.write(f"{G.number_of_nodes()}\n")
    for node in range(1, G.number_of_nodes() + 1):
        prerequisites = [predecessor + 1 for predecessor in G.predecessors(node - 1)]
        file.write(f"{len(prerequisites)} {' '.join(map(str, prerequisites))}\n")
#plt.figure(figsize=(12, 12))
#pos = nx.spring_layout(G, seed=42)
#nx.draw(G, pos, node_size=5, width=0.5, with_labels=False, arrows=False)
#plt.show()
