"""Testes unitários da lógica de geração (mikeygenerator.keygen)."""

import unittest

from mikeygenerator.keygen import (
    ALGORITMOS,
    CARACTERES,
    ajustar_valor,
    calcular_hash,
    gerar_chave,
)


class TestGerarChave(unittest.TestCase):
    def test_formato_padrao(self):
        chave = gerar_chave(5, 5)
        self.assertRegex(chave, r"^[A-Za-z0-9]{5}(-[A-Za-z0-9]{5}){4}$")

    def test_numero_de_segmentos(self):
        for count in (1, 3, 8):
            chave = gerar_chave(count, 4)
            self.assertEqual(len(chave.split("-")), count)

    def test_tamanho_dos_segmentos(self):
        chave = gerar_chave(6, 3)
        segmentos = chave.split("-")
        self.assertTrue(all(len(s) == 3 for s in segmentos))

    def test_caracteres_permitidos(self):
        chave = gerar_chave(4, 4)
        sem_hifens = chave.replace("-", "")
        self.assertTrue(all(c in CARACTERES for c in sem_hifens))

    def test_valores_minimos_forcados(self):
        # segment_count=0 e segment_length=-2 devem virar 1x1
        chave = gerar_chave(0, -2)
        self.assertRegex(chave, r"^[A-Za-z0-9]{1}$")

    def test_aleatoriedade(self):
        chaves = {gerar_chave(5, 5) for _ in range(20)}
        self.assertEqual(len(chaves), 20)


class TestCalcularHash(unittest.TestCase):
    def test_hashes_conhecidos(self):
        chave = "abc123"
        esperados = {
            "MD5": "e99a18c428cb38d5f260853678922e03",
            "SHA1": "6367c48dd193d56ea7b0baad25b19455e529f5ee",
            "SHA256": "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090",
            "SHA512": (
                "c70b5dd9ebfb6f51d09d4132b7170c9d20750a7852f00680f65658f0310e8100"
                "56e6763c34c9a00b0e940076f54495c169fc2302cceb312039271c43469507dc"
            ),
        }
        for alg in ALGORITMOS:
            self.assertEqual(calcular_hash(chave, alg), esperados[alg])

    def test_algoritmo_padrao(self):
        self.assertEqual(
            calcular_hash("abc123"),
            calcular_hash("abc123", "SHA256"),
        )

    def test_fallback_para_desconhecido(self):
        # Algoritmo não reconhecido deve usar SHA512 (comportamento original)
        self.assertEqual(
            calcular_hash("abc123", "DESCONHECIDO"),
            calcular_hash("abc123", "SHA512"),
        )

    def test_hash_muda_com_a_chave(self):
        self.assertNotEqual(calcular_hash("chave1"), calcular_hash("chave2"))


class TestAjustarValor(unittest.TestCase):
    def test_limites(self):
        self.assertEqual(ajustar_valor(0), 1)
        self.assertEqual(ajustar_valor(-5), 1)
        self.assertEqual(ajustar_valor(1), 1)
        self.assertEqual(ajustar_valor(99), 99)
        self.assertEqual(ajustar_valor(150), 99)


if __name__ == "__main__":
    unittest.main()
