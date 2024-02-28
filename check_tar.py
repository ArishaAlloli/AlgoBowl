from queue import Queue
from tarjan import tarjan
import networkx as nx
import matplotlib.pyplot as plt

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
def dfs(graph):
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
                    if neighbor in path:
                        cycles.append(path[path.index(neighbor):] + [neighbor])
                    else:
                        stack.append((neighbor, path + [neighbor]))
    return cycles
def tc(g):
    ret = {}
    for scc in tarjan(g):
        ws = set()
        ews = set()
        for v in scc:
            ws.update(g[v])
        for w in ws:
            ews.add(w)
            ews.update(ret.get(w, ()))
        if len(scc) > 1:
            ews.update(scc)
        ews = tuple(ews)
        for v in scc:
            ret[v] = ews
    return ret

def filter_big_scc(g, edges_to_be_removed):
    G.remove_edges_from(edges_to_be_removed)
    sccs = nx.strongly_connected_components(G)
    return [frozenset(scc) for scc in sccs if len(scc) > 1]
def heuristic_feedback_arc_set(H, edges_to_remove):
    #removed_edges = []
    for edge in edges_to_remove:
        H.remove_edge(*edge)
    is_dag=dfs(H)
    if len(is_dag) > 0:
        edges_with_more_in_than_out = [edge for edge in G.edges() if degree_dict[edge[0]][1] < degree_dict[edge[0]][0]]
        if len(edges_with_more_in_than_out)>0:
            heuristic_feedback_arc_set(H, edges_with_more_in_than_out)
    return H

def remove_cycles(H):
    cycles = dfs(H)
    while cycles:
        for cycle in cycles:

            edge_to_remove = (cycle[0], cycle[1])
            if H.has_edge(*edge_to_remove):
                H.remove_edge(*edge_to_remove)
        cycles = dfs(H)
    return cycles
def greedy_local_heuristic(G, sccs, degree_dict, queue):
    edges_to_be_removed = []
    max_nodes_to_remove =[]
    for scc in sccs:
        subgraph = G.subgraph(scc)
        max_degree_diff = -1
        max_node = None
        for node in subgraph:
            in_degree, out_degree = degree_dict[node][:2]
            degree_diff = abs(in_degree - out_degree)
            if degree_diff > max_degree_diff:
                max_degree_diff = degree_diff
                max_node = node
        if max_node is not None and max_node in subgraph :
                max_nodes_to_remove+=node
            #if degree_dict[max_node][2] == "in":
                edges = [(max_node, o) for o in subgraph.successors(max_node)]
                edges_to_be_removed += edges
            #else:
                edges = [(i, max_node) for i in subgraph.predecessors(max_node)]
                edges_to_be_removed += edges
        edges_to_be_removed += edges
    for node in max_nodes_to_remove:
        if node in G:
            G.remove_node(node)
    is_dag = dfs(G)
    if len(is_dag) > 0:
        G.remove_edges_from(edges_to_be_removed)
    else:
        return G
    is_dag = dfs(G)
    if len(is_dag) > 0:
        edges_to_remove = [edge for edge in G.edges() if degree_dict[edge[0]][1] > degree_dict[edge[0]][0]]
        H = heuristic_feedback_arc_set(G, edges_to_remove)
        cycles = remove_cycles(H)
        if len(cycles) < 0:
            print("Hey Cycles")
        #sub_graphs = filter_big_scc(G, edges_to_be_removed)
        #sccs.extend(sub_graphs)
        #sub_graphs = filter_big_scc(G, edges_to_be_removed)
        #sccs.extend([frozenset(sg.nodes) for sg in sub_graphs if len(sg.nodes) > 1])
        return H
    else:
        return G

if __name__ == '__main__':
    with open("a.txt", 'r') as file:
        input_str = file.read()
    resulting_graph = parse_input_to_graph(input_str)
    sccs = tc(resulting_graph)
    unique_sccs = [frozenset(scc) for scc in set(sccs.values())]
    G = nx.DiGraph()
    for node, neighbors in resulting_graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    degree_dict = {}
    for node in G.nodes():
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        if in_degree > out_degree:
            degree_flag = 'in'
        elif out_degree > in_degree:
            degree_flag = 'out'
        else:
            degree_flag = 'equal'
        degree_dict[node] = (in_degree, out_degree, degree_flag)
    q = Queue()
    graph_test = greedy_local_heuristic(G, unique_sccs, degree_dict, q)
    nodes_with_no_outgoing = []
    for node in graph_test:
        if not graph_test[node]:  # Check if the node has no outgoing edges
            nodes_with_no_outgoing.append(node)
    print(len(nodes_with_no_outgoing))
    print(' '.join(nodes_with_no_outgoing))
    nx.draw(graph_test, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700,font_size=14)
    plt.show()
