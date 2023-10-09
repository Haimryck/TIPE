# TIPE
Sujet: le Mastermind

But:
Trouver la meilleure stratégie par critère:
Coup maximal permissible (maxpart?)
Moyenne de coups minimale (minimax?)

Quelle est la quantité d’information minimale qu’on peut recevoir par coup/combinaison de coups?

Comment agit le nombre de couleurs et la taille de la combinaison sur ce nombre de coups?

En combien de coups peut-on être sûr de trouver la combinaison?
Déjà effectué:
Réalisation du jeu avec un programme python, qui compare le code secret et le code proposé.
Stratégies:
Simple: il propose un code puis il reçoit les résultats de la comparaison avec le code secret. Ensuite il teste tous les codes possibles avec les résultats de la comparaison et garde seulement les codes qui sont potentiellement des codes secrets. Recommence avec la nouvelle liste.
Entropy: même stratégie que simple, mais avec une liste triée selon l’entropie des codes.
Objectifs:

Que all_code soit modifiable par rapport aux nombres de coups
Enjolir le code
Implémenter maxpart
Implémenter minimax
Comprendre la théorie de l’information


