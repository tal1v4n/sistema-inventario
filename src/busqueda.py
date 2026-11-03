from producto import Producto


def buscar_por_codigo(productos, codigo):
    """Busca un producto por su código exacto. Devuelve el producto o None."""
    for producto in productos:
        if producto.codigo.lower() == codigo.lower():
            return producto
    return None


def buscar_por_nombre(productos, texto):
    """Busca productos cuyo nombre contenga el texto indicado.
    Devuelve una lista (vacía si no hay coincidencias)."""
    return [p for p in productos if texto.lower() in p.nombre.lower()]


# Ejemplo de uso
if __name__ == "__main__":
    inventario = [
        Producto("P001", "Teclado mecánico", 450.00, 25),
        Producto("P002", "Mouse inalámbrico", 220.50, 40),
        Producto("P003", "Monitor 24 pulgadas", 1899.99, 10),
    ]

    # Búsqueda por código
    resultado = buscar_por_codigo(inventario, "P002")
    if resultado:
        resultado.mostrar_informacion()
    else:
        print("Producto no encontrado.")

    # Búsqueda por nombre
    coincidencias = buscar_por_nombre(inventario, "mo")
    if coincidencias:
        print(f"\nSe encontraron {len(coincidencias)} coincidencias:\n")
        for p in coincidencias:
            p.mostrar_informacion()
    else:
        print("No hay coincidencias.")