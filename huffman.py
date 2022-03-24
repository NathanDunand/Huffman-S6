#####################################################
######  Introduction à la cryptographie  	###
#####   Codes de Huffman             		###
####################################################

import math
import unidecode

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


def header_huffman_tree_write(file_out, dico):
    print(dico)
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


def encodage(dico, fichier_entree, fichier_sortie, dans_fichier=True):
    out_str = ""
    with open(fichier_entree, "r") as file_in:
        with open(fichier_sortie, "wb") as file_out:
            while True:
                c = file_in.read(1)
                if not c:
                    break
                if not dans_fichier:
                    c = unidecode.unidecode(c.lower())
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


###  Ex.4  décodage d'un fichier compresse
# Eerie eyeseen
def decodage(fichierCompresse, arbre=False):
    with open(fichierCompresse, "rb") as file:
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
            tree = arbre_huffman(frequences(caracteres, proba))[0]
            letter_dict = code_huffman(tree)

        content_bin = (
            content_bin[: len(content_bin) - 8]
            + content_bin[len(content_bin) - 8 :][-(8 - padding_text) :]
        )

        print(letter_dict)

        decoded_text = ""
        while len(content_bin) > 0:
            keep = ""
            for k in letter_dict:
                code_letter = letter_dict.get(k)
                if code_letter == content_bin[: len(code_letter)]:
                    if keep == "":
                        keep = k
                    elif len(code_letter) > len(letter_dict.get(keep)):
                        keep = k
            decoded_text += keep
            content_bin = content_bin[len(letter_dict.get(keep)) :]

        print("TEXTE DECODE : " + decoded_text)


if __name__ == "__main__":
    """Ft = frequences(caracteres, proba)
    tree = arbre_huffman(Ft)[0]
    code = code_huffman(tree)
    encodage(code, "unelettre.txt", "unelettreencode", False)

    decodage("unelettreencode", True)"""

    Ft = frequences(caracteres, proba)
    tree = arbre_huffman(Ft)[0]
    code = code_huffman(tree)
    encodage(code, "unelettre.txt", "unelettreencode", False)

    decodage("unelettreencode", True)

"""
    Ft = frequences_depuis_texte("leHorla.txt")
    tree = arbre_huffman(Ft)[0]he
    code = code_huffman(tree)
    encodage(code, "leHorla.txt", "leHorla.out")

    decodage("leHorla.out")
    """
