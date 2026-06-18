'''Console program to generate formulas in dimacs format for the graph coloring problem.
The program reads a graph from a file, generates the formulas for the graph coloring problem, and writes the formulas to an output file in dimacs format.

Usage:
    python main.py -i input_graph.txt -k 3 -o output_formulas.cnf 
Arguments:
    -i, --input-file: Path to the input graph file.
    -k, -n, --num-colors: Number of colors.
    -o, --output-file: Path to the output DIMACS file. Default is 'formulas.cnf'.
    -v, --verify: Optional flag to verify the generated formulas using a SAT solver.
    -t, --solver-timeout: Optional timeout in seconds for the SAT solver verification step. Default is 60 seconds.
    -p, --proof_output: Optional path to the proof output file. If provided, the proof will be written to this file.
The input graph file should be in the following format:

4 4
1 2
2 3
3 4

Where the first line contains two integers representing the number of nodesin the graph (repeated twice), and each subsequent line contains two integers representing an edge between two nodes.
'''

import os
import sys


PATH_TO_VARISAT = 'varisat.exe' # Update this path to point to your Varisat executable or ensure that Varisat is in your system's PATH.


# for PyInstaller compatibility
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

PATH_TO_VARISAT = resource_path("varisat.exe")


def main():
    import argparse
    import networkx as nx
    from src.graph_parser import file_to_graph
    from src.formula import generate_formula_file

    parser = argparse.ArgumentParser(
        description='Generate formulas in DIMACS format for graph coloring.'
    )

    parser.add_argument(
        '-i', '--input-file',
        type=str,
        required=True,
        help='Path to the input graph file.'
    )

    parser.add_argument(
        '-o', '--output-file',
        type=str,
        default='formulas.cnf',
        help='Output DIMACS file.'
    )

    parser.add_argument(
        '-k', '-n', '--num-colors',
        type=int,
        required=True,
        help='Number of colors.'
    )

    parser.add_argument(
        '-v', '--verify',
        action='store_true',
        help='Verify the generated formulas using a SAT solver.'
    )
    parser.add_argument(
        '-t', '--solver-timeout',
        type=int,
        default=60,
        help='Timeout in seconds for the SAT solver verification step.'
    )
    parser.add_argument(
        '-p', '--proof_output',
        type=str,
        default=None,
        help='Optional path to the proof output file. If provided, the proof will be written to this file.'
    )

    try:
        args = parser.parse_args()

        G = file_to_graph(args.input_file)
        generate_formula_file(G, args.num_colors, args.output_file)
        print(f"Formulas generated and written to {args.output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if args.verify:
        from src.utils.check_satisfiability import check_satisfiability
        try:
            is_satisfiable = check_satisfiability(args.output_file, PATH_TO_VARISAT, output_file=args.proof_output, timeout=args.solver_timeout)[0]
        except Exception as e:
            print(f"Error occurred while verifying the generated formula: {e}")
        if is_satisfiable is True:
            print("The generated formula is satisfiable.")
        elif is_satisfiable is False:
            print("The generated formula is unsatisfiable.")
        else:
            print("Could not determine the satisfiability of the generated formula.")

if __name__ == "__main__":
    main()