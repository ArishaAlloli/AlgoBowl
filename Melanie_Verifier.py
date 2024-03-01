def parse_input_to_graph(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        graph = {}
        n = int(lines[0].strip())  # Assuming the first line is the number of nodes
        for line in lines[1:]:
            parts = line.strip().split()
            node = parts[0]
            if node not in graph:
                graph[node] = []
            for neighbor in parts[1:]:
                graph[node].append(neighbor)
    return graph


def remove_nodes_from_graph(graph, nodes_to_remove):
    # Remove specified nodes
    for node in nodes_to_remove:
        if node in graph:
            del graph[node]

    # Remove edges to the removed nodes
    for node, neighbors in graph.items():
        graph[node] = [neighbor for neighbor in neighbors if neighbor not in nodes_to_remove]


def parse_output_file(output_file_path):
    with open(output_file_path, 'r') as file:
        nodes_to_remove = file.readline().strip().split()  # Assuming nodes to remove are listed in the first line
    return nodes_to_remove


def is_dag(graph):
    def visit(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if visit(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    visited, rec_stack = set(), set()
    for node in graph:
        if node not in visited:
            if visit(node, visited, rec_stack):
                return False
    return True


# Main verification function
def verify_algobowl(input_file_path, output_file_path):
    graph = parse_input_to_graph(input_file_path)
    nodes_to_remove = parse_output_file(output_file_path)
    remove_nodes_from_graph(graph, nodes_to_remove)
    return is_dag(graph)


# Assuming 'input.txt' is the path to the input file and 'output.txt' is the path to the output file
input_file_path = 'input.txt'
output_file_path = 'output.txt'
result = verify_algobowl(input_file_path, output_file_path)
print(f"The resulting graph is a DAG: {result}")
