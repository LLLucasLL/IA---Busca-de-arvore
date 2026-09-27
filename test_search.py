import os
import subprocess
import sys
import unittest
from BuscaP import buscaP
import F_auxiliares as fa


class BuscaPTests(unittest.TestCase):
    def test_custo_uniforme_grid_encontra_objetivo(self):
        mapa, nx, ny = fa.Gera_Problema_Grid_Fixo_P('mapa.txt')
        solver = buscaP()

        resultado = solver.custo_uniforme_grid([7, 0], [1, 4], mapa, nx, ny)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0][-1], [1, 4])
        self.assertGreaterEqual(resultado[1], 0)

    def test_aia_estrela_grid_termina(self):
        script = """
import sys
from BuscaP import buscaP
import F_auxiliares as fa
mapa, nx, ny = fa.Gera_Problema_Grid_Fixo_P('mapa.txt')
solver = buscaP()
resultado = solver.aia_estrela_grid([7, 0], [1, 4], mapa, nx, ny)
print(resultado is not None)
"""
        completed = subprocess.run(
            [sys.executable, '-c', script],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        self.assertIn('True', completed.stdout)


if __name__ == '__main__':
    unittest.main()
