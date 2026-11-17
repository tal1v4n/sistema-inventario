from producto import Producto
from busqueda import buscar_por_codigo, buscar_por_nombre

VERSION = "1.1.0"


def leer(mensaje):
    """Lee una línea del teclado. Regresa None si ya no hay entrada (EOF)."""
    try:
        return input(mensaje).strip()
    except EOFError:
        return None


def leer_numero(mensaje, tipo):
    """Pide un número hasta que sea válido y no negativo."""
    while True:
        texto = leer(mensaje)
        if texto is None:
            return None
        try:
            valor = tipo(texto)
        except ValueError:
            print("Valor no válido, intenta de nuevo.")
            continue
        if valor < 0:
            print("El valor no puede ser negativo.")
            continue
        return valor


def registrar_producto(inventario):
    codigo = leer("Código: ")
    if not codigo:
        print("El código es obligatorio.")
        return
    if buscar_por_codigo(inventario, codigo):
        print(f"Ya existe un producto con el código {codigo}.")
        return

    nombre = leer("Nombre: ")
    if not nombre:
        print("El nombre es obligatorio.")
        return

    precio = leer_numero("Precio: ", float)
    if precio is None:
        return
    existencia = leer_numero("Existencia: ", int)
    if existencia is None:
        return

    inventario.append(Producto(codigo, nombre, precio, existencia))
    print(f"Producto {codigo} registrado correctamente.")


def mostrar_productos(inventario):
    if not inventario:
        print("No hay productos registrados.")
        return
    print(f"Total de productos: {len(inventario)}")
    for producto in inventario:
        producto.mostrar_informacion()


def consultar_por_codigo(inventario):
    codigo = leer("Código a buscar: ")
    if codigo is None:
        return
    producto = buscar_por_codigo(inventario, codigo)
    if producto:
        producto.mostrar_informacion()
    else:
        print("Producto no encontrado.")


def consultar_por_nombre(inventario):
    texto = leer("Nombre o parte del nombre: ")
    if texto is None:
        return
    coincidencias = buscar_por_nombre(inventario, texto)
    if not coincidencias:
        print("No hay coincidencias.")
        return
    print(f"Se encontraron {len(coincidencias)} coincidencias:")
    for producto in coincidencias:
        producto.mostrar_informacion()


def menu():
    inventario = []
    opciones = {
        "1": registrar_producto,
        "2": mostrar_productos,
        "3": consultar_por_codigo,
        "4": consultar_por_nombre,
    }

    print(f"SISTEMA DE INVENTARIO v{VERSION}")
    while True:
        print("\n1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Buscar por código")
        print("4. Buscar por nombre")
        print("5. Salir")
        opcion = leer("Elige una opción: ")

        if opcion is None or opcion == "5":
            print("Hasta luego.")
            break
        accion = opciones.get(opcion)
        if accion:
            accion(inventario)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
