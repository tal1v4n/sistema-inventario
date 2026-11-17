#!/usr/bin/env bash
# Despliega en el servidor una versión publicada en GitHub Releases.
# Uso: desplegar.sh <version> [--simular-falla]
# Ejemplo: desplegar.sh v1.1.0
set -euo pipefail

VERSION="${1:?Indica la versión, por ejemplo v1.0.2}"
SIMULAR_FALLA="${2:-}"

BASE="$HOME/sistema-inventario"
PAQUETE="sistema-inventario-$VERSION.zip"
SCRIPTS="$BASE/scripts"

registrar() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$BASE/historial.log"
    echo "$1"
}

mkdir -p "$BASE/entrantes" "$BASE/paquetes" "$BASE/versiones" "$SCRIPTS"

# Copiar los scripts que llegaron con el workflow
if [ -d "$BASE/entrantes/deploy" ]; then
    cp "$BASE/entrantes/deploy/"*.sh "$SCRIPTS/"
    chmod +x "$SCRIPTS/"*.sh
fi

# Requisitos del entorno
for comando in python3 unzip; do
    if ! command -v "$comando" >/dev/null 2>&1; then
        registrar "ERROR: falta $comando en el servidor. Instálalo con: sudo apt install $comando"
        exit 1
    fi
done

# Conservar el paquete recibido
if [ -f "$BASE/entrantes/$PAQUETE" ]; then
    mv -f "$BASE/entrantes/$PAQUETE" "$BASE/paquetes/$PAQUETE"
fi
if [ ! -f "$BASE/paquetes/$PAQUETE" ]; then
    registrar "ERROR: no se encontró el paquete $PAQUETE"
    exit 1
fi
unzip -tq "$BASE/paquetes/$PAQUETE" >/dev/null || {
    registrar "ERROR: el paquete $PAQUETE está dañado"
    exit 1
}

# Extraer en una carpeta propia de la versión
DESTINO="$BASE/versiones/$VERSION"
rm -rf "$DESTINO"
mkdir -p "$DESTINO"
unzip -q "$BASE/paquetes/$PAQUETE" -d "$DESTINO"
find "$DESTINO" -name "__pycache__" -type d -prune -exec rm -rf {} +
registrar "Paquete $PAQUETE extraído en versiones/$VERSION"

if [ "$SIMULAR_FALLA" = "--simular-falla" ]; then
    rm -f "$DESTINO/src/producto.py"
    registrar "SIMULACIÓN: se eliminó src/producto.py de $VERSION para provocar una falla"
fi

# Activar la nueva versión y guardar cuál estaba antes
ANTERIOR=""
if [ -L "$BASE/actual" ]; then
    ANTERIOR="$(basename "$(readlink "$BASE/actual")")"
fi
# Si se vuelve a desplegar la misma versión, la anterior es la que ya estaba registrada
if [ "$ANTERIOR" = "$VERSION" ]; then
    ANTERIOR="$(cat "$BASE/version-anterior" 2>/dev/null || true)"
fi
if [ -n "$ANTERIOR" ]; then
    echo "$ANTERIOR" > "$BASE/version-anterior"
fi
ln -sfn "$DESTINO" "$BASE/actual"
registrar "Versión activa: $VERSION (anterior: ${ANTERIOR:-ninguna})"

# Verificar y, si falla, regresar a la versión anterior
if bash "$SCRIPTS/verificar.sh" "$BASE/actual"; then
    echo "$VERSION" > "$BASE/version-actual"
    registrar "DESPLIEGUE CORRECTO de $VERSION"
    exit 0
fi

registrar "FALLA en la verificación de $VERSION"
if [ -n "$ANTERIOR" ] && [ "$ANTERIOR" != "$VERSION" ]; then
    registrar "Iniciando recuperación automática a $ANTERIOR"
    bash "$SCRIPTS/revertir.sh" "$ANTERIOR"
else
    registrar "No hay una versión anterior para recuperar"
fi
exit 1
