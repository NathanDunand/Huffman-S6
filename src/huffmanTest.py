"""
Ce fichier sert à effectuer des tests sur le code du fichier
huffman.py

Les textes utilisé dans ce fichier sont stockés dans le dossier
textes_exemples
"""
from huffman import *
import unittest


class TestHuffman(unittest.TestCase):
    """Test class that extends TestCase from unittest"""

    def test_frequences(self):
        """
        This method performs all normal and limit unit tests about the
        frequences method from huffman module
        """
        self.assertEqual(str(frequences(["a"], [1])), str({"a": 1}))
        self.assertEqual(str(frequences(["a", "b"], [1, 1])), str({"a": 1, "b": 1}))
        self.assertEqual(str(frequences([], [])), str({}))

    def test_frequences_error(self):
        """
        This method performs all error unit tests about the
        frequences method from huffman module
        """
        with self.assertRaises(TypeError):
            frequences(None, None)
            frequences(None, [])
            frequences([], None)

    def test_frequences_depuis_texte(self):
        """
        This method performs all normal and limit unit tests about the
        frequences_depuis_texte method from huffman module
        """
        self.assertEqual(
            str(
                frequences_depuis_texte(
                    "src/textes_exemples/textes_non_compresses/une_lettre.txt"
                )
            ),
            str({"l": 1.0}),
        )
        self.assertEqual(str(frequences([], [])), str({}))

    def test_frequences_depuis_texte_error(self):
        """
        This method performs all error unit tests about the
        frequences_depuis_texte method from huffman module
        """
        with self.assertRaises(TypeError):
            frequences_depuis_texte(None, None)
            frequences_depuis_texte(None, [])
            frequences_depuis_texte([], None)

    def test_arbre_init(self):
        """
        This method performs all normal and limit unit tests about the
        init method of Arbre class from huffman module
        """

        self.assertEqual(str(Arbre(1)), "<1..None.None>")
        self.assertEqual(str(Arbre(1, "e")), "<1.e.None.None>")
        self.assertEqual(
            str(Arbre(1, "e", Arbre(0.5, "z"), Arbre(0.25, "w"))),
            "<1.e.<0.5.z.None.None>.<0.25.w.None.None>>",
        )

    def test_arbre_init_error(self):
        """
        This method performs all error unit tests about the
        init method of Arbre class from huffman module
        """

        with self.assertRaises(TypeError):
            Arbre()

    def test_arbre_estFeuille(self):
        """
        This method performs all normal and limit unit tests about the
        estFeuille method of Arbre class from huffman module
        """

        self.assertTrue(Arbre(1).estFeuille)
        self.assertFalse(Arbre(1, "e", Arbre(2)).estFeuille())

    def test_heappush(self):
        """
        This method performs all normal and limit unit tests about the
        heappush method from huffman module
        """
        self.assertTrue(heappush([], Arbre(1)))
        self.assertFalse(heappush(None, Arbre(1)))
        self.assertTrue(heappush([Arbre(1)], Arbre(2)))
        self.assertFalse(heappush([], None))

    def test_heappush_error(self):
        """
        This method performs all error unit tests about the
        heappush method from huffman module
        """
        with self.assertRaises(TypeError):
            heappush()
            heappush(1)

    def test_heappop(self):
        """
        This method performs all normal and limit unit tests about the
        heappop method from huffman module
        """
        a = [1, 2, 6, 6]
        self.assertEqual(heappop(a), 1)
        self.assertEqual(heappop(a), 2)
        self.assertEqual(heappop(a), 6)
        self.assertEqual(heappop(a), 6)
        self.assertEqual(heappop(a), None)

    def test_heappop_error(self):
        """
        This method performs all error unit tests about the
        heappop method from huffman module
        """

        with self.assertRaises(TypeError):
            heappop()

    def test_arbre_huffman(self):
        """
        This method performs all normal and limit unit tests about the
        arbre_huffman method from huffman module
        """

        self.assertEqual(str(arbre_huffman({"a": 2})), "<2.a.None.None>")
        self.assertEqual(
            str(arbre_huffman({"a": 12, "b": 10, "c": 4, "d": 6, "e": 2, "f": 2})),
            "<36..<14..<6.d.None.None>.<8..<4.c.None.None>.<4..<2.e.None.None>.<2.f.None.None>>>>.<22..<10.b.None.None>.<12.a.None.None>>>",
        )
        self.assertEqual(arbre_huffman({}), None)
        self.assertEqual(arbre_huffman(None), None)

    def test_arbre_huffman_error(self):
        """
        This method performs all error unit tests about the
        arbre_huffman method from huffman module
        """

        with self.assertRaises(TypeError):
            arbre_huffman()

    def test_code_huffman(self):
        """
        This method performs all normal and limit unit tests about the
        code_huffman method from huffman module
        """
        self.assertEqual(code_huffman(None), None)
        self.assertEqual(str(code_huffman(arbre_huffman({"a": 2}))), str({"a": "0"}))
        self.assertEqual(
            str(
                code_huffman(
                    arbre_huffman({"a": 12, "b": 10, "c": 4, "d": 6, "e": 2, "f": 2})
                )
            ),
            "{'d': '00', 'c': '010', 'e': '0110', 'f': '0111', 'b': '10', 'a': '11'}",
        )

    def test_code_huffman_error(self):
        """
        This method performs all error unit tests about the
        code_huffman method from huffman module
        """
        with self.assertRaises(TypeError):
            code_huffman()


def testEncodageDecodage():
    # Test 1 : cas normal : leHorlat.txt
    # Arbre construit à partir du texte

    print("\nTest 1 : cas normal : leHorlat.txt")
    freq = frequences_depuis_texte(
        "src/textes_exemples/textes_non_compresses/leHorla.txt"
    )
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/leHorla.txt",
        "src/textes_exemples/textes_compresses/leHorla.out1",
        True,
    )

    decodage(
        "src/textes_exemples/textes_compresses/leHorla.out1",
        "src/textes_exemples/textes_non_compresses/leHorlat.txt.out1",
        False,
    )

    # Test 2 : cas normal : leHorlat.txt
    # Arbre construit à partir des fréquences statiques

    print("\nTest 2 : cas normal : leHorlat.txt")

    freq = frequences(caracteres, proba)
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/leHorla.txt",
        "src/textes_exemples/textes_compresses/leHorla.out2",
        False,
    )

    decodage(
        "src/textes_exemples/textes_compresses/leHorla.out2",
        "src/textes_exemples/textes_non_compresses/leHorlat.txt.out2",
        True,
    )

    # Test 3 : cas normal : chevalier.txt
    # Arbre construit à partir du texte

    print("\nTest 3 : cas normal : chevalier.txt")

    freq = frequences_depuis_texte(
        "src/textes_exemples/textes_non_compresses/chevalier.txt"
    )
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/chevalier.txt",
        "src/textes_exemples/textes_compresses/chevalier.out1",
        True,
    )

    decodage(
        "src/textes_exemples/textes_compresses/chevalier.out1",
        "src/textes_exemples/textes_non_compresses/chevalier.txt.out1",
        False,
    )

    # Test 4 : cas normal : chevalier.txt
    # Arbre construit à partir des fréquences statiques

    print("\nTest 4 : cas normal : chevalier.txt")

    freq = frequences(caracteres, proba)
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/chevalier.txt",
        "src/textes_exemples/textes_compresses/chevalier.out2",
        False,
    )

    decodage(
        "src/textes_exemples/textes_compresses/chevalier.out2",
        "src/textes_exemples/textes_non_compresses/chevalier.txt.out2",
        True,
    )

    # Test 5 : cas normal : big.txt
    # Arbre construit à partir du texte

    print("\nTest 5 : cas normal : big.txt")

    freq = frequences_depuis_texte("src/textes_exemples/textes_non_compresses/big.txt")
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/big.txt",
        "src/textes_exemples/textes_compresses/big.out1",
        True,
    )

    decodage(
        "src/textes_exemples/textes_compresses/big.out1",
        "src/textes_exemples/textes_non_compresses/big.txt.out1",
        False,
    )

    # Test 6 : cas normal : big.txt
    # Arbre construit à partir des fréquences statiques

    print("\nTest 6 : cas normal : big.txt")

    freq = frequences(caracteres, proba)
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/big.txt",
        "src/textes_exemples/textes_compresses/big.out2",
        False,
    )

    decodage(
        "src/textes_exemples/textes_compresses/big.out2",
        "src/textes_exemples/textes_non_compresses/big.txt.out2",
        True,
    )

    # Test 7 : cas limite : une_lettre.txt
    # Arbre construit à partir du texte

    print("\nTest 7 : cas limite : une_lettre.txt")

    freq = frequences_depuis_texte(
        "src/textes_exemples/textes_non_compresses/une_lettre.txt"
    )
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/une_lettre.txt",
        "src/textes_exemples/textes_compresses/une_lettre.out1",
        True,
    )

    decodage(
        "src/textes_exemples/textes_compresses/une_lettre.out1",
        "src/textes_exemples/textes_non_compresses/une_lettre.txt.out1",
        False,
    )

    # Test 8 : cas limite : une_lettre.txt
    # Arbre construit à partir des fréquences statiques

    print("\nTest 8 : cas limite : une_lettre.txt")

    freq = frequences(caracteres, proba)
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/une_lettre.txt",
        "src/textes_exemples/textes_compresses/une_lettre.out2",
        False,
    )

    decodage(
        "src/textes_exemples/textes_compresses/une_lettre.out2",
        "src/textes_exemples/textes_non_compresses/une_lettre.txt.out2",
        True,
    )

    # Test 9 : cas erreur : pas_de_lettre.txt
    # Arbre construit à partir du texte

    print("\nTest 9 : cas erreur : pas_de_lettre.txt")

    freq = frequences_depuis_texte(
        "src/textes_exemples/textes_non_compresses/pas_de_lettre.txt"
    )
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/pas_de_lettre.txt",
        "src/textes_exemples/textes_compresses/pas_de_lettre.out1",
        True,
    )

    # Test 9 : cas erreur : pas_de_lettre.txt
    # Arbre construit à partir des fréquences statiques

    print("\nTest 8 : cas erreur : pas_de_lettre.txt")

    freq = frequences(caracteres, proba)
    tree = arbre_huffman(freq)
    code = code_huffman(tree)
    encodage(
        code,
        "src/textes_exemples/textes_non_compresses/pas_de_lettre.txt",
        "src/textes_exemples/textes_compresses/pas_de_lettre.out2",
        False,
    )


if __name__ == "__main__":

    testEncodageDecodage()
    unittest.main()
