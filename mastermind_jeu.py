from random import randint
import pygame

num_colors = 6
num_cases = 4
lettres = ["A", "B", "C", "D", "E", "F"]

blanc = 0
bleu = 0

matrice_info = [0 for i in range(num_cases)]
secret = [lettres[randint(0, num_colors-1)] for i in range(num_cases)]

def lettres_to_nombres(code):
    tableau = []
    for i in range(len(code)):
        for j in range(len(lettres)):
            if code[i] == lettres[j]:
                tableau.append(j+1)
    return tableau

def nombres_to_lettres(code):
    tableau = []
    for i in range(len(code)):
        tableau.append(lettres[code[i]-1])
    return tableau
                 
def comptage(code):
    tableau = []
    for i in range(1, num_colors+1):
        compte = 0
        for j in range(len(code)):
            if code[j] == i:
                compte += 1
        tableau.append(compte)
    return tableau

def match(code1, code2):
    tableau = [0 for i in range(num_colors)]
    for i in range(len(code1)):
        if code1[i] == code2[i]:
            tableau[code1[i]-1] += 1
    return tableau

def compare(secret, test, match):
    tableau = []
    for i in range(len(test)):
        if secret[i] >= test[i]:
            tableau.append(test[i]-match[i])
        else:
            tableau.append(secret[i]-match[i])
    return tableau
    
def count(tableau):
    compte = 0
    for i in range(len(tableau)):
        compte += tableau[i]
    return compte

while blanc < num_cases:
    blanc = 0
    bleu = 0
    test_input = []
    
    for i in range (num_cases):
        test_input.append(input("type your guess"))
    
    test_nombres = lettres_to_nombres(test_input)
    test_comptage = comptage(test_nombres)

    secret_nombres = lettres_to_nombres(secret)
    secret_comptage = comptage(secret_nombres)
    
    test_match = match(secret_nombres, test_nombres)
    test_compare = compare(secret_comptage, test_comptage, test_match)
    
    blanc = count(test_match)
    bleu = count(test_compare)
    print(blanc, bleu)