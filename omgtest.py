from queue import Queue
from tarjan import tarjan
import networkx as nx
import matplotlib.pyplot as plt
import sys
import shutil
sys.setrecursionlimit(15000000)
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
def dfs(G):
    visited = set()
    cycles = []
    for start_node in G:
        if start_node in visited:
            continue
        stack = [(start_node, [start_node])]
        while stack:
            node, path = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in G.successors(node):  # Use successors for directed edges
                    if neighbor in path[:-1]:  # Check if neighbor is in path excluding the last element
                        cycles.append(path[path.index(neighbor):] + [neighbor])
                    else:
                        stack.append((neighbor, path + [neighbor]))
    return cycles


def topological_sort(G):
    # Calculate in-degrees for each node
    in_degree = {node: 0 for node in G}
    for node in G:
        for neighbor in G[node]:
            in_degree[neighbor] += 1

    # Initialize queue with nodes having in-degree 0
    queue = [node for node in G if in_degree[node] == 0]

    # Initialize sorted list
    sorted_nodes = []

    # Process until the queue is empty
    while queue:
        current_node = queue.pop(0)
        sorted_nodes.append(current_node)

        # Decrease in-degree of neighbors and add to queue if in-degree becomes 0
        for neighbor in G[current_node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes are visited, there is a cycle
    if len(sorted_nodes) != len(G):
        return False, None  # Graph contains cycle
    else:
        return True, sorted_nodes  # Graph is DAG with topological order
def remove_highest_indegree_nodes(in_graph, removed_nodes = []):
    max_in_degree_node, _ = max(G.in_degree(), key=lambda x: x[1], default=(None, None))
    if max_in_degree_node:
        in_graph.remove_node(max_in_degree_node)
        removed_nodes.append(max_in_degree_node)
    if(len(dfs(in_graph)) > 0):
        max_out_degree_node, _ = max(G.out_degree(), key=lambda x: x[1], default=(None, None))
        if max_out_degree_node:
            in_graph.remove_node(max_out_degree_node)
            removed_nodes.append(max_out_degree_node)
        if (len(dfs(in_graph)) > 0):
            #remove_highest_indegree_nodes(in_graph)
            in_deg = [node for node, indegree in G.in_degree() if indegree > 1]
            in_graph.remove_nodes_from(in_deg)
            for i in in_deg:
                removed_nodes.append(i)
            chec_g = dfs(in_graph)
            in_graph_dag = dfs(in_graph)
            return in_graph, removed_nodes
        else:
            chec_g = dfs(in_graph)
            if len(chec_g)>0:
                outdegree = [node for node, indegree in G.out_degree() if indegree > 1]
                chec_g.remove_nodes_from(outdegree)
                for i in outdegree:
                    removed_nodes.append(i)
                chec_g = dfs(chec_g)
                return chec_g,removed_nodes
            else:
                return in_graph, removed_nodes
    return in_graph, removed_nodes
if __name__ == '__main__':
    input_file_path = "C:/Users/arish/OneDrive/Documents/Algorithms406/AlgoBowl_Python/venv/inputs/input_group787.txt"
    output_file_path = "C:/Users/arish/OneDrive/Documents/Algorithms406/AlgoBowl_Python/venv/outputs/output_group787.txt"
    with open(input_file_path, 'r') as file:
        input_str = file.read()
        resulting_graph = parse_input_to_graph(input_str)
        copy_graph = nx.DiGraph()
        for node, neighbors in resulting_graph.items():
            for neighbor in neighbors:
                copy_graph.add_edge(node, neighbor)
        G = nx.DiGraph()
        for node, neighbors in resulting_graph.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        is_dag = dfs(G)
        in_graph, removed_nodes = remove_highest_indegree_nodes(G)
        #copy_graph.remove_nodes_from(removed_nodes)
        is_dag = dfs(in_graph)
        is_dagtop, topological_order = topological_sort(in_graph)
        if is_dagtop:
            print("The graph is a Directed Acyclic Graph.")
            #print("Topological order:", topological_order)
        else:
            print("The graph contains a cycle.")
        if len(is_dag) > 0:
            print("NOt a DAG")
        else:
            #print(removed_nodes)
            #print(len(removed_nodes))
            #print(' '.join(map(str, removed_nodes)))
            with open(output_file_path, 'w') as file:
                num_courses = str(len(removed_nodes))
                file.write(num_courses + '\n')
                file.write(' '.join(map(str, removed_nodes)))
