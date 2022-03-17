#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

"""from heapq import *
import heapq"""
import pickle
import math

###  distribution de proba sur les letrres
"""
caracteres = [
    " ",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

proba = [
    0.1835,
    0.0640,
    0.0064,
    0.0259,
    0.0260,
    0.1486,
    0.0078,
    0.0083,
    0.0061,
    0.0591,
    0.0023,
    0.0001,
    0.0465,
    0.0245,
    0.0623,
    0.0459,
    0.0256,
    0.0081,
    0.0555,
    0.0697,
    0.0572,
    0.0506,
    0.0100,
    0.0000,
    0.0031,
    0.0021,
    0.0008,
]
"""
caracteres = ["E", "i", "y", "l", "k", ".", "r", "s", "n", "a", " ", "e"]
proba = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 8]


def frequences(tableau_car, proba_car):
    table = {}
    n = len(tableau_car)
    for i in range(n):
        table[tableau_car[i]] = proba_car[i]
    return table


def frequences_depuis_texte(path):
    nb_symboles = 0
    occurences = []
    lettres = []
    with open(path, "r") as file:
        while True:
            c = file.read(1)
            if not c:
                break
            if c != "\n":
                try:
                    lettres.index(c)
                except:
                    lettres.append(c)
                    occurences.append(0)
                index_c = lettres.index(c)
                occurences[index_c] += 1
                nb_symboles += 1

    for i in range(0, len(occurences)):
        occurences[i] = round((occurences[i] / nb_symboles), 4)
    return frequences(lettres, occurences)


###  la classe Arbre


class Arbre:
    def __init__(self, frequence, lettre="", gauche=None, droit=None):
        self.gauche = gauche
        self.droit = droit
        self.lettre = lettre
        self.frequence = frequence

    def estFeuille(self):
        return self.gauche == None and self.droit == None

    def estVide(self):
        return self == None

    def __str__(self):
        return (
            "<"
            + str(self.frequence)
            + "."
            + str(self.lettre)
            + "."
            + str(self.gauche)
            + "."
            + str(self.droit)
            + ">"
        )

    def __lt__(self, other):
        return self.frequence < other.frequence

    def __gt__(self, other):
        return self.frequence > other.frequence

    def __ge__(self, other):
        return self.frequence >= other.frequence

    def __le__(self, other):
        return self.frequence <= other.frequence


# ajoute un élément dans l'arbre, avec invariance
def heappush(liste, arbre):
    if len(liste) == 1 or not liste:
        liste.append(arbre)
        return True
    for k in range(0, len(liste) - 1):
        if (
            liste[k].frequence <= arbre.frequence
            and liste[k + 1].frequence > arbre.frequence
        ):
            liste.insert(k + 1, arbre)
            return True
        elif len(liste) == k + 2:
            liste.append(arbre)
            return True
    return False


# enlève le plus petit élement
def heappop(liste):
    if not liste:
        return None
    return liste.pop(0)


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(f):
    # pour créer la liste de départ
    huffman_list = []
    for i in f:
        noeud = Arbre(f.get(i), i)
        huffman_list.append(noeud)

    # on construit l'arbre
    huffman_list.sort()
    while len(huffman_list) != 1:
        # assemblage des deux arbres en un seul
        gauche = heappop(huffman_list)
        droite = heappop(huffman_list)
        nouveau_noeud = Arbre(
            gauche.frequence + droite.frequence, gauche=gauche, droit=droite
        )
        heappush(huffman_list, nouveau_noeud)
        # heapify(huffman_list)
    return huffman_list


###  Ex.2  construction du code d'Huffamn


def parcours(arbre: Arbre, prefixe, code):
    if not arbre.estFeuille():
        if arbre.gauche:
            parcours(arbre.gauche, prefixe + "0", code)
        if arbre.droit:
            parcours(arbre.droit, prefixe + "1", code)
    else:
        code[arbre.lettre] = prefixe


def code_huffman(arbre):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre, "", code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier


def header_huffman_tree_write(file_out, dico: dict):
    letter_code_max_size = len(max(dico.values(), key=len))
    nb_octet_per_letter = math.ceil(letter_code_max_size / 8)
    nb_letter_in_dico = len(dico)

    longueur_dico = 1 + (1 + 1 + nb_octet_per_letter) * nb_letter_in_dico
    file_out.write(longueur_dico.to_bytes(1, "little"))
    file_out.write(nb_octet_per_letter.to_bytes(1, "little"))

    for key in dico:
        print(key + " " + str(ord(key)))
        file_out.write(ord(key).to_bytes(1, "little"))

        code_padding = (8 * nb_octet_per_letter) - len(dico.get(key))
        file_out.write((code_padding).to_bytes(1, "little"))

        print(int(dico.get(key), 2))
        file_out.write(int(dico.get(key), 2).to_bytes(nb_octet_per_letter, "little"))


def encodage(dico, fichier_entree, fichier_sortie, arbre):
    out_str = ""
    with open(fichier_entree, "r") as file_in:
        with open(fichier_sortie, "wb") as file_out:
            while True:
                c = file_in.read(1)
                if not c:
                    break
                if not dico.get(c):
                    c = " "
                out_c = dico.get(c)
                out_str += out_c

            # On veut savoir combien d'octet on a
            nb_it = int(len(out_str) / 8)

            # On veut savoir combien de bit il nous reste
            stay = len(out_str) % 8
            padding = 8 - stay
            file_out.write(padding.to_bytes(1, "little"))

            header_huffman_tree_write(file_out, dico)

            for i in range(0, nb_it):
                # On récupère notre octet et on converti notre chaine binaire en integer
                # Par exemple, on récupère la chaine 10100001 alors on obtient 161
                buffer = int(out_str[0 + 8 * i : 8 + 8 * i], 2)
                # On écrit notre nombre décimal en octet dans le fichier
                # Par exemple on prend notre nombre 161 alors on va l'écrire sous la forme
                # d'un octet dans le fichier.
                file_out.write(buffer.to_bytes(1, "little"))

            if stay != 0:
                buffer = int(out_str[len(out_str) - stay :], 2)
                file_out.write(buffer.to_bytes(1, "little"))


###  Ex.4  décodage d'un fichier compresse
# Eerie eyeseen


def decodage(arbre, fichierCompresse):
    # à compléter
    decode = decodage(H, "leHorlaEncoded.txt")
    print(decode)


if __name__ == "__main__":
    # exo 1
    # Avec le texte
    # F = frequences_depuis_texte("texte")
    # print(F)

    # F = frequences(caracteres, proba)
    # arbre1 = arbre_huffman(F)
    # print(arbre1[0])

    # exo 2
    # codage = code_huffman(arbre1[0])
    # print(codage)

    # Feyes = frequences_depuis_texte("eyes.txt")
    # Feyes = frequences(caracteres, proba)
    # print(Feyes)
    # eyes_arbre = arbre_huffman(Feyes)
    # for arbre in eyes_arbre:
    #    print(arbre)
    # eyes_codage = code_huffman(eyes_arbre[0])
    # print(eyes_codage)
    # encodage(eyes_codage, "eyes.txt", "out", eyes_arbre)

    Ft = frequences_depuis_texte("leHorla.txt")
    tree = arbre_huffman(Ft)
    codage = code_huffman(tree[0])
    encodage(codage, "leHorla.txt", "leHorla.out", tree)
