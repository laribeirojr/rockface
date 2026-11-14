# Instalar RockFace

## Para qué sirve

RockFace Suite se instala desde un archivo por equipo. Los cinco programas — Petro, Atlas, Explorer, Lab y MC — y
la línea de comandos `rockface` vienen juntos, en una de dos ediciones: **RockFace Suite** (todo salvo las redes
neuronales) y **RockFace Suite AI** (lo mismo, más los modelos de IA: aplicarlos y entrenarlos en el procesador). La
misma instalación trabaja con un archivo de proyecto y con la base de datos compartida del equipo (modo servidor).

## Antes de empezar

* **Qué archivo.** La página de descargas ofrece, para cada versión:

| Equipo | Archivo (RockFace Suite / RockFace Suite AI) |
|---|---|
| Windows 10 u 11, 64 bits | `RockFace-Suite-<versión>-windows-x64-setup.exe` / `RockFace-Suite-AI-…-setup.exe` |
| Windows, sin instalar | `…-windows-x64-portable.zip` |
| macOS 11 o posterior, Apple silicon (M1–M4) | `…-macos-arm64.dmg` |
| macOS 11 o posterior, Intel | `…-macos-x86_64.dmg` |
| Linux x86_64 (Ubuntu, Debian, Mint, Fedora, RHEL, Rocky, Alma, openSUSE, Arch, Manjaro…) | `…-linux-x86_64.AppImage` |
| Linux, una carpeta simple | `…-linux-x86_64.tar.gz` |

* **Qué edición.** Elija **AI** para segmentar con los modelos incluidos, entrenar los suyos y usar las pestañas de
  IA de Lab y MC. Sin IA todo lo demás funciona y el instalador es más pequeño. En un programa instalado, **Lab → IA
  → Hardware y dispositivo…** indica qué edición conviene a este equipo.
* **Espacio.** Cerca de 1 GB para RockFace Suite y 2 GB para RockFace Suite AI.

## Paso a paso

**Windows**

1. Ejecute el `…-setup.exe`. Instala para su usuario sin derechos de administrador (o para todos los usuarios, si
   lo elige), después de que acepte la licencia.
2. Si Windows SmartScreen dice "Windows protegió su PC" (las versiones de prueba aún no están firmadas): **Más
   información → Ejecutar de todas formas**.
3. El menú Inicio tiene RockFace Petro, Atlas, Explorer, Lab y MC. Marque **Añadir la línea de comandos rockface al
   PATH** para usar `rockface` en una terminal. Desinstale en Configuración → Aplicaciones.

**macOS**

1. Abra el `.dmg` y arrastre **RockFace Suite** a **Aplicaciones**.
2. La primera vez (las versiones de prueba aún no están firmadas con un Apple Developer ID): haga clic con Control
   en la aplicación en Aplicaciones → **Abrir** → **Abrir**; en macOS 15 y posteriores, Ajustes del Sistema →
   **Privacidad y seguridad** → **Abrir igualmente**.
3. La aplicación abre RockFace Petro; Atlas, Explorer, Lab y MC se abren desde Petro o desde la terminal.

**Linux**

1. Haga ejecutable el AppImage e instálelo en su menú:

```bash
chmod +x RockFace-Suite-*-linux-x86_64.AppImage
./RockFace-Suite-*-linux-x86_64.AppImage --install      # menu entries for the five programs, .rockface files
```

2. O extraiga el `.tar.gz` y ejecute su instalador, que primero ofrece instalar las bibliotecas del sistema que Qt
   necesita con el gestor de paquetes de su distribución (apt, dnf, zypper o pacman):

```bash
tar xzf RockFace-Suite-*-linux-x86_64.tar.gz
cd RockFace-Suite-*/ && ./install.sh                     # for your user; sudo ./install.sh for every user
```

3. Abra RockFace Petro desde el menú, o ejecute `rockface petro` (el instalador pone `rockface` en `~/.local/bin`).

**Después, en todo sistema:** ejecute una vez **Ayuda → Ejecutar la autoprueba…** (vea
[Autoprueba de una instalación](selftest.md)).

## Opciones

| Opción | Qué hace |
|---|---|
| Windows: solo para mí / para todos los usuarios | Instalación por usuario (sin derechos de administrador) o en Archivos de programa |
| Windows: icono en el escritorio, línea de comandos en el PATH | Ambos desmarcados por defecto |
| Linux `--install` / `--uninstall` (AppImage) | Añade o quita las entradas del menú, los iconos y el tipo de archivo `.rockface` |
| Linux `install.sh --prefix CARPETA`, `--no-system-packages`, `--uninstall` | Dónde instalar; omitir el gestor de paquetes; quitar |
| `ROCKFACE_AI_DEVICE` | El dispositivo de los modelos de IA (cpu, directml, coreml) en una sesión |

## Cómo funciona

* Cada instalador lleva su propio Python y todas las bibliotecas: no se instala nada más en el equipo, y los
  programas instalados no cambian un Python que usted ya tenga.
* La edición AI lleva ONNX Runtime (aplicar modelos; en Windows con DirectML, que usa tarjetas gráficas NVIDIA, AMD
  e Intel; en macOS con Core ML) y PyTorch para el procesador (entrenamiento). NVIDIA CUDA no está en los
  instaladores de esta versión.
* En Linux el AppImage funciona en distribuciones de 2022 en adelante (glibc 2.35 o posterior). Qt necesita algunas
  bibliotecas del sistema (OpenGL, EGL, fontconfig, xkbcommon, las bibliotecas XCB); las distribuciones de
  escritorio ya las tienen, e `install.sh` instala lo que falte con el gestor de paquetes de la propia distribución,
  después de preguntar.
* Las preferencias se guardan en la carpeta del usuario, así que una versión nueva instalada sobre la anterior las
  conserva.
* Cada archivo tiene una suma SHA-256 en la página de descargas (`SHA256SUMS.txt`): `sha256sum -c SHA256SUMS.txt
  --ignore-missing` en Linux, `shasum -a 256` en macOS, `certutil -hashfile <archivo> SHA256` en Windows.

## Desde un script

```python
import rockface.api as rf

print(rf.installation())     # version, installed or from source, edition ("ai" or "standard"), system
```

Desde una terminal: `rockface --version`, `rockface ai info` (el dispositivo y la IA encontrados), `rockface
selftest`.

## Límites y problemas comunes

* **Linux: "AppImages require FUSE".** Instale `libfuse2` (Ubuntu 22.04: `sudo apt install libfuse2`; Ubuntu 24.04
  y posteriores: `sudo apt install libfuse2t64`), o ejecute `./…AppImage --appimage-extract-and-run`, o use el
  `.tar.gz`.
* **Linux: "could not load the Qt platform plugin xcb".** Falta una biblioteca del sistema: ejecute `install.sh` del
  `.tar.gz` (las instala), o instale `libxcb-cursor0` y `libxkbcommon-x11-0` (Debian, Ubuntu) o `xcb-util-cursor` y
  `libxkbcommon-x11` (Fedora, RHEL, openSUSE, Arch).
* **Un servidor o un equipo sin pantalla.** La línea de comandos funciona sin pantalla: `QT_QPA_PLATFORM=offscreen
  rockface selftest`.
* **Linux ARM y los sistemas de 32 bits** no tienen instalador en esta versión.

## Cobertura

1.0 (instaladores para Windows, macOS y Linux, con y sin IA; ROADMAP).
