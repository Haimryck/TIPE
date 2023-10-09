# Création arbre version 2
from graphviz import Digraph

def check_guess(secret_code, guess):
    """Vérifie la proposition par rapport au code secret et renvoie les indices corrects."""
    correct_positions = 0
    correct_colors = 0
    
    secret_code_copy = secret_code.copy()
    guess_copy = guess.copy()
    
    # Vérifier d'abord les positions correctes
    for i in range(len(secret_code_copy)):
        if guess_copy[i] == secret_code_copy[i]:
            correct_positions += 1
            guess_copy[i] = None
            secret_code_copy[i] = None
    
    # Vérifier les couleurs correctes à la mauvaise position
    for i in range(len(secret_code_copy)):
        if guess_copy[i] is not None and guess_copy[i] in secret_code_copy:
            correct_colors += 1
            secret_code_copy[secret_code_copy.index(guess_copy[i])] = None
    
    return (correct_positions, correct_colors)

def all_code(colors, positions):
    def generate_combinations(positions, current_combination):
        if positions == 0:
            return [current_combination]
        combinations = []
        for i in range(colors):
            new_combination = current_combination + [C[i]]
            combinations.extend(generate_combinations(positions - 1, new_combination))
        return combinations

    C = list(range(colors))
    return generate_combinations(positions, [])

# Génération de l'arbre minimax
# Création d'une classe noeud
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

# Fonction qui génère l'arbre 
def generate_mastermind_tree(positions, colors):
    L = all_code(colors, positions)
    root = Node([None for _ in range(positions)])

    generate_tree_recursive(root, L.copy(), L, False, 0)
    return root

# Fonction appelée récursivement pour créer les branches
def generate_tree_recursive(node, T, L, joueur, profondeur):
    # Fin de joue ou arrêter pour éviter le crash
    if profondeur == 10 or (len(T) == 1 and T[0] == node.data and not(joueur)):  
        return
    
    # Condition pour savoir quel joueur joue

    if joueur:
        for code in L:
            child = Node(code)
            node.children.append(child)
            new_L = [elem for elem in L if elem != code]

            reponse = check_guess(node.data, code)
            new_T = [elem for elem in T if check_guess(elem, code) == reponse]

            generate_tree_recursive(child, new_T, new_L, not(joueur), profondeur+1)
    else:
        for code in T:
            child = Node(code)
            node.children.append(child)
            
            reponse = check_guess(code, node.data)
            new_L = [elem for elem in L if check_guess(elem, node.data) == reponse]

            generate_tree_recursive(child, T, new_L, not(joueur), profondeur+1)


# Fonction pour générer un graphique à partir de l'arbre
def generate_tree_graph(node, dot=None):
    if dot is None:
        dot = Digraph()
    
    node_id = str(id(node))
    dot.node(node_id, label=str(node.data))
    
    for child in node.children:
        child_id = str(id(child))
        dot.edge(node_id, child_id)
        generate_tree_graph(child, dot)
    
    return dot

if __name__ == "__main__":
    colors = 3
    positions = 4
    mastermind_tree = generate_mastermind_tree(positions, colors)
    
    # Générer le graphique à partir de l'arbre
    dot = generate_tree_graph(mastermind_tree)
    dot.render("arbre({}#{})_bis".format(colors, positions))
