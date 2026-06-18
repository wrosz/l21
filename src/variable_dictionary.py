import networkx as nx

class variable_dictionary:
    def __init__(self, G: nx.Graph, k: int):
        self.G = G
        self.k = k
        self.dict = {}
        for node in G.nodes():
            for color in range(k):
                self.dict[(node, color)] = len(self.dict) + 1
    
    def get_variable_number(self, node: int, color: int) -> int:
        '''Returns the variable number for a given node and color.
        Args:
            node (int): The node for which to get the variable number.
            color (int): The color for which to get the variable number.'''
        return self.dict[(node, color)]
    
    def get_node_color_pair(self, variable_number: int) -> tuple[int, int]:
        '''Returns the node and color corresponding to a given variable number.
        Args:
            variable_number (int): The variable number for which to get the node and color.'''
        for (node, color), var_num in self.dict.items():
            if var_num == variable_number:
                return (node, color)
        raise ValueError(f"Variable number {variable_number} not found in dictionary.")
    
    def get_variables_for_node(self, node: int) -> list[int]:
        '''Returns a list of variable numbers corresponding to a given node for all colors.
        Args:
            node (int): The node for which to get the variable numbers.'''
        return [self.dict[(node, color)] for color in range(self.k)]
