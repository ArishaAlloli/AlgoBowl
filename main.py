import networkx as nx
def parse_input_to_graph(input_str):
    lines = input_str.strip().split("\n")
    n = int(lines[0])
    edges = []
    for i in range(1, n + 1):
        parts = lines[i].split()
        course = i
        for prereq in parts[1:]:
            edges.append((int(prereq), course))  # Edge from prereq to course

    # Create a directed graph in networkx
    G = nx.DiGraph()
    G.add_edges_from(edges)

    return G

if __name__ == '__main__':
    with open("test_direct_inputs/a.txt", 'r') as file:
        input_str = file.read()
    graph = parse_input_to_graph(input_str)
    print("Done")
