class Producto:
    """Representa un producto del inventario."""

    def __init__(self, codigo, nombre, precio, existencia):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.existencia = existencia

    def mostrar_informacion(self):
        """Muestra en pantalla la información del producto."""
        print("----- INFORMACIÓN DEL PRODUCTO -----")
        print(f"Código     : {self.codigo}")
        print(f"Nombre     : {self.nombre}")
        print(f"Precio     : ${self.precio:,.2f}")
        print(f"Existencia : {self.existencia} unidades")
        print("Respuesta")


# Ejemplo de uso
if __name__ == "__main__":
    producto1 = Producto("P001", "Teclado mecánico", 450.00, 25)
    producto1.mostrar_informacion()