# sistema-inventario
Sistema web para la gestión de inventarios de un comercio electrónico.

## Pruebas (fase TEST)

Las pruebas de la clase `Producto` están en `tests/test_producto.py` y usan `unittest`, que viene incluido con Python.

Ejecutar todas las pruebas:

```bash
python -m unittest discover -s tests -v
```

Ejecutar las pruebas con el reporte de resultados:

```bash
python tests/test_producto.py
```

| ID | Caso de prueba | Datos de entrada | Resultado esperado |
|----|----------------|------------------|--------------------|
| CP01 | Crear un producto | P001, Teclado, 350, 10 | El producto se crea con los datos proporcionados |
| CP02 | Mostrar el código | P001 | Se muestra P001 |
| CP03 | Mostrar el nombre | Teclado | Se muestra Teclado |
| CP04 | Mostrar el precio | 350 | Se muestra 350 |
| CP05 | Mostrar la existencia | 10 | Se muestra 10 |
| CP06 | Mostrar información completa | Todos los datos anteriores | Se muestran los cuatro datos correctamente |
| CP07 | Crear otro producto | P002, Mouse, 180, 5 | Se crea sin confundir sus datos con los del primero |

Las pruebas también se ejecutan de forma automática con GitHub Actions (`.github/workflows/tests.yml`) en cada push y pull request a `main`. Las evidencias de ejecución están en la carpeta `evidencias/`.
