# Installing RockFace

## What it is for

RockFace Suite is installed from one file per computer. The five programs — Petro, Atlas, Explorer, Lab and MC —
and the `rockface` command line come together, with the AI models (applying them and training them on the processor)
and Mio. From 1.0.0 there is one edition, with AI. The same installation works on a project file and on the team's shared database (server mode).

## Before you start

* **Which file.** The [downloads page](https://github.com/laribeirojr/rockface-releases/releases) (during the testing phase, open to the invited testers signed in to
  GitHub) lists, for each version:

| Computer | File |
|---|---|
| Windows 10 or 11, 64-bit | `RockFace-Suite-<version>-windows-x64-setup.exe` |
| Windows, without installing | `…-windows-x64-portable.zip` |
| macOS 13 or later, Apple silicon (M1–M4) | `…-macos-arm64.dmg` |
| macOS 13 or later, Intel | `…-macos-x86_64.dmg` |
| Linux x86_64 (Ubuntu, Debian, Mint, Fedora, RHEL, Rocky, Alma, openSUSE, Arch, Manjaro…) | `…-linux-x86_64.AppImage` |
| Linux, a plain folder | `…-linux-x86_64.tar.gz` |

* **Earlier versions.** Up to 1.0.0rc3 there were two editions, `RockFace-Suite-…` without AI and
  `RockFace-Suite-AI-…`. Version 1.0.0 installs over either and keeps the preferences. The edition without AI is no
  longer published. In an installed program, **Lab → AI → Hardware and device** tells which device the models use
  on this computer.
* **Space.** About 2 GB.

## Step by step

**Windows**

1. Run the `…-setup.exe`. It installs for your user without administrator rights (or for every user, if you
   choose), after you accept the licence.
2. If Windows SmartScreen says "Windows protected your PC" (the installers are not signed yet): **More info →
   Run anyway**.
3. The Start menu has RockFace Petro, Atlas, Explorer, Lab and MC. Tick **Add the rockface command line to the
   PATH** to use `rockface` in a terminal. Uninstall from Settings → Apps.

**macOS**

1. Open the `.dmg` and drag **RockFace Suite** onto **Applications**.
2. The first time (the installers are not signed with an Apple Developer ID yet): Control-click the app in
   Applications → **Open** → **Open**; on macOS 15 and later, System Settings → **Privacy & Security** → **Open
   Anyway**.
3. The app opens RockFace Petro; Atlas, Explorer, Lab and MC are opened from Petro or from the terminal.

**Linux**

1. Make the AppImage executable and install it in your menu:

```bash
chmod +x RockFace-Suite-*-linux-x86_64.AppImage
./RockFace-Suite-*-linux-x86_64.AppImage --install      # menu entries for the five programs, .rockface files
```

2. Or extract the `.tar.gz` and run its installer, which first offers to install the system libraries that Qt
   needs with your distribution's package manager (apt, dnf, zypper or pacman):

```bash
tar xzf RockFace-Suite-*-linux-x86_64.tar.gz
cd RockFace-Suite-*/ && ./install.sh                     # for your user; sudo ./install.sh for every user
```

3. Open RockFace Petro from the menu, or run `rockface petro` (the installer puts `rockface` in `~/.local/bin`).

**Then, on every system:** run **Help → Run the self-test…** once (see
[Self-test of an installation](selftest.md)).

## Options

| Option | What it does |
|---|---|
| Windows: for me / for every user | Per-user installation (no administrator rights) or in Program Files |
| Windows: desktop icon, command line on the PATH | Both unticked by default |
| Linux `--install` / `--uninstall` (AppImage) | Adds or removes the menu entries, icons and the `.rockface` file type |
| Linux `install.sh --prefix DIR`, `--no-system-packages`, `--uninstall` | Where it goes; skip the package manager; remove it |
| `ROCKFACE_AI_DEVICE` | The device of the AI models (cpu, directml, coreml) for one session |

## How it works

* Each installer carries its own Python and every library: nothing else is installed on the computer, and the
  installed programs do not change a Python installation you may have.
* Every installer carries ONNX Runtime (applying models; on Windows with DirectML, which uses NVIDIA, AMD and Intel
  graphics cards; on macOS with Core ML) and PyTorch for the processor (training). NVIDIA CUDA is not in the
  installers of this version.
* On Linux the AppImage runs on distributions from 2022 on (glibc 2.34 or later: RHEL, Rocky and Alma 9 and newer). Qt needs a few system libraries
  (OpenGL, EGL, fontconfig, xkbcommon, the XCB libraries); desktop distributions have them, and `install.sh`
  installs what is missing with the distribution's own package manager after asking.
* Preferences are kept in the user's folder, so a new version installed over the old one keeps them.
* Every file has a SHA-256 checksum on the downloads page (`SHA256SUMS.txt`): `sha256sum -c SHA256SUMS.txt
  --ignore-missing` on Linux, `shasum -a 256` on macOS, `certutil -hashfile <file> SHA256` on Windows.

## From a script

```python
import rockface.api as rf

print(rf.installation())     # version, installed or from source, edition ("ai" or "standard"), system
```

From a terminal: `rockface --version`, `rockface ai info` (the device and the AI found), `rockface selftest`.

## Limits and common problems

* **macOS: "RockFace-Suite.app is damaged and can't be opened".** The app is not broken: the copies of 1.0.0 and
  1.1.0 carry an incomplete signature, and macOS 15 and 26 refuse such a downloaded app without an *Open Anyway*
  button. Click **Cancel** (not *Move to Trash*), drag the app to **Applications**, open **Terminal** and run:

  ```
  xattr -dr com.apple.quarantine /Applications/RockFace-Suite.app
  ```

  Then open the app as usual. If macOS still refuses it, run also
  `codesign --force --deep --sign - /Applications/RockFace-Suite.app` and open it again. From 1.1.1 the installers
  are signed again after they are built, and this is no longer needed.
* **Linux: "AppImages require FUSE".** Install `libfuse2` (Ubuntu 22.04: `sudo apt install libfuse2`; Ubuntu 24.04
  and later: `sudo apt install libfuse2t64`), or run `./…AppImage --appimage-extract-and-run`, or use the `.tar.gz`.
* **Linux: "could not load the Qt platform plugin xcb".** A system library is missing: run `install.sh` of the
  `.tar.gz` (it installs them), or install `libxcb-cursor0` and `libxkbcommon-x11-0` (Debian, Ubuntu) or
  `xcb-util-cursor` and `libxkbcommon-x11` (Fedora, RHEL, openSUSE, Arch).
* **A server or a computer without a screen.** The command line works without one: `QT_QPA_PLATFORM=offscreen
  rockface selftest`.
* **ARM Linux and 32-bit systems** have no installer in this version.

## Coverage

1.0 (installers for Windows, macOS and Linux; from 1.0.0 one edition, with AI; ROADMAP).
