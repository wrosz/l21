import networkx as nx

def get_nodes_distance_2(G: nx.Graph, node: int) -> set[int]:
    '''Returns a set of nodes that are at distance 2 from the given node in the graph.
    Args:
        G (nx.Graph): The graph in which to find the nodes at distance 2 from the given node.'''
    neighbors = set(G.neighbors(node))
    nodes_at_distance_2 = set()
    for neighbor in neighbors:
        nodes_at_distance_2.update(G.neighbors(neighbor))
    nodes_at_distance_2.discard(node)
    nodes_at_distance_2.discard(neighbors)
    return nodes_at_distance_2

