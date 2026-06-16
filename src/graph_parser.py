import networkx as nx

def file_to_graph(file_path:str) -> nx.Graph:
    """
    Reads a file and returns a NetworkX graph.
    The first line should contain two integers representing the number of nodes.
    Each subsequent line should contain two integers representing an edge between two nodes.
    
    Args:
        file_path: Path to the input file.
    
    Returns:
        A NetworkX graph constructed from the file's contents.
    """

    tuples = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and split the line into parts
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    u = int(parts[0])
                    v = int(parts[1])
                    tuples.append((u, v))
                except ValueError:
                    raise ValueError(f"Line '{line.strip()}' contains non-integer values.")
            elif len(parts) == 0:
                continue  # Skip empty lines
            else:
                raise ValueError(f"Line '{line.strip()}' does not contain exactly two elements.")

    G = nx.Graph()
    
    n = tuples[0][0] # the first element of the first tuple is the number of nodes
    m = tuples[0][1] # the second element of the first tuple is repeated number of nodes

    if n < 0 or n != m:
        raise ValueError(f"Invalid number of nodes: {n}. The first tuple should contain two equal non-negative integers.")

    G.add_nodes_from(range(n))

    for u, v in tuples[1:]:  # Skip the first tuple as it represents the number of nodes
        if u == v:
            raise ValueError(f"Self-loop detected at node {u}.")
        elif u <= 0 or v <= 0:
            raise ValueError(f"Negative node value detected: ({u}, {v}).")
        elif u > n or v > n:
            raise ValueError(f"Node value out of bounds: ({u}, {v}) for graph with {n} nodes.")
        G.add_edge(u - 1, v - 1)  # Convert to 0-based indexing for NetworkX
    return G


def graph_to_file(graph: nx.Graph, file_path: str) -> None:
    """
    Writes the edges of a NetworkX graph to a file.
    
    Each edge is written on a new line in the format "u v", where u and v are the nodes connected by the edge.
    
    Args:
        graph: A NetworkX graph whose edges are to be written to a file.
        file_path: Path to the output file.
    """
    with open(file_path, 'w') as file:
        n = graph.number_of_nodes()
        file.write(f"{n} {n}\n")  # Write the number of nodes first
        for u, v in graph.edges():
            # Convert back to 1-based indexing for output
            file.write(f"{u + 1} {v + 1}\n")