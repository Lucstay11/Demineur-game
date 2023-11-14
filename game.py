import random
from termcolor import colored


def afficher_grille(grille, decouvert):
    print("    " + "   ".join(str(i + 1) for i in range(len(grille[0]))))
    print(colored("—" * (4 * len(grille[0]) + 3),"green"))

    for i, ligne in enumerate(grille):
        print(chr(ord('A') + i) + colored(" |","blue"),end=" ")

        for j, case in enumerate(ligne):
            if decouvert[i][j]:
                print(case, end=colored(" | ","blue"))
            else:
                print(colored('*',"dark_grey"), end=colored(" | ","blue"))

        print(colored("\n" + "—" * (4 * len(grille[0]) + 3),"green"))


def decouvrir_case(grille, decouvert, ligne, colonne):
    if decouvert[ligne][colonne]:
        print(colored("Cette case a déjà été découverte.","light_red"))
        return

    decouvert[ligne][colonne] = True

    if grille[ligne][colonne] == 'B':
        print(colored("Boom ! Vous avez perdu.","light_red"))
        afficher_grille(grille, decouvert)
        exit()

    if grille[ligne][colonne] == 0:
        decouvrir_cases_voisines(grille, decouvert, ligne, colonne)


def decouvrir_cases_voisines(grille, decouvert, ligne, colonne):
    for i in range(max(0, ligne - 1), min(len(grille), ligne + 2)):
        for j in range(max(0, colonne - 1), min(len(grille[0]), colonne + 2)):
            if not decouvert[i][j]:
                decouvert[i][j] = True
                if grille[i][j] == 0:
                    decouvrir_cases_voisines(grille, decouvert, i, j)


def generer_grille_niveau_facile():
    N = 9
    bombes = lire_emplacements_bombes("bombes.txt")

    grille = [['B' if (i, j) in bombes else 0 for j in range(N)] for i in range(N)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] != 'B':
                for x in range(max(0, i - 1), min(N, i + 2)):
                    for y in range(max(0, j - 1), min(N, j + 2)):
                        if grille[x][y] == 'B':
                            grille[i][j] += 1

    return grille


def generer_grille_niveau_moyen(N):
    bombes = generer_emplacements_bombes(N, N * N // 5)

    grille = [['B' if (i, j) in bombes else 0 for j in range(N)] for i in range(N)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] != 'B':
                for x in range(max(0, i - 1), min(N, i + 2)):
                    for y in range(max(0, j - 1), min(N, j + 2)):
                        if grille[x][y] == 'B':
                            grille[i][j] += 1

    return grille


def generer_grille_niveau_difficile(N):
    bombes = generer_emplacements_bombes(N, N * N // 5)

    grille = [['B' if (i, j) in bombes else 0 for j in range(N)] for i in range(N)]

    for i in range(N):
        for j in range(N):
            if grille[i][j] != 'B':
                for x in range(max(0, i - 1), min(N, i + 2)):
                    for y in range(max(0, j - 1), min(N, j + 2)):
                        if grille[x][y] == 'B':
                            grille[i][j] += 1

    return grille


def lire_emplacements_bombes(fichier):
    with open(fichier, 'r') as file:
        bombes = [tuple(map(int, ligne.strip().split(','))) for ligne in file]
    return bombes


def generer_emplacements_bombes(N, nombre_bombes):
    bombes = set()
    while len(bombes) < nombre_bombes:
        bombes.add((random.randint(0, N - 1), random.randint(0, N - 1)))
    return list(bombes)


def jouer():
    print(colored("--------Bienvenue dans le Démineur------","light_magenta"))
    print(colored("Trouver les cases sans bombes!","dark_grey"))
    print(colored("Ne vous faîte pas exploser!","light_red"))
    niveau = int(input(colored("Veuillez entrer le niveau (0 pour Facile, 1 pour Moyen, 2 pour Difficile) : ","white")))

    if niveau == 0:
        grille = generer_grille_niveau_facile()
    elif niveau == 1:
        N = int(input("Veuillez entrer la taille de la grille : "))
        grille = generer_grille_niveau_moyen(N)
    elif niveau == 2:
        N = int(input("Veuillez entrer la taille de la grille : "))
        grille = generer_grille_niveau_difficile(N)
    else:
        print("Niveau invalide.")
        return

    decouvert = [[False] * len(grille[0]) for _ in range(len(grille))]

    while True:
        afficher_grille(grille, decouvert)
        if niveau==0:
           print(colored("Case découvert: ","light_green")+str(sum(row.count(True) for row in decouvert))+"/71")
        else:
            print(colored("Case découvert: ", "light_green") + str(sum(row.count(True) for row in decouvert)) + "/" + str(len(decouvert) * len(decouvert)-len(decouvert) * len(decouvert)//5))
        ligne = input("Veuillez entrer la lettre d’une ligne : ").upper()
        colonne = int(input("Veuillez entrer le numéro d’une colonne : ")) - 1

        ligne_index = ord(ligne) - ord('A')

        if not (0 <= ligne_index < len(grille) and 0 <= colonne < len(grille[0])):
            print(colored("Coordonnées invalides. Veuillez entrer des coordonnées valides.","red"))
            continue

        decouvrir_case(grille, decouvert, ligne_index, colonne)

        if toutes_cases_decouvertes(decouvert, grille):
            print(colored("Félicitations ! Vous avez gagné.","green"))
            afficher_grille(grille, decouvert)
            break

def toutes_cases_decouvertes(decouvert, grille):
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if not decouvert[i][j] and grille[i][j] != 'B':
                return False
    return True


if __name__ == "__main__":
    jouer()
