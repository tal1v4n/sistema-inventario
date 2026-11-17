import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import main


def ejecutar_menu(entradas):
    """Corre el menú con las entradas indicadas y regresa lo que imprimió."""
    buffer = io.StringIO()
    with patch("builtins.input", side_effect=entradas), redirect_stdout(buffer):
        main.menu()
    return buffer.getvalue()


class TestMenu(unittest.TestCase):

    def test_cp08_registrar_y_mostrar(self):
        """CP08 - Registrar y mostrar producto"""
        salida = ejecutar_menu(["1", "P010", "Bocina", "299.9", "7", "2", "5"])
        self.assertIn("Producto P010 registrado correctamente.", salida)
        self.assertIn("Total de productos: 1", salida)
        self.assertIn("Nombre     : Bocina", salida)
        self.assertIn("Precio     : $299.90", salida)

    def test_cp09_buscar_por_codigo(self):
        """CP09 - Buscar por código"""
        salida = ejecutar_menu(["1", "P011", "Cable HDMI", "120", "15", "3", "p011", "5"])
        self.assertIn("Código     : P011", salida)
        self.assertNotIn("Producto no encontrado.", salida)

    def test_cp10_codigo_duplicado(self):
        """CP10 - Rechazar código duplicado"""
        salida = ejecutar_menu([
            "1", "P012", "Hub USB", "250", "4",
            "1", "P012",
            "2", "5",
        ])
        self.assertIn("Ya existe un producto con el código P012.", salida)
        self.assertIn("Total de productos: 1", salida)

    def test_cp11_precio_invalido(self):
        """CP11 - Validar precio"""
        salida = ejecutar_menu(["1", "P013", "Webcam", "abc", "-5", "560", "3", "5"])
        self.assertIn("Valor no válido", salida)
        self.assertIn("no puede ser negativo", salida)
        self.assertIn("Producto P013 registrado correctamente.", salida)

    def test_cp12_fin_de_entrada(self):
        """CP12 - Termina sin error si no hay más entrada"""
        with patch("builtins.input", side_effect=EOFError):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                main.menu()
        self.assertIn("Hasta luego.", buffer.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
