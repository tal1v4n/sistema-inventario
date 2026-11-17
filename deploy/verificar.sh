#!/usr/bin/env bash
# Verifica que una versión desplegada del Sistema de Inventario funciona.
# Uso: verificar.sh <carpeta-de-la-version>
set -u

DIR="${1:?Indica la carpeta de la versión a verificar}"
FALLAS=0

ok()    { echo "  [OK]    $1"; }
falla() { echo "  [FALLA] $1"; FALLAS=$((FALLAS + 1)); }

echo "Verificando: $DIR"

if command -v python3 >/dev/null 2>&1; then
    ok "Python disponible: $(python3 --version 2>&1)"
else
    falla "python3 no está instalado"
    exit 1
fi

cd "$DIR" 2>/dev/null || { falla "No existe la carpeta $DIR"; exit 1; }

for archivo in src/producto.py src/busqueda.py; do
    if [ -f "$archivo" ]; then ok "Existe $archivo"; else falla "Falta $archivo"; fi
done

# Mostrar un producto
salida=$(python3 src/producto.py 2>&1)
if echo "$salida" | grep -q "Código     : P001"; then
    ok "Se muestra la información de un producto"
else
    falla "src/producto.py no se ejecutó bien"
    echo "$salida" | sed 's/^/          /'
fi

# Consultar productos
salida=$(python3 src/busqueda.py 2>&1)
if echo "$salida" | grep -q "coincidencias"; then
    ok "La búsqueda de productos responde"
else
    falla "src/busqueda.py no se ejecutó bien"
    echo "$salida" | sed 's/^/          /'
fi

# A partir de v1.1.0 existe el menú principal
if [ -f src/main.py ]; then
    entradas=$'1\nV001\nProducto de verificacion\n99.5\n3\n2\n3\nV001\n5\n'
    salida=$(printf '%s' "$entradas" | python3 src/main.py 2>&1)
    if echo "$salida" | grep -q "Producto V001 registrado correctamente." \
        && echo "$salida" | grep -q "Total de productos: 1" \
        && echo "$salida" | grep -q "Precio     : \$99.50"; then
        ok "Menú principal: se registra y se consulta un producto"
    else
        falla "src/main.py no permitió registrar o consultar"
        echo "$salida" | tail -5 | sed 's/^/          /'
    fi
fi

if [ "$FALLAS" -eq 0 ]; then
    echo "Resultado: verificación correcta"
    exit 0
fi
echo "Resultado: $FALLAS comprobación(es) fallida(s)"
exit 1
