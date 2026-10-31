"""Prueba de caracterizacion: el comportamiento externo no debe cambiar.

La salida esperada fue capturada de la VERSION INICIAL (tag estado-inicial) y se
conserva en docs/evidencias/salida_inicial.txt.
"""
import os
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from escenario import ejecutar  # noqa: E402

GOLDEN = os.path.join(RAIZ, "docs", "evidencias", "salida_inicial.txt")


class TestCaracterizacion(unittest.TestCase):
    def test_escenario_completo_coincide_con_version_inicial(self):
        with tempfile.TemporaryDirectory() as d:
            obtenido = ejecutar(d)
        with open(GOLDEN, encoding="utf-8") as f:
            esperado = f.read()
        self.assertEqual(esperado, obtenido)


if __name__ == "__main__":
    unittest.main()
