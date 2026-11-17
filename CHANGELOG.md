# Historial de versiones

## v1.1.0

- Nuevo menú principal (`src/main.py`) para registrar, listar y buscar productos.
- Validación de código duplicado, precio y existencia.
- Pruebas del menú (CP08 a CP12).
- El paquete ya no incluye la carpeta `__pycache__`.
- Scripts y workflows de despliegue (`deploy/`, `deploy.yml`, `rollback.yml`).

## v1.0.2

- Corrección del error en la visualización del precio detectado durante las pruebas.
- Validación satisfactoria de la funcionalidad Producto (7 de 7 pruebas).
- Publicación del paquete sistema-inventario-v1.0.2.zip.

## v1.0.1 (no publicada)

- Versión con un error intencional en el precio.
- El workflow de liberación se detuvo en las pruebas y no se publicó.

## v1.0.0

- Primera versión del Sistema de Inventario.
- Incorporación de la funcionalidad Producto.
- Implementación de pruebas automatizadas con unittest.
- Workflow de liberación con GitHub Actions y GitHub Releases.
