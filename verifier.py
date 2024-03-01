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

def parse_output_file(output_file_path):
    with open(output_file_path, 'r') as file:
        file.readline()
        nodes_to_remove = file.readline().strip().split()
    return nodes_to_remove


def dfs(Graph):
    visited = set()
    cycles = []
    for start_node in Graph:
        if start_node in visited:
            continue
        stack = [(start_node, [start_node])]
        while stack:
            node, path = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in Graph.successors(node):  # Use successors for directed edges
                    if neighbor in path[:-1]:  # Check if neighbor is in path excluding the last element
                        cycles.append(path[path.index(neighbor):] + [neighbor])
                    else:
                        stack.append((neighbor, path + [neighbor]))
    return cycles



if __name__ == '__main__':
    input_file_path = "C:/Users/arish/OneDrive/Documents/Algorithms406/AlgoBowl_Python/venv/inputs/input_group774.txt"
    output_file_path = "C:/Users/arish/OneDrive/Documents/Algorithms406/AlgoBowl_Python/venv/outputs/output_group774.txt"
    with open("a.txt", 'r') as file:
        input_str = file.read()
        result = parse_input_to_graph(input_str)
        G = nx.DiGraph()
        for node, neighbors in result.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        nodes_to_remove = parse_output_file(output_file_path)
        #nodes_to_remove =['143', '264', '209', '287', '23', '40', '201', '263', '131', '152', '252', '6', '123', '13', '244', '232', '284', '127', '31', '250', '47', '63', '160', '190', '22', '203', '189', '210', '79', '242', '228', '2', '169', '60', '173', '156', '61', '15', '159', '114', '133', '225', '117', '233', '165', '128', '170', '81', '102', '297', '175', '73', '20', '120', '220', '28', '78', '94', '86', '84', '51', '283', '194', '115', '214', '130', '68', '187', '18', '260', '147', '106', '49', '50', '288', '149', '212', '99', '137', '186', '163', '10', '247', '211', '104', '56', '17', '153', '184', '92', '204', '229', '103', '111', '109', '85', '21', '76', '132', '151', '180', '183', '239', '171', '294', '11', '301', '75', '54', '142', '224', '227', '238', '36', '285', '226', '266', '278', '5', '197', '52', '30', '80', '261', '243', '292', '126', '213', '286', '245', '267', '138', '167', '280', '299', '141', '254', '221', '139', '144', '134', '12', '146', '273', '38', '300', '53', '256', '62', '42', '295', '58', '136', '281', '161', '195', '121', '69', '27', '113', '70', '196', '3', '59', '271', '83', '33', '216', '71', '208', '129', '200', '202', '205', '298', '108', '158', '168', '55', '206', '234', '272', '100', '240', '172', '43', '119', '19', '235', '179', '122', '48', '251', '148', '198', '93', '237', '39', '222', '192', '88', '112', '91', '124', '4', '154', '110', '157', '258', '282', '262', '24', '274', '290', '25', '105']
        G.remove_nodes_from(nodes_to_remove)
        is_dag = dfs(G)
        if not len(is_dag):
            print(f"The resulting graph is a DAG")
        else:
            print("Not a DAG")
