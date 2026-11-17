# Procedimiento de despliegue del Sistema de Inventario

Este documento explica cómo instalar, ejecutar y verificar una versión del Sistema de Inventario en un entorno nuevo. Siempre se usa el paquete publicado en **GitHub Releases**. No se copian archivos desde la computadora de un desarrollador.

## 1. Requisitos del entorno

| Requisito | Detalle |
|---|---|
| Sistema operativo | Linux (Ubuntu Server 22.04 o 24.04 recomendado). Para el despliegue manual también sirve Windows 10/11 |
| Python | 3.10 o superior. Se probó con 3.11, 3.12 y 3.13 |
| Bibliotecas | Ninguna. El sistema solo usa la biblioteca estándar de Python |
| unzip | Necesario en el servidor para extraer el paquete |
| Servidor SSH | `openssh-server`, para recibir el despliegue automático |
| Espacio en disco | Menos de 1 MB por versión |
| Red | Acceso a GitHub para descargar el paquete. Para el despliegue automático, el servidor debe ser alcanzable por SSH desde GitHub Actions |

Comprobación rápida en el servidor:

```bash
python3 --version
unzip -v | head -1
systemctl is-active ssh
```

## 2. Versiones disponibles

| Versión | Paquete | Contenido | Cómo se ejecuta |
|---|---|---|---|
| v1.0.0 | `sistema-inventario-v1.0.0.zip` | Clase `Producto` | `python3 src/producto.py` |
| v1.0.2 | `sistema-inventario-v1.0.2.zip` | `Producto` con precio corregido y búsqueda | `python3 src/producto.py` y `python3 src/busqueda.py` |
| v1.1.0 | `sistema-inventario-v1.1.0.zip` | Menú principal para registrar y consultar productos | `python3 src/main.py` |

La v1.0.1 no existe como paquete porque el workflow de liberación la detuvo en las pruebas.

## 3. Despliegue manual

### 3.1 Descargar el paquete

1. Entrar al repositorio en GitHub y abrir **Releases**.
2. Elegir la versión, por ejemplo **v1.0.2**.
3. En **Assets**, descargar `sistema-inventario-v1.0.2.zip`.

Desde la terminal también se puede descargar:

```bash
mkdir -p ~/despliegue-inventario && cd ~/despliegue-inventario
curl -L -o sistema-inventario-v1.0.2.zip \
  https://github.com/tal1v4n/sistema-inventario/releases/download/v1.0.2/sistema-inventario-v1.0.2.zip
```

En Windows (PowerShell):

```powershell
mkdir $HOME\despliegue-inventario; cd $HOME\despliegue-inventario
Invoke-WebRequest -OutFile sistema-inventario-v1.0.2.zip `
  https://github.com/tal1v4n/sistema-inventario/releases/download/v1.0.2/sistema-inventario-v1.0.2.zip
```

### 3.2 Extraer los archivos

```bash
unzip sistema-inventario-v1.0.2.zip -d version-v1.0.2
```

```powershell
Expand-Archive sistema-inventario-v1.0.2.zip -DestinationPath version-v1.0.2
```

Debe quedar una carpeta `src/` con `producto.py` y `busqueda.py`.

### 3.3 Configuración

El sistema no necesita archivos de configuración, variables de entorno ni base de datos. Los productos se guardan en memoria mientras el programa está abierto.

### 3.4 Ejecutar

```bash
cd version-v1.0.2
python3 src/producto.py
python3 src/busqueda.py
```

En Windows se usa `python` en lugar de `python3`.

Para la v1.1.0 el archivo principal es `src/main.py`:

```bash
python3 src/main.py
```

### 3.5 Comprobar que funciona

- `producto.py` muestra el producto P001 con código, nombre, precio y existencia.
- `busqueda.py` encuentra el producto P002 y muestra las coincidencias de la búsqueda por nombre.
- En v1.1.0, el menú permite registrar un producto (opción 1), verlo en la lista (opción 2) y encontrarlo por código (opción 3).

## 4. Preparar la máquina de destino

### 4.1 Crear la VM

1. En VirtualBox crear una VM con Ubuntu Server (2 GB de RAM y 15 GB de disco son suficientes).
2. Durante la instalación marcar **Install OpenSSH server**.
3. En **Configuración → Red** usar **Adaptador puente** para que la VM tenga una IP de la red local.

### 4.2 Instalar lo necesario

Copiar `deploy/preparar-servidor.sh` a la VM y ejecutarlo:

```bash
bash preparar-servidor.sh
```

El script instala Python, unzip y SSH, crea `~/sistema-inventario` y muestra la IP de la VM.

### 4.3 Crear la llave SSH para GitHub Actions

En la computadora del equipo (no en la VM):

```bash
ssh-keygen -t ed25519 -f deploy_inventario -N "" -C "github-actions"
```

Se generan dos archivos:

- `deploy_inventario.pub`: llave pública. Va en la VM.
- `deploy_inventario`: llave privada. Va en los secretos de GitHub y no se sube al repositorio.

Agregar la llave pública a la VM:

```bash
ssh-copy-id -i deploy_inventario.pub usuario@IP_DE_LA_VM
```

Si `ssh-copy-id` no existe (Windows), pegar el contenido de `deploy_inventario.pub` en `~/.ssh/authorized_keys` dentro de la VM.

Probar la conexión:

```bash
ssh -i deploy_inventario usuario@IP_DE_LA_VM "python3 --version"
```

### 4.4 Hacer que GitHub Actions llegue a la VM

Los runners de GitHub están en internet. Una VM de VirtualBox con IP `192.168.x.x` o `10.0.2.15` no es visible desde ahí. Hay dos caminos:

**Opción A. VM en la nube.** Crear una VM Linux en Azure for Students, AWS u Oracle Cloud con IP pública y el puerto 22 abierto. `DEPLOY_HOST` es esa IP pública. No se necesita nada más.

**Opción B. VM local con Tailscale.** Tailscale crea una red privada entre la VM y el runner.

1. Crear una cuenta gratuita en tailscale.com.
2. En la consola de Tailscale, en **Access controls**, agregar la etiqueta para CI dentro de `tagOwners`:
   ```json
   "tagOwners": { "tag:ci": ["autogroup:admin"] }
   ```
3. En la VM:
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   tailscale ip -4
   ```
   La IP que empieza con `100.` es la que va en `DEPLOY_HOST`.
4. En **Settings → Keys** generar una auth key **Reusable** y **Ephemeral** con la etiqueta `tag:ci`. Se guarda en el secreto `TS_AUTHKEY`.

Los workflows detectan solos si existe `TS_AUTHKEY`. Si existe, conectan el runner a Tailscale antes de usar SSH.

## 5. Secretos en GitHub

En el repositorio: **Settings → Secrets and variables → Actions → New repository secret**.

| Secreto | Valor |
|---|---|
| `DEPLOY_HOST` | IP o nombre del servidor |
| `DEPLOY_USER` | Usuario de la VM |
| `DEPLOY_KEY` | Contenido completo de `deploy_inventario`, incluidas las líneas `BEGIN` y `END` |
| `DEPLOY_PORT` | `22` |
| `TS_AUTHKEY` | Solo en la opción B |

Ninguna contraseña ni llave se escribe en los archivos YAML.

## 6. Despliegue automatizado

Archivo: `.github/workflows/deploy.yml`.

1. Abrir **Actions → Despliegue del Sistema de Inventario → Run workflow**.
2. Escribir la versión (por ejemplo `v1.0.2`) y dejar sin marcar **Simular una falla**.
3. Ejecutar.

Lo que hace el workflow:

1. Valida que la versión tenga formato `vX.Y.Z`.
2. Descarga los scripts de la carpeta `deploy/`.
3. Descarga el paquete de GitHub Releases y muestra su fecha de publicación.
4. Comprueba que el ZIP no esté dañado y lista su contenido.
5. Si hay `TS_AUTHKEY`, se conecta a Tailscale.
6. Transfiere el ZIP y los scripts al servidor por SCP.
7. En el servidor ejecuta `desplegar.sh`, que extrae la versión en su propia carpeta, la activa y la verifica.
8. Muestra el estado final del servidor.

Estructura que queda en el servidor:

```
~/sistema-inventario/
├── actual -> versiones/v1.1.0     enlace a la versión en uso
├── entrantes/                     lo que llega desde GitHub Actions
├── paquetes/                      ZIP de cada versión desplegada (se conservan)
├── versiones/
│   ├── v1.0.2/src/...
│   └── v1.1.0/src/...
├── scripts/                       desplegar, verificar, revertir, estado
├── version-actual
├── version-anterior
└── historial.log
```

## 7. Ejecutar y verificar en el servidor

```bash
ssh -i deploy_inventario usuario@IP_DE_LA_VM
cd ~/sistema-inventario/actual
python3 src/main.py              # v1.1.0
python3 src/producto.py          # v1.0.x
```

Verificación automática:

```bash
bash ~/sistema-inventario/scripts/verificar.sh ~/sistema-inventario/actual
bash ~/sistema-inventario/scripts/estado.sh
```

`verificar.sh` revisa que Python esté instalado, que existan los archivos, que se muestre un producto, que la búsqueda responda y, en v1.1.0, que el menú registre y consulte un producto.

## 8. Publicar la versión v1.1.0

Después de integrar los cambios a `main`:

```bash
git checkout main
git pull
git tag v1.1.0
git push origin v1.1.0
```

El workflow `release.yml` corre las pruebas y publica `sistema-inventario-v1.1.0.zip` en Releases.

## 9. Recuperar una versión anterior

### Recuperación automática

Si la verificación de una versión nueva falla, `desplegar.sh` vuelve a extraer el paquete conservado de la versión anterior, la activa y la verifica. El workflow termina en rojo para que el equipo se entere, pero el sistema queda funcionando.

Para practicarlo: correr el workflow de despliegue con `v1.1.0` y marcar **Simular una falla**. El script borra `src/producto.py` de la copia recién extraída, la verificación falla y se recupera la versión anterior.

### Recuperación desde GitHub Actions

**Actions → Recuperar versión anterior → Run workflow**. Se puede escribir la versión (por ejemplo `v1.0.2`) o dejarlo vacío para regresar a la anterior.

### Recuperación manual en el servidor

```bash
bash ~/sistema-inventario/scripts/revertir.sh v1.0.2
```

Sin scripts, a mano:

```bash
cd ~/sistema-inventario
rm -rf versiones/v1.0.2
unzip -q paquetes/sistema-inventario-v1.0.2.zip -d versiones/v1.0.2
ln -sfn ~/sistema-inventario/versiones/v1.0.2 actual
cd actual && python3 src/producto.py
```

## 10. Problemas frecuentes

| Problema | Causa probable | Solución |
|---|---|---|
| `python3: command not found` | Python no está instalado | `sudo apt install python3` |
| `unzip: command not found` | Falta unzip | `sudo apt install unzip` |
| `release not found` en el workflow | La versión escrita no existe en Releases | Revisar el nombre exacto de la etiqueta |
| `dial tcp ... i/o timeout` | El runner no llega al servidor | Usar IP pública o Tailscale (sección 4.4) |
| `ssh: handshake failed` / `unable to authenticate` | Llave incorrecta o no autorizada | Revisar `DEPLOY_KEY` completo y que la pública esté en `authorized_keys` |
| `Permission denied` al escribir | El usuario no es dueño de la carpeta | `sudo chown -R $USER ~/sistema-inventario` |
| `ModuleNotFoundError: No module named 'producto'` | Falta un archivo o se ejecutó desde otra carpeta | Ejecutar desde la carpeta de la versión con `python3 src/main.py`; si falta el archivo, recuperar la versión |
| `src/main.py: No such file or directory` | La versión activa es v1.0.x | En v1.0.x usar `producto.py` y `busqueda.py` |
| El ZIP está dañado | Descarga incompleta | Volver a correr el workflow; se descarga de nuevo |
