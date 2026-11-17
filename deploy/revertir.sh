#!/usr/bin/env bash
# Regresa el Sistema de Inventario a una versión anterior usando el paquete conservado.
# Uso: revertir.sh [version]
# Sin versión, usa la que quedó registrada en version-anterior.
set -euo pipefail

BASE="$HOME/sistema-inventario"
SCRIPTS="$BASE/scripts"

registrar() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$BASE/historial.log"
    echo "$1"
}

VERSION="${1:-}"
if [ -z "$VERSION" ] && [ -f "$BASE/version-anterior" ]; then
    VERSION="$(cat "$BASE/version-anterior")"
fi
if [ -z "$VERSION" ]; then
    echo "No se indicó versión y no hay una versión anterior registrada."
    echo "Paquetes disponibles:"
    ls "$BASE/paquetes" 2>/dev/null || true
    exit 1
fi

PAQUETE="$BASE/paquetes/sistema-inventario-$VERSION.zip"
if [ ! -f "$PAQUETE" ]; then
    registrar "ERROR: no se conservó el paquete de $VERSION"
    exit 1
fi

SALIENTE=""
if [ -L "$BASE/actual" ]; then
    SALIENTE="$(basename "$(readlink "$BASE/actual")")"
fi
if [ -n "$SALIENTE" ] && [ "$SALIENTE" != "$VERSION" ]; then
    echo "$SALIENTE" > "$BASE/version-anterior"
fi

# Se vuelve a extraer desde el paquete para no reutilizar archivos que pudieron alterarse
DESTINO="$BASE/versiones/$VERSION"
rm -rf "$DESTINO"
mkdir -p "$DESTINO"
unzip -q "$PAQUETE" -d "$DESTINO"
find "$DESTINO" -name "__pycache__" -type d -prune -exec rm -rf {} +
ln -sfn "$DESTINO" "$BASE/actual"
registrar "RECUPERACIÓN: versión activa $VERSION, restaurada desde $(basename "$PAQUETE")"

if bash "$SCRIPTS/verificar.sh" "$BASE/actual"; then
    echo "$VERSION" > "$BASE/version-actual"
    registrar "RECUPERACIÓN CORRECTA a $VERSION"
    exit 0
fi
registrar "ERROR: la versión $VERSION tampoco pasó la verificación"
exit 1
