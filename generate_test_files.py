import networkx as nx
from src.graph_parser import graph_to_file, file_to_graph
from src.formula import generate_formula_file


def generate_test_graph_files():
    '''Generates test files for the formula generation.'''

    TEST_INPUT_DIR = "test_files/input"

    # 1: paths of length 2, 3, 4, 5, 10
    for length in [2, 3, 4, 5, 10]:
        G = nx.path_graph(length)
        input_file_path = f"{TEST_INPUT_DIR}/path_{length}.txt"
        graph_to_file(G, input_file_path)


    # 2: cycles of length 3, 5, 10
    for length in [3, 5, 10]:
        G = nx.cycle_graph(length)
        input_file_path = f"{TEST_INPUT_DIR}/cycle_{length}.txt"
        graph_to_file(G, input_file_path)

        
    # 3: 5-dimensional hypercube
    G = nx.hypercube_graph(5)
    G = nx.convert_node_labels_to_integers(G)
    input_file_path = f"{TEST_INPUT_DIR}/hypercube_5.txt"
    graph_to_file(G, input_file_path)


    # 4: random trees with 4, 6, 8 nodes
    for num_nodes in [4, 6, 8]:
        G = nx.random_labeled_tree(num_nodes)
        input_file_path = f"{TEST_INPUT_DIR}/random_tree_{num_nodes}.txt"
        graph_to_file(G, input_file_path)


    # 5: random graphs d-regular graphs
    for num_nodes, degree in [(4, 3), (6, 3), (10, 2), (15, 2)]:
        G = nx.random_regular_graph(degree, num_nodes)
        input_file_path = f"{TEST_INPUT_DIR}/random_regular_{num_nodes}_{degree}.txt"
        graph_to_file(G, input_file_path)


    # 6: incidence graph of projective plane of order 3 (https://houseofgraphs.org/graphs/44089)
    adj_list = {
        1: [2, 3, 4, 5],
        2: [1, 15, 16, 17],
        3: [1, 18, 21, 22],
        4: [1, 20, 23, 24],
        5: [1, 19, 25, 26],
        6: [15, 18, 19, 20],
        7: [15, 22, 23, 25],
        8: [15, 21, 24, 26],
        9: [17, 18, 23, 26],
        10: [16, 18, 24, 25],
        11: [16, 19, 21, 23],
        12: [16, 20, 22, 26],
        13: [17, 20, 21, 25],
        14: [17, 19, 22, 24],
        15: [2, 6, 7, 8],
        16: [2, 10, 11, 12],
        17: [2, 9, 13, 14],
        18: [3, 6, 9, 10],
        19: [5, 6, 11, 14],
        20: [4, 6, 12, 13],
        21: [3, 8, 11, 13],
        22: [3, 7, 12, 14],
        23: [4, 7, 9, 11],
        24: [4, 8, 10, 14],
        25: [5, 7, 10, 13],
        26: [5, 8, 9, 12]
    }
    G = nx.Graph()
    for node, neighbors in adj_list.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node - 1, neighbor - 1)  # Convert to 0-based indexing
    input_file_path = f"{TEST_INPUT_DIR}/projective_plane_3.txt"
    graph_to_file(G, input_file_path)



def generate_dimacs_formulas():
    '''Generates test files for the formula generation.'''
    TEST_INPUT_DIR = "test_files/input"
    TEST_OUTPUT_DIR_SAT = "test_files/dimacs_formulas/sat"
    TEST_OUTPUT_DIR_UNSAT = "test_files/dimacs_formulas/unsat"

    # span is the minimum maximum label (starting from 0), so the minimum number of labels is span + 1, and the maximum unsatisfiable k is span

    # 1: paths
    # paths have span = 2 for P_2, span = 3 for P_3, and P_4, span = 4 for P_n, n >= 5
    for length in [2, 3, 4, 5, 10]:
        input_file_path = f"{TEST_INPUT_DIR}/path_{length}.txt"
        G = file_to_graph(input_file_path)
        if length == 2:
            span = 2
        elif length in [3, 4]:
            span = 3
        else:
            span = 4
        k_sat = span + 1  # k = span + 1 is satisfiable
        k_unsat = span
        output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/path_{length}_{k_sat}.dimacs"
        output_file_path_unsat = f"{TEST_OUTPUT_DIR_UNSAT}/path_{length}_{k_unsat}.dimacs"
        generate_formula_file(G, k_sat, output_file_path_sat)
        generate_formula_file(G, k_unsat, output_file_path_unsat)

    # 2: cycles
    # cycles have span = 4 for all lengths
    for length in [3, 5, 10]:
        input_file_path = f"{TEST_INPUT_DIR}/cycle_{length}.txt"
        G = file_to_graph(input_file_path)
        span = 4
        k_sat = span + 1
        k_unsat = span
        output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/cycle_{length}_{k_sat}.dimacs"
        output_file_path_unsat = f"{TEST_OUTPUT_DIR_UNSAT}/cycle_{length}_{k_unsat}.dimacs"
        generate_formula_file(G, k_sat, output_file_path_sat)
        generate_formula_file(G, k_unsat, output_file_path_unsat)


    # 3: 5-dimensional hypercube
    # the n-dimensional hypercube has  n+3 <= span <= 2n+1 for all n >= 5
    input_file_path = f"{TEST_INPUT_DIR}/hypercube_5.txt"
    G = file_to_graph(input_file_path)
    k_sat = 2 * 5 + 1 + 1
    k_unsat = 5 + 3
    output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/hypercube_5_{k_sat}.dimacs"
    output_file_path_unsat = f"{TEST_OUTPUT_DIR_UNSAT}/hypercube_5_{k_unsat}.dimacs"
    generate_formula_file(G, k_sat, output_file_path_sat)
    generate_formula_file(G, k_unsat, output_file_path_unsat)


    # 4: random trees
    # trees have max_degree + 1 <= span <= max_degree + 2
    for num_nodes in [4, 6, 8]:
        input_file_path = f"{TEST_INPUT_DIR}/random_tree_{num_nodes}.txt"
        G = file_to_graph(input_file_path)
        max_degree = max(dict(G.degree()).values())
        k_sat = max_degree + 2 + 1
        k_unsat = max_degree + 1
        output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/random_tree_{num_nodes}_{k_sat}.dimacs"
        output_file_path_unsat = f"{TEST_OUTPUT_DIR_UNSAT}/random_tree_{num_nodes}_{k_unsat}.dimacs"
        generate_formula_file(G, k_sat, output_file_path_sat)
        generate_formula_file(G, k_unsat, output_file_path_unsat)
    
    # 5: random regular graphs
    # all graphs satisfy span <= max_degree^2 + 2 * max_degree, so d-regular graphs satisfy span <= d^2 + 2d
    for num_nodes, degree in [(4, 3), (6, 3), (10, 2), (15, 2)]:
        input_file_path = f"{TEST_INPUT_DIR}/random_regular_{num_nodes}_{degree}.txt"
        G = file_to_graph(input_file_path)
        k_sat = degree ** 2 + 2 * degree + 1  # k = d^2 + 2d + 1 must be satisfiable
        output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/random_regular_{num_nodes}_{degree}_{k_sat}.dimacs"
        generate_formula_file(G, k_sat, output_file_path_sat)


    # 6: incidence graph of projective plane of order 3
    # incidence graph of projective plane of order n has span = n^2 + n
    input_file_path = f"{TEST_INPUT_DIR}/projective_plane_3.txt"
    G = file_to_graph(input_file_path)
    k_sat = 3 ** 2 + 3 + 1  # k = n^2 + n + 1 is satisfiable
    k_unsat = 3 ** 2 + 3  # k = n^2 + n is unsatisfiable
    output_file_path_sat = f"{TEST_OUTPUT_DIR_SAT}/projective_plane_3_{k_sat}.dimacs"
    output_file_path_unsat = f"{TEST_OUTPUT_DIR_UNSAT}/projective_plane_3_{k_unsat}.dimacs"
    generate_formula_file(G, k_sat, output_file_path_sat)
    generate_formula_file(G, k_unsat, output_file_path_unsat)



if __name__ == "__main__":
    generate_test_graph_files()
    generate_dimacs_formulas()