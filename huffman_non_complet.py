#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

"""from heapq import *
import heapq"""

###  distribution de proba sur les letrres

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

# caracteres = ["E", "i", "y", "l", "k", "PT", "r", "s", "n", "a", "sp", "e"]
# proba = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 8]


def frequences(tableau_car, proba_car):
    table = {}
    n = len(tableau_car)
    for i in range(n):
        table[tableau_car[i]] = proba_car[i]
    return table


def frequences_depuis_texte(path):
    nb_symboles = -1
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

    def __eq__(self, other):
        return self.frequence == other.frequence

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


def heapify():
    pass


###  Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
def arbre_huffman(frequences):
    # pour créer la liste de départ
    huffman_list = []
    for i in F:
        noeud = Arbre(F.get(i), i)
        huffman_list.append(noeud)

    # on construit l'arbre
    while len(huffman_list) != 1:
        for a in huffman_list:
            print(a)
        print("--------------")
        # assemblage des deux arbres en un seul
        gauche = heappop(huffman_list)
        droite = heappop(huffman_list)
        nouveau_noeud = Arbre(
            gauche.frequence + droite.frequence, gauche=gauche, droit=droite
        )
        heappush(huffman_list, nouveau_noeud)
        # heapify(huffman_list)
    for a in huffman_list:
        print(a)


###  Ex.2  construction du code d'Huffamn


def parcours(arbre, prefixe, code):
    return
    # à compléter


def code_huffman(arbre):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    parcours(arbre, "", code)
    return code


###  Ex.3  encodage d'un texte contenu dans un fichier


def encodage(dico, fichier):
    # à compléter
    encode = encodage(dico, "leHorla.txt")
    print(encode)


###  Ex.4  décodage d'un fichier compresse


def decodage(arbre, fichierCompresse):
    # à compléter
    decode = decodage(H, "leHorlaEncoded.txt")
    print(decode)


if __name__ == "__main__":
    a = frequences_depuis_texte("t")
    print(a)
    F = frequences(caracteres, proba)
    # print(F)

    # exo 1
    print(F)
    # arbre_huffman(F)
