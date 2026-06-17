# L21 - Graph Coloring SAT Solver

A Python-based tool for converting graph coloring problems into SAT (Boolean Satisfiability) formulas in DIMACS format, with optional verification using the Varisat SAT solver.

## Overview

This project generates Boolean satisfiability formulas for the graph coloring problem and provides tools to verify satisfiability and extract proofs. It includes experimental frameworks for testing on various graph families from literature and finding optimal lambda parameters.

## Features

- **Formula Generation**: Converts graph coloring constraints into DIMACS CNF format
- **SAT Verification**: Verifies satisfiability using the Varisat SAT solver
- **Proof Extraction**: Extracts and saves formal proofs from SAT solver verification
- **Graph Parsing**: Reads graph specifications from input files
- **Experimental Framework**: Batch processing of test cases and proof verification

## Installation

### Option 1: Download Pre-built Executable

A pre-built executable is available for Windows. Download the latest release and run it directly without requiring Python or dependencies to be installed.

### Option 2: Run from Source

#### Requirements

- Python 3.8+
- NetworkX 3.6.1
- Varisat executable (for verification)

#### Setup

1. Clone or download the project
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the Varisat executable is available:
   - Place `varisat.exe` in the project root directory, or
   - Update the `PATH_TO_VARISAT` variable in `main.py`

## Usage

### Basic Usage

Generate formulas for a graph with k colors:

```bash
python main.py -i input_graph.txt -k 3 -o output_formulas.cnf
```

### Command-Line Arguments

| Argument | Short | Type | Required | Description |
|----------|-------|------|----------|-------------|
| `--input-file` | `-i` | str | Yes | Path to the input graph file |
| `--num-colors` | `-k, -n` | int | Yes | Number of colors for the coloring problem |
| `--output-file` | `-o` | str | No | Output DIMACS file (default: `formulas.cnf`) |
| `--verify` | `-v` | flag | No | Verify formulas using SAT solver |
| `--solver-timeout` | `-t` | int | No | SAT solver timeout in seconds (default: 60) |
| `--proof_output` | `-p` | str | No | Path to save the solver proof |

### Examples

Generate and verify formulas with proof extraction:

```bash
python main.py -i graph.txt -k 4 -o formulas.cnf -v -p proof.txt
```

With custom solver timeout:

```bash
python main.py -i graph.txt -k 5 -o output.cnf -v -t 120 -p proof.txt
```

### Input File Format

Graph input files should follow this format:

```
4 4
1 2
2 3
3 4
```

Where:
- First line: Two integers representing the number of nodes (typically repeated)
- Following lines: Pairs of integers representing edges (node1 node2)

## Project Structure

```
l21/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── l21.spec                         # PyInstaller specification
├── src/
│   ├── formula.py                   # Formula generation for graph coloring
│   ├── graph_parser.py              # Graph input file parsing
│   ├── variable_dictionary.py       # Variable mapping for coloring formulas
│   └── utils/
│       ├── check_satisfiability.py  # SAT solver integration
│       └── get_nodes_distance_2.py  # Graph distance utilities
├── experiments/
│   ├── cases_from_literature/       # Testing on standard graph families
│   │   ├── check_instances_from_files.py
│   │   ├── generate_test_files.py
│   │   ├── verify_proofs.py
│   │   ├── plot_sat_times.py
│   │   ├── proofs/                  # Extracted SAT proofs
│   │   ├── plots/                   # Result visualizations
│   │   ├── test_files/              # Test graph instances
│   │   ├── satisfiability_results.csv
│   │   └── proof_verification_results.csv
│   └── find_lambda/                 # Lambda parameter optimization
│       ├── find_lambda.py
│       ├── plot_results.py
│       ├── results.csv
│       ├── formulas/
│       └── detailed_results/
└── build/                           # PyInstaller build output
```

## Core Components

### `formula.py`
Generates SAT formulas for graph coloring with constraints:
- Every vertex must have at least one color
- Every vertex has at most one color
- Adjacent vertices must have different colors

### `graph_parser.py`
Parses input graph files and constructs NetworkX graph objects.

### `variable_dictionary.py`
Manages variable mappings between graph nodes, colors, and Boolean variables in the CNF formula.

### `check_satisfiability.py`
Interfaces with the Varisat SAT solver to verify satisfiability and extract proofs.

## Experiments

### Cases from Literature

Batch test graph families from academic literature:
- Cycles (3-200 nodes)
- Paths (2-200 nodes)
- Hypercubes (5-7 dimensions)
- Random regular graphs
- Projective planes
- Random trees

Run tests and verify proofs:
```bash
python experiments/cases_from_literature/check_instances_from_files.py
python experiments/cases_from_literature/verify_proofs.py
```

Generate visualizations:
```bash
python experiments/cases_from_literature/plot_sat_times.py
```

### Finding Lambda

Optimize the lambda parameter for formula generation:
```bash
python experiments/find_lambda/find_lambda.py
python experiments/find_lambda/plot_results.py
```

## Dependencies

- **networkx**: Graph manipulation and analysis
- **varisat**: External SAT solver (binary executable)

## Building Custom Executable

If you want to build your own executable from the source code (e.g., after making modifications), use PyInstaller:

```bash
pyinstaller l21.spec
```

The executable will be in the `build/` directory.

## Output

### DIMACS CNF Format

Generated formulas follow the DIMACS CNF standard:
```
c Graph coloring problem
p cnf 12 42
1 2 3 0
-1 -2 0
...
```

### Proof Files

When `--proof_output` is specified, the SAT solver's proof is saved in text format.


## Notes

- The project requires Varisat for satisfiability verification
- Larger graphs may require increased solver timeout values
- Proof extraction is useful for understanding unsatisfiable cores
