'''Console program to generate formulas in dimacs format for the graph coloring problem.
The program reads a graph from a file, generates the formulas for the graph coloring problem, and writes the formulas to an output file in dimacs format.

Usage:
    python main.py -i input_graph.txt -k 3 -o output_formulas.cnf 
Arguments:
    -i, --input-file: Path to the input graph file.
    -k, -n, --num-colors: Number of colors.
    -o, --output-file: Path to the output DIMACS file. Default is 'formulas.cnf'.
The input graph file should be in the following format:

4 4
1 2
2 3
3 4

Where the first line contains two integers representing the number of nodesin the graph (repeated twice), and each subsequent line contains two integers representing an edge between two nodes.
'''


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

    args = parser.parse_args()

    G = file_to_graph(args.input_file)
    generate_formula_file(G, args.num_colors, args.output_file)