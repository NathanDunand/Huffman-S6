#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

import math
import os
import sys

# distribution de proba sur les letrres

caracteres = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
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
    "\n",
    "ù",
    "é",
    "è",
    "à",
    "ï",
    "ö",
    "ë",
    "ü",
    "û",
    "ô",
    "ê",
    "â",
    "î",
    "ç",
    ".",
    ";",
    ":",
    ",",
    "'",
    '"',
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "-",
    "!",
    "?",
]

proba = [
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,  # Z
    0.12,  # space
    0.07,
    0.01,
    0.01,
    0.01,
    0.10,
    0.01,
    0.01,
    0.01,
    0.05,
    0.0003,
    0.0003,
    0.05,
    0.02,
    0.06,
    0.05,
    0.02,
    0.0005,
    0.05,
    0.05,
    0.05,
    0.05,
    0.01,
    0.001,
    0.003,
    0.004,
    0.001,  # z
    0.001,
    0.0002,
    0.002,
    0.003,
    0.0028,
    0.0002,
    0.0004,
    0.0001,
    0.0001,
    0.0001,
    0.0003,
    0.0003,
    0.0004,
    0.0004,
    0.0006,
    0.005,
    0.002,
    0.002,
    0.004,
    0.006,
    0.006,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
    0.001,
]


"""
Cette méthode crée un dictionnaire de fréquences en fonction d'un tableau
de caractères et d'un tableau de probabilités

IN:
    tableau_car : tableau de caractères
    proba_car   : tableau de probabilités 
OUT:
    retourne un dictionnaire qui combine les deux tableaux donnés en entrée
"""


def frequences(tableau_car, proba_car):
    table = {}
    n = int((len(tableau_car) + len(proba_car)) / 2)
    for i in range(n):
        table[tableau_car[i]] = proba_car[i]
    return table


"""
Cette méthode crée un dictionnaire de fréquences en fonction d'un text
donné en entré.

IN:
    path    : chemin du fichier à lire
OUT:
    retourne un dictionnaire qui combine les deux tableaux donnés en entrée
"""


def frequences_depuis_texte(path):
    nb_symboles = 0
    occurences = []
    lettres = []
    with open(path, "r") as file:
        while True:
            c = file.read(1)
            if not c:
                break
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


"""
Classe Arbre

Cette classe permet de modéliser un arbre binaire ou chaque feuille de cet
arbre est un objet Arbre.
"""


class Arbre:
    def __init__(self, frequence, lettre="", gauche=None, droit=None):
        self.gauche = gauche
        self.droit = droit
        self.lettre = lettre
        self.frequence = frequence

    def estFeuille(self):
        return self.gauche == None and self.droit == None

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


"""
Ajoute un élément dans l'arbre, avec invariance

IN:
    liste   : liste contenant l'ensemble des arbres 
    arbre   : arbre a ajouté dans la liste
OUT:
    Retourne un booléen qui agit comme un flag, True si
    l'ajout est réussi, sinon False
"""


def heappush(liste, arbre: Arbre):
    if not arbre or liste == None:
        return False
    if len(liste) <= 1:
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


"""
Enlève le plus petit élement de la liste

IN:
    liste   : liste dans laquelle il faut retirer l'élement
OUT:
    Retourne un arbre
"""


def heappop(liste):
    if not liste:
        return None
    return liste.pop(0)


# Ex.1  construction de l'arbre d'Huffamn utilisant la structure de "tas binaire"
"""
Cette fonction construit l'arbre de huffman à partir d'un dictionnaire de fréquence
"""


def arbre_huffman(f):
    if f == None:
        return None
    # pour créer la liste de départ
    huffman_list = []
    for i in f:
        noeud = Arbre(f.get(i), i)
        huffman_list.append(noeud)

    # on construit l'arbre
    huffman_list.sort()
    if len(huffman_list) == 0:
        return None
    while len(huffman_list) > 1:
        # assemblage des deux arbres en un seul
        gauche = heappop(huffman_list)
        droite = heappop(huffman_list)
        nouveau_noeud = Arbre(
            gauche.frequence + droite.frequence, gauche=gauche, droit=droite
        )
        heappush(huffman_list, nouveau_noeud)
    return huffman_list[0]


# Ex.2  construction du code d'Huffamn
"""
Méthode de parcours d'arbre pour déterminer les code des lettres
"""


def parcours(arbre: Arbre, prefixe, code):
    if not arbre.estFeuille():
        if arbre.gauche:
            parcours(arbre.gauche, prefixe + "0", code)
        if arbre.droit:
            parcours(arbre.droit, prefixe + "1", code)
    else:
        if prefixe == "":
            prefixe = "0"
        code[arbre.lettre] = prefixe


"""
Cette fonction renvoie un dictionnaire contenant les lettres et leur code
"""


def code_huffman(arbre):
    # on remplit le dictionnaire du code d'Huffman en parcourant l'arbre
    code = {}
    if arbre == None:
        return None
    parcours(arbre, "", code)
    return code


# Ex.3  encodage d'un texte contenu dans un fichier

"""
Cette fonction permet d'écrire le header du fichier encodé
"""


def header_huffman_tree_write(file_out, dico):
    dict_encoded = ""
    code_encoded = ""

    longeur_dico_bit = 0
    for lettre in dico:
        code = dico.get(lettre)
        longeur_dico_bit += 16 + 8 + len(code)

        unicode_lettre = format(ord(lettre), "#018b")[2:]
        longueur_code = format(len(dico.get(lettre)), "#010b")[2:]
        code_lettre = dico.get(lettre)
        dict_encoded += unicode_lettre + longueur_code
        code_encoded += code_lettre

    dict_encoded += code_encoded
    longeur_dico_octet = math.ceil(longeur_dico_bit / 8)
    padding_dico_octet = 8 - (longeur_dico_bit % 8)

    file_out.write(padding_dico_octet.to_bytes(1, "little"))
    file_out.write(longeur_dico_octet.to_bytes(2, "big"))
    file_out.write(len(dico).to_bytes(1, "little"))

    for i in range(longeur_dico_octet):
        chain = dict_encoded[8 * i : 8 + 8 * i]
        if not chain:
            break
        buffer = int(chain, 2)
        file_out.write(buffer.to_bytes(1, "big"))


"""
Cette fonction encode le fichier donné en entrée

IN:
    dico : dictionnaire contenant les codes des lettres
    fichier_entree : fichier à encoder
    fichier_sortie : fichier de sortie
    dans_fichier : True si l'arbre est à mettre dans le fichier, sinon False
"""


def encodage(dico, fichier_entree, fichier_sortie, dans_fichier=True):
    if dico == None:
        return print("Il n'y a rien à encoder")
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

            if dans_fichier:
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

    if out_str == "":
        return print("Il n'y a rien à encoder")

    diff_size = 1 - (os.path.getsize(fichier_sortie) / os.path.getsize(fichier_entree))
    print(
        "Le taux de compression est le suivant : "
        + str(round(diff_size * 100, 2))
        + " %"
    )


"""
Cette fonction décode le fichier donné en entrée

IN:
    fichier_compresse : fichier à décompresser
    fichier_sortie : fichier décompressé
    arbre : False si l'arbre est dans le fichier, sinon True
"""


def decodage(fichier_compresse, fichier_sortie, arbre=False):
    with open(fichier_compresse, "rb") as file:
        content = file.read()
        content_bin = bin(int.from_bytes(content, "big"))[2:]
        content_bin = "0" * (8 - (len(content_bin) % 8)) + content_bin

        padding_text, content_bin = content_bin[:8], content_bin[8:]
        padding_text = int(padding_text, 2)
        if not arbre:
            padding_dico, content_bin = content_bin[:8], content_bin[8:]
            len_dict, content_bin = content_bin[:16], content_bin[16:]
            number_of_letter, content_bin = content_bin[:8], content_bin[8:]

            padding_dico = int(padding_dico, 2)
            len_dict = int(len_dict, 2)
            number_of_letter = int(number_of_letter, 2)

            letter_dict = {}

            size_code = 0
            for i in range(number_of_letter):
                unicode, content_bin = content_bin[:16], content_bin[16:]
                size, content_bin = content_bin[:8], content_bin[8:]
                unicode = chr(int(unicode, 2))
                size = int(size, 2)
                size_code += size
                letter_dict[unicode] = size

            while size_code % 8 != 0:
                size_code += 1

            # remove padding
            only_code, content_bin = content_bin[:size_code], content_bin[size_code:]

            only_code = (
                only_code[: len(only_code) - 8]
                + only_code[len(only_code) - 8 :][-(8 - padding_dico) :]
            )

            for letter in letter_dict:
                size = letter_dict.get(letter)
                code, only_code = only_code[:size], only_code[size:]

                letter_dict[letter] = code
        else:
            tree = arbre_huffman(frequences(caracteres, proba))
            letter_dict = code_huffman(tree)

        content_bin = (
            content_bin[: len(content_bin) - 8]
            + content_bin[len(content_bin) - 8 :][-(8 - padding_text) :]
        )

        with open(fichier_sortie, "w") as file:
            while len(content_bin) > 0:
                keep = ""
                for k in letter_dict:
                    code_letter = letter_dict.get(k)
                    if code_letter == content_bin[: len(code_letter)]:
                        if keep == "":
                            keep = k
                        elif len(code_letter) > len(letter_dict.get(keep)):
                            keep = k
                file.write(keep)
                content_bin = content_bin[len(letter_dict.get(keep)) :]


if __name__ == "__main__":
    valid = False

    if len(sys.argv) == 5:
        if sys.argv[1] == "e":
            if sys.argv[4] == "0":
                valid = True
                encodage(
                    code_huffman(arbre_huffman(frequences_depuis_texte(sys.argv[2]))),
                    sys.argv[2],
                    sys.argv[3],
                    True,
                )
            elif sys.argv[4] == "1":
                encodage(
                    code_huffman(arbre_huffman(frequences(caracteres, proba))),
                    sys.argv[2],
                    sys.argv[3],
                    False,
                )
                valid = True
        elif sys.argv[1] == "d":
            if sys.argv[4] == "0":
                decodage(sys.argv[2], sys.argv[3], False)
                valid = True
            elif sys.argv[4] == "1":
                decodage(sys.argv[2], sys.argv[3], True)
                valid = True

    if not valid:
        print(
            """Utilisation :
            Pour encoder :
                python3 src/huffman.py e file_to_encode file_output [0,1]
            Pour decoder :
                python3 src/huffman.py d file_to_decode file_output [0,1]
            
            Le mode 0 construit l'arbre en fonction du fichier d'entrée et
            le mode 1 en fonction de la table de fréquence"""
        )
