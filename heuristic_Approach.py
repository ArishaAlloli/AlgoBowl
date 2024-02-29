import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
def parse_input_to_graph(input_str):
    lines = input_str.strip().split("\n")
    n = int(lines[0])
    graph = {str(i): [] for i in range(1, n + 1)}
    for i in range(1, len(lines)):
        parts = lines[i].split()
        target_node = str(i)
        for j in range(1, len(parts)):
            prerequisite = parts[j]
            graph[prerequisite].append(target_node)

    return graph


def is_cyclic(graph):
    visited = set()
    rec_stack = set()

    def dfs(node):
        if node not in visited:
            visited.add(node)
            rec_stack.add(node)

            for neighbour in graph.neighbors(node):
                if neighbour not in visited and dfs(neighbour):
                    return True
                elif neighbour in rec_stack:
                    return True

            rec_stack.remove(node)
        return False

    for node in list(graph.nodes):
        if dfs(node):
            return True

    return False

def heuristic_feedback_arc_set(G):
    edges_sorted = sorted(G.edges(), key=lambda edge: G.in_degree(edge[0]) - G.out_degree(edge[0]), reverse=True)
    H = G.copy()
    removed_edges = []
    for edge in edges_sorted:
        H.remove_edge(*edge)
        if not is_cyclic(H):  # If removing the edge does not introduce a cycle
            removed_edges.append(edge)
        else:  # If removing the edge introduces a cycle, add it back
            H.add_edge(*edge)
    return removed_edges

if __name__ == '__main__':
    with open("a.txt", 'r') as file:
        input_str = file.read()
    resulting_graph = parse_input_to_graph(input_str)
    G = nx.DiGraph()
    for node, neighbors in resulting_graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    fas_edges = heuristic_feedback_arc_set(G)
    for edge in fas_edges:
        G.remove_edge(*edge)
    print("Edges to remove to make the graph acyclic:", fas_edges)

