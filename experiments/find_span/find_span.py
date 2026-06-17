import os
import networkx as nx

# set the project root to the parent directory of the src folder
from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

PATH_TO_VARISAT = "varisat.exe"  # must be in the same directory as this script, or provide the correct path to the Varisat executable


from src.utils.check_satisfiability import check_satisfiability
from src.formula import generate_formula_file


def try_find_span(G, formula_path_prefix, timeout=120, detailed_results_file_path=None):
    '''Attempts to find a span for a graph with the given number of nodes. Returns True if a span is found, False otherwise.'''
    # generate the graph
    max_degree = max(dict(G.degree()).values())
    number_of_nodes = G.number_of_nodes()

    k = min(max_degree ** 2 + max_degree + 1, 2 * number_of_nodes)  # k is a number for which we know that there exists an L(2,1)-labeling with k colors

    if detailed_results_file_path is not None:
        with open(detailed_results_file_path, "a") as f:
            f.write("n, k, Satisfiable, Time taken (seconds), Timeout happened\n")
            f.close()

    while True:
        print(f"Trying to find a span for graph with {number_of_nodes} nodes and k={k}...")
        formula_file_path = f"{formula_path_prefix}_{k}.cnf"
        generate_formula_file(G, k, formula_file_path)
        satisfiable, elapsed_time = check_satisfiability(formula_file_path, PATH_TO_VARISAT, timeout=timeout)
        if detailed_results_file_path is not None:
            with open(detailed_results_file_path, "a") as f:
                f.write(f"{number_of_nodes}, {k}, {satisfiable}, {elapsed_time:.4f}, {satisfiable is None}\n")
                f.close()

        if satisfiable is False:
            did_timeout_happen = False
            return k, did_timeout_happen, elapsed_time
        elif satisfiable is None:
            did_timeout_happen = True
            return k, did_timeout_happen, elapsed_time
        else:
            k -= 1
            if k < 0:
                raise Exception(f"Unexpected result: k became negative while trying to find a span for graph.")
        

def main():
    errors = []
    result_file_path = "experiments/find_span/results_cd.csv"
    with open(result_file_path, "w") as f:
        f.write("Number of nodes, Span, Time taken (seconds), Timeout happened\n")
        f.close()
    
    #for n in [5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 200, 250]:
    for n in [200, 250]:
        G = nx.barabasi_albert_graph(n, 2)
        formula_path_prefix = f"experiments/find_span/formulas/barabasi_albert_{n}"
        detailed_results_file_path = f"experiments/find_span/detailed_results/barabasi_albert_{n}.csv"
        print(f"Trying to find a span for Barabási–Albert graph with {n} nodes...")
        try:
            span, did_timeout_happen, elapsed_time = try_find_span(G, formula_path_prefix, timeout=120, detailed_results_file_path=detailed_results_file_path)
            print(f"Found span: {span}, Time taken: {elapsed_time:.4f} seconds, Timeout happened: {did_timeout_happen}")
            with open(result_file_path, "a") as f:
                f.write(f"{n}, {span}, {elapsed_time:.4f}, {did_timeout_happen}\n")
                f.close()
        except Exception as e:
            print(f"Error occurred while trying to find a span for Barabási–Albert graph with {n} nodes, Error: {e}")
            errors.append((n, str(e)))
        print()
    if errors:
        with open("experiments/find_span/errors.txt", "w") as f:
            f.write("\nErrors:\n")
            for n, error in errors:
                f.write(f"Graph with {n} nodes: Error: {error}\n")
        f.close()
        

if __name__ == "__main__":
    main()