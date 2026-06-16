import networkx as nx
from src.variable_dictionary import variable_dictionary
from src.utils.get_nodes_distance_2 import get_nodes_distance_2


def every_vertex_has_color(var_dict: variable_dictionary) -> list[str]:
    '''Returns a list of formulas in dimacs format that represent the condition that every vertex in the graph has a color from 1 to k.
    Args:
        var_dict (variable_dictionary): The variable dictionary.'''
    
    G = var_dict.G
    formulas = []
    for node in G.nodes():
        variables = var_dict.get_variables_for_node(node)
        formula = ' '.join(str(var) for var in variables) + ' 0'
        formulas.append(formula)
    return formulas


def every_vertex_has_at_most_one_color(var_dict: variable_dictionary) -> list[str]:
    '''Returns a list of formulas in dimacs format that represent the condition that every vertex in the graph has at most one color from 1 to k.
    Args:
        var_dict (variable_dictionary): The variable dictionary.'''
    
    G = var_dict.G
    formulas = []
    for node in G.nodes():
        variables = var_dict.get_variables_for_node(node)
        for i in range(len(variables)):
            for j in range(i+1, len(variables)):
                formula = f"-{variables[i]} -{variables[j]} 0"
                formulas.append(formula)
    return formulas


def colors_of_adjacent_vertices_differ_by_at_least_two(var_dict: variable_dictionary) -> list[str]:
    '''Returns a list of formulas in dimacs format that represent the condition that the colors of adjacent vertices in the graph differ.
    Args:
        var_dict (variable_dictionary): The variable dictionary.'''
    
    G = var_dict.G
    k = var_dict.k
    formulas = []
    for edge in G.edges():
        node1, node2 = edge
        for color in range(k):
            var1 = var_dict.get_variable_number(node1, color)
            var2 = var_dict.get_variable_number(node2, color)  # neighbor must not be the same color
            var3 = var_dict.get_variable_number(node2, (color + 1) % k)  # neighbor must not be color + 1
            var4 = var_dict.get_variable_number(node2, (color - 1) % k)  # neighbor must not be color - 1
            formula1 = f"-{var1} -{var2} 0"
            formula2 = f"-{var1} -{var3} 0"
            formula3 = f"-{var2} -{var4} 0"
            formulas.extend([formula1, formula2, formula3])
    return formulas
        

def colors_of_vertices_at_distance_2_differ(var_dict: variable_dictionary) -> list[str]:
    '''Returns a list of formulas in dimacs format that represent the condition that the colors of vertices at distance 2 in the graph differ.
    Args:
        var_dict (variable_dictionary): The variable dictionary.'''
    
    G = var_dict.G
    k = var_dict.k
    formulas = []
    for node in G.nodes():
        nodes_at_distance_2 = get_nodes_distance_2(G, node)
        for v in nodes_at_distance_2:
            for color in range(k):
                var1 = var_dict.get_variable_number(node, color)
                var2 = var_dict.get_variable_number(v, color)
                formula = f"-{var1} -{var2} 0"
                formulas.append(formula)
    return formulas


def generate_formulas(G: nx.Graph, k: int) -> list[str]:
    '''Generates a list of formulas in dimacs format that represent the conditions for a valid coloring of the graph.
    Args:
        G (nx.Graph): The graph for which to generate the formulas.
        k (int): The number of colors to use for coloring the graph.'''

    var_dict = variable_dictionary(G, k)
    formulas = []
    formulas.extend(every_vertex_has_color(var_dict))
    formulas.extend(every_vertex_has_at_most_one_color(var_dict))
    formulas.extend(colors_of_adjacent_vertices_differ_by_at_least_two(var_dict))
    formulas.extend(colors_of_vertices_at_distance_2_differ(var_dict))
    return formulas


def generate_formula_file(G: nx.Graph, k: int, file_path: str) -> None:
    '''Generates a formula file in dimacs format that represents the conditions for a valid coloring of the graph.
    Args:
        G (nx.Graph): The graph for which to generate the formulas.
        k (int): The number of colors to use for coloring the graph.
        file_path (str): The path to the output file.'''
    
    formulas = generate_formulas(G, k)
    with open(file_path, 'w') as f:
        f.write(f"p cnf {len(G.nodes()) * k} {len(formulas)}\n")
        for formula in formulas:
            f.write(formula + '\n')
