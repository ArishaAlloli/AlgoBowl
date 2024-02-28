import networkx as nx
from random import randint, sample


def generate_connected_graph_with_cycles(vertices=10000, total_edges_limit=100000):
    G = nx.DiGraph()
    G.add_nodes_from(range(vertices))
    for node in range(1, vertices):
        G.add_edge(node - 1, node)
    total_edges_added = vertices - 1
    while total_edges_added < total_edges_limit:
        for node in range(vertices):
            if total_edges_added >= total_edges_limit:
                break
            edges_to_add = min(randint(1, 4), total_edges_limit - total_edges_added)
            potential_targets = [n for n in range(vertices) if n != node]
            targets = sample(potential_targets, edges_to_add)
            for target in targets:
                if not G.has_edge(node, target):
                    G.add_edge(node, target)
                    total_edges_added += 1
                    if total_edges_added >= total_edges_limit:
                        break

    return G
G = generate_connected_graph_with_cycles()

with open("input.txt", 'w') as file:
    file.write(f"{G.number_of_nodes()}\n")
    for node in range(1, G.number_of_nodes() + 1):
        prerequisites = [predecessor + 1 for predecessor in G.predecessors(node - 1)]
        file.write(f"{len(prerequisites)} {' '.join(map(str, prerequisites))}\n")