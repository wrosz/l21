# L21 - Graph Coloring SAT Solver

A Python tool for solving the **L(2,1)-labelling** problem on graphs using SAT.

## What is L(2,1)-labelling?

An L(2,1)-labelling of a graph $G$ is an assignment of non-negative integers to its vertices such that adjacent vertices receive labels differing by at least 2, and vertices at distance 2 receive labels differing by at least 1. The **labelling number** λ(G) is the smallest possible value of the largest label used.

This tool encodes the L(2,1)-labelling problem as a Boolean satisfiability (SAT) formula in DIMACS CNF format and verifies it using the Varisat solver. Given a graph and a number of labels k, it determines whether a valid L(2,1)-labelling exists using labels from {0, 1, ..., k}.

## Installation

### Requirements

- Python 3.8+
- NetworkX 3.6.1
- Varisat executable (for verification)

### Setup

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place `varisat.exe` in the project root, or update `PATH_TO_VARISAT` in `main.py`.

Alternatively, download the pre-built Windows executable from the latest release.

## Usage

```bash
python main.py -i input_graph.txt -k 5 -o output.cnf
```


### Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--input-file` | `-i` | Yes | Path to the input graph file |
| `--num-colors` | `-k, -n` | Yes | Number of labels k (labels will be 0..k) |
| `--output-file` | `-o` | No | Output DIMACS file (default: `formulas.cnf`) |
| `--verify` | `-v` | No | Verify using Varisat SAT solver |
| `--solver-timeout` | `-t` | No | Solver timeout in seconds (default: 60) |
| `--proof_output` | `-p` | No | Path to save the solver proof |

### Example

```bash
python main.py -i graph.txt -k 4 -o formulas.cnf -v -p proof.txt
```

```bash
l21.exe -i graph.txt -k 4 -o formulas.cnf -v -p proof.txt
```


### Input Format

```
4 4
1 2
2 3
3 4
```

The first line contains the number of nodes (repeated twice). Each subsequent line is an edge, with nodes numbered from 1.

## Project Structure

```
l21/
├── main.py
├── src/
│   ├── formula.py             # SAT formula generation
│   ├── graph_parser.py        # Input file parsing
│   ├── variable_dictionary.py # Variable mapping
│   └── utils/
│       ├── check_satisfiability.py
│       └── get_nodes_distance_2.py
└── experiments/               # Batch testing and lambda search
```

## Experiments

The `experiments/` directory contains scripts for batch-testing known graph families (cycles, paths, hypercubes, projective planes) against values from the literature, and for searching for λ(G) on arbitrary graphs.