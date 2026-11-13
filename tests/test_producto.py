import io
import os
import sys
import unittest
from contextlib import redirect_stdout

# Permite importar los módulos de la carpeta src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from producto import Producto


def capturar_salida(producto):
    """Ejecuta mostrar_informacion() y regresa lo que se imprimió en pantalla."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        producto.mostrar_informacion()
    return buffer.getvalue()


class TestProducto(unittest.TestCase):

    def setUp(self):
        self.producto = Producto("P001", "Teclado", 350, 10)
        self.salida = capturar_salida(self.producto)

    def test_cp01_crear_producto(self):
        """CP01 - Crear producto"""
        self.assertIsInstance(self.producto, Producto)
        self.assertEqual(self.producto.codigo, "P001")
        self.assertEqual(self.producto.nombre, "Teclado")
        self.assertEqual(self.producto.precio, 350)
        self.assertEqual(self.producto.existencia, 10)

    def test_cp02_mostrar_codigo(self):
        """CP02 - Mostrar código"""
        self.assertEqual(self.producto.codigo, "P001")
        self.assertIn("Código     : P001", self.salida)

    def test_cp03_mostrar_nombre(self):
        """CP03 - Mostrar nombre"""
        self.assertEqual(self.producto.nombre, "Teclado")
        self.assertIn("Nombre     : Teclado", self.salida)

    def test_cp04_mostrar_precio(self):
        """CP04 - Mostrar precio"""
        self.assertEqual(self.producto.precio, 350)
        self.assertIn("Precio     : $350.00", self.salida)

    def test_cp05_mostrar_existencia(self):
        """CP05 - Mostrar existencia"""
        self.assertEqual(self.producto.existencia, 10)
        self.assertIn("Existencia : 10 unidades", self.salida)

    def test_cp06_mostrar_informacion_completa(self):
        """CP06 - Mostrar información"""
        esperado = (
            "----- INFORMACIÓN DEL PRODUCTO -----\n"
            "Código     : P001\n"
            "Nombre     : Teclado\n"
            "Precio     : $350.00\n"
            "Existencia : 10 unidades\n"
        )
        self.assertEqual(self.salida, esperado)

    def test_cp07_crear_segundo_producto(self):
        """CP07 - Crear segundo producto"""
        producto2 = Producto("P002", "Mouse", 180, 5)
        salida2 = capturar_salida(producto2)

        # El segundo producto conserva sus propios datos
        self.assertEqual(producto2.codigo, "P002")
        self.assertEqual(producto2.nombre, "Mouse")
        self.assertEqual(producto2.precio, 180)
        self.assertEqual(producto2.existencia, 5)
        self.assertIn("Código     : P002", salida2)
        self.assertIn("Precio     : $180.00", salida2)
        self.assertNotIn("Teclado", salida2)

        # El primer producto no se modificó
        self.assertEqual(self.producto.codigo, "P001")
        self.assertEqual(self.producto.nombre, "Teclado")
        self.assertEqual(self.producto.precio, 350)
        self.assertEqual(self.producto.existencia, 10)


class ReporteResultado(unittest.TextTestResult):
    """Guarda el estado de cada prueba para imprimir el reporte final."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estados = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.estados.append((test.shortDescription(), "CORRECTO"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.estados.append((test.shortDescription(), "FALLÓ"))

    def addError(self, test, err):
        super().addError(test, err)
        self.estados.append((test.shortDescription(), "ERROR"))


def ejecutar_con_reporte():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProducto)
    runner = unittest.TextTestRunner(resultclass=ReporteResultado, verbosity=2)
    resultado = runner.run(suite)

    print("\nRESULTADOS DE LAS PRUEBAS\n")
    for descripcion, estado in resultado.estados:
        print(f"{descripcion:<40}{estado}")
    correctas = sum(1 for _, e in resultado.estados if e == "CORRECTO")
    print(f"\nResultado: {correctas} de {resultado.testsRun} pruebas satisfactorias.")
    return resultado.wasSuccessful()


if __name__ == "__main__":
    sys.exit(0 if ejecutar_con_reporte() else 1)
