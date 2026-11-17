#!/usr/bin/env bash
# Muestra qué versión está activa en el servidor y el historial reciente.
BASE="$HOME/sistema-inventario"

echo "Servidor        : $(hostname)"
echo "Usuario         : $(whoami)"
echo "Python          : $(python3 --version 2>&1)"
if [ -L "$BASE/actual" ]; then
    echo "Versión activa  : $(basename "$(readlink "$BASE/actual")")"
else
    echo "Versión activa  : ninguna"
fi
echo "Versión anterior: $(cat "$BASE/version-anterior" 2>/dev/null || echo ninguna)"
echo
echo "Paquetes conservados:"
ls -l "$BASE/paquetes" 2>/dev/null | tail -n +2 | awk '{print "  " $NF " (" $5 " bytes)"}'
echo
echo "Versiones extraídas:"
ls "$BASE/versiones" 2>/dev/null | sed 's/^/  /'
echo
echo "Historial (últimos 15 movimientos):"
tail -n 15 "$BASE/historial.log" 2>/dev/null | sed 's/^/  /'
