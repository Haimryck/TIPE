# Implémentation minimax version 1
import random
from graphviz import Digraph

COLORS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
colors = 3
positions = 2

def generate_code(size, num_colors):
    """Génère un code de la taille donnée avec un nombre de couleurs spécifié."""
    code = []
    for _ in range(size):
        code.append(random.choice(COLORS[:num_colors]))
    return code

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


def play_game(code_size, num_colors, max_attempts):
    """Fonction principale pour jouer au jeu."""
    secret_code = generate_code(code_size, num_colors)
    attempts = 0
    previous_guesses = set()
    
    while attempts < max_attempts:
        print("Tour :", attempts + 1)
        guess = input("Quelle est votre proposition ? ").split()
        
        # Vérification de la validité de la proposition
        if len(guess) != code_size or any(color not in COLORS[:num_colors] for color in guess):
            print("Proposition invalide. Utilisez les lettres de {}.".format(COLORS[:num_colors]))
            continue
        
        # Conversion de l'entrée en liste de caractères
        guess = list(guess)
        
        # Vérification si la proposition a déjà été faite
        if tuple(guess) in previous_guesses:
            print("Vous avez déjà essayé cette combinaison.")
            continue
        
        previous_guesses.add(tuple(guess))
        
        correct_positions, correct_colors = check_guess(secret_code, guess)
        print(secret_code)
        print("Indices corrects :", correct_positions)
        print("Couleurs correctes à la mauvaise position :", correct_colors)
        
        if correct_positions == code_size:
            return "Bien joué ! Vous avez trouvé le code secret."
        
        attempts += 1
    
    return "Dommage, vous avez épuisé toutes vos tentatives. Le code secret était :", secret_code


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
        self.score = None

# Fonction qui génère l'arbre 
def generate_mastermind_tree(positions, colors):
    L = all_code(colors, positions)
    root = Node([None] * positions)

    root.score = generate_tree_recursive(root, L.copy(), L, False, 0, float('-inf'), float('inf'))
    return root

# Fonction appelée récursivement pour créer les branches
def generate_tree_recursive(node, T, L, joueur, coups, alpha, beta):
    # Fin de jeu ou arrêter pour éviter le crash
    if coups == 20 or (len(T) == 1 and T[0] == node.data and not(joueur)):
        return
    
    # Condition pour savoir quel joueur joue
    
    if joueur:
        best_score = float('-inf')
        for code in L:
            child = Node(code)
            node.children.append(child)
            new_L = [elem for elem in L if elem != code]

            reponse = check_guess(node.data, code)
            new_T = [elem for elem in T if check_guess(elem, code) == reponse]
            child.score = generate_tree_recursive(child, new_T, new_L, not(joueur), coups+1, alpha, beta)

            if child.score is None:
                 best_score = max(best_score, coups+1)
            else: best_score = max(best_score, child.score)
            alpha = max(alpha, best_score)
            if beta <= alpha: break
        return best_score
    else:
        best_score = float('inf')
        for code in T:
            child = Node(code)
            node.children.append(child)
            child.score = generate_tree_recursive(child, T, L, not(joueur), coups+1, alpha, beta)

            if child.score is None:
                 best_score = min(best_score, coups+1)
            else: best_score = min(best_score, child.score)
            beta = min(beta, best_score)
            if beta <= alpha: break
        return best_score

# Fonction obsolète pour afficher le graphe dans le shell
def print_tree(node, depth=0):
    if node.data is not None:
        print(" " * depth, node.data)
    for child in node.children:
        print_tree(child, depth + 2)

"""
mastermind_tree = generate_mastermind_tree(positions, colors)
print_tree(mastermind_tree)"""


# Fonction pour générer un graphique à partir de l'arbre
def generate_tree_graph(node, dot=None):
    if dot is None:
        dot = Digraph()
    
    node_id = str(id(node))
    
    label = str(node.data)
    if node.score is not None:
        label += " (Score: {})".format(node.score)
    
    dot.node(node_id, label=label)
    
    for child in node.children:
        child_id = str(id(child))
        dot.edge(node_id, child_id)
        generate_tree_graph(child, dot)
    
    return dot

if __name__ == "__main__":
    mastermind_tree = generate_mastermind_tree(positions, colors)
    
    # Générer le graphique à partir de l'arbre
    dot = generate_tree_graph(mastermind_tree)
    dot.render("minimax_mastermind(3#2)")
