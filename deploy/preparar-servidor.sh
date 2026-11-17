#!/usr/bin/env bash
# Prepara una VM Ubuntu/Debian como entorno de destino del Sistema de Inventario.
# Se ejecuta una sola vez dentro de la VM: bash preparar-servidor.sh
set -euo pipefail

echo "Instalando Python, unzip y servidor SSH..."
sudo apt update
sudo apt install -y python3 unzip openssh-server

sudo systemctl enable --now ssh

mkdir -p ~/sistema-inventario/{entrantes,paquetes,versiones,scripts}
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

echo
echo "Comprobación del entorno"
python3 --version
unzip -v | head -1
systemctl is-active ssh
echo "Usuario   : $(whoami)"
echo "IP local  : $(hostname -I)"
echo "Carpeta   : $HOME/sistema-inventario"
echo
echo "Falta pegar la llave pública de GitHub Actions en ~/.ssh/authorized_keys"
