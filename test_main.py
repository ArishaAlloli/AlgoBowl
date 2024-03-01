import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import  sys

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


def remove_nodes_and_verify_dag(graph, nodes_to_remove):
    # Remove specified nodes and their edges
    reduced_graph = {node: edges for node, edges in graph.items() if node not in nodes_to_remove}
    for node, edges in reduced_graph.items():
        reduced_graph[node] = [edge for edge in edges if edge not in nodes_to_remove]

    # Check if the resulting graph is a DAG
    return dfs(reduced_graph)

def dfs(graph):
    visited = set()
    cycles = []

    for start_node in graph:
        if start_node in visited:
            continue
        stack = [(start_node, [start_node])]
        while stack:
            node, path = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph.get(node, []):
                    if neighbor in path:
                        cycles.append(path[path.index(neighbor):] + [neighbor])
                    else:
                        stack.append((neighbor, path + [neighbor]))
    return cycles


def remove_nodes_from_graph(graph, nodes_to_remove):
    # Remove the nodes
    for node in nodes_to_remove:
        if node in graph:
            del graph[node]
    for node, edges in graph.items():
        graph[node] = [edge for edge in edges if edge not in nodes_to_remove]
    return graph


if __name__ == '__main__':
    with open("a.txt", 'r') as file:
        input_str = file.read()
    resulting_graph = parse_input_to_graph(input_str)
    temp_graph = resulting_graph
    has_cycle = dfs(resulting_graph)
    # with open('cycles_output.txt', 'w') as file:
    # for cycle in has_cycle:
    # cycle_str = " -> ".join(map(str, cycle)) + "\n"  # Convert each cycle to a string
    # file.write(cycle_str)
    nodes_in_cycles = [node for cycle in has_cycle for node in cycle]
    node_frequencies = Counter(nodes_in_cycles)
    critical_nodes = [node for node, freq in node_frequencies.items() if freq > 1]
    after_node_removal_graph = remove_nodes_from_graph(resulting_graph, critical_nodes)
    G = nx.DiGraph()
    for node, edges in after_node_removal_graph.items():
        G.add_node(node)
        for edge in edges:
            G.add_edge(node, edge)

    # Draw the graph
    #nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, font_size=14)

    # Show the plot
    #plt.show()
    updated_cycles = dfs(after_node_removal_graph)
    if not updated_cycles:
        nodes_with_no_dependencies = [node for node, edges in after_node_removal_graph.items() if not edges]
        check_dag = remove_nodes_and_verify_dag(temp_graph, nodes_with_no_dependencies)
        if not len(check_dag):
            print(len(nodes_with_no_dependencies))
            print(' '.join(nodes_with_no_dependencies))

    else:
        print("There are still cycles in the graph.")

