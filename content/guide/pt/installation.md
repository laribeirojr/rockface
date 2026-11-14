# Instalando o RockFace

## Para que serve

O RockFace Suite é instalado a partir de um arquivo por computador. Os cinco programas — Petro, Atlas, Explorer,
Lab e MC — e a linha de comando `rockface` vêm juntos, numa de duas edições: **RockFace Suite** (tudo menos as redes
neurais) e **RockFace Suite AI** (o mesmo, mais os modelos de IA: aplicá-los e treiná-los no processador). A mesma
instalação trabalha num arquivo de projeto e no banco de dados compartilhado da equipe (modo servidor).

## Antes de começar

* **Qual arquivo.** A página de downloads traz, para cada versão:

| Computador | Arquivo (RockFace Suite / RockFace Suite AI) |
|---|---|
| Windows 10 ou 11, 64 bits | `RockFace-Suite-<versão>-windows-x64-setup.exe` / `RockFace-Suite-AI-…-setup.exe` |
| Windows, sem instalar | `…-windows-x64-portable.zip` |
| macOS 11 ou mais novo, Apple silicon (M1–M4) | `…-macos-arm64.dmg` |
| macOS 11 ou mais novo, Intel | `…-macos-x86_64.dmg` |
| Linux x86_64 (Ubuntu, Debian, Mint, Fedora, RHEL, Rocky, Alma, openSUSE, Arch, Manjaro…) | `…-linux-x86_64.AppImage` |
| Linux, uma pasta simples | `…-linux-x86_64.tar.gz` |

* **Qual edição.** Escolha **AI** para segmentar com os modelos que vêm com o programa, treinar os seus e usar as
  abas de IA do Lab e do MC. Sem IA, todo o resto funciona e o instalador é menor. Num programa instalado, **Lab →
  IA → Hardware e dispositivo…** diz qual edição serve para este computador.
* **Espaço.** Cerca de 1 GB para o RockFace Suite e 2 GB para o RockFace Suite AI.

## Passo a passo

**Windows**

1. Execute o `…-setup.exe`. Ele instala para o seu usuário sem direitos de administrador (ou para todos os usuários,
   se você escolher), depois que você aceita a licença.
2. Se o Windows SmartScreen disser "O Windows protegeu o computador" (as versões de teste ainda não são
   assinadas): **Mais informações → Executar assim mesmo**.
3. O menu Iniciar tem RockFace Petro, Atlas, Explorer, Lab e MC. Marque **Adicionar a linha de comando rockface ao
   PATH** para usar `rockface` num terminal. Desinstale em Configurações → Aplicativos.

**macOS**

1. Abra o `.dmg` e arraste **RockFace Suite** para **Aplicativos**.
2. Na primeira vez (as versões de teste ainda não são assinadas com um Apple Developer ID): clique com Control no
   aplicativo em Aplicativos → **Abrir** → **Abrir**; no macOS 15 e mais novos, Ajustes do Sistema → **Privacidade e
   Segurança** → **Abrir Mesmo Assim**.
3. O aplicativo abre o RockFace Petro; Atlas, Explorer, Lab e MC são abertos pelo Petro ou pelo terminal.

**Linux**

1. Torne o AppImage executável e instale-o no seu menu:

```bash
chmod +x RockFace-Suite-*-linux-x86_64.AppImage
./RockFace-Suite-*-linux-x86_64.AppImage --install      # menu entries for the five programs, .rockface files
```

2. Ou extraia o `.tar.gz` e execute o instalador dele, que primeiro oferece instalar as bibliotecas do sistema de
   que o Qt precisa com o gerenciador de pacotes da sua distribuição (apt, dnf, zypper ou pacman):

```bash
tar xzf RockFace-Suite-*-linux-x86_64.tar.gz
cd RockFace-Suite-*/ && ./install.sh                     # for your user; sudo ./install.sh for every user
```

3. Abra o RockFace Petro pelo menu, ou execute `rockface petro` (o instalador põe `rockface` em `~/.local/bin`).

**Depois, em todo sistema:** execute uma vez **Ajuda → Executar o autoteste…** (veja
[Autoteste de uma instalação](selftest.md)).

## Opções

| Opção | O que faz |
|---|---|
| Windows: só para mim / para todos os usuários | Instalação por usuário (sem direitos de administrador) ou em Arquivos de Programas |
| Windows: ícone na área de trabalho, linha de comando no PATH | Ambos desmarcados por padrão |
| Linux `--install` / `--uninstall` (AppImage) | Adiciona ou remove as entradas do menu, os ícones e o tipo de arquivo `.rockface` |
| Linux `install.sh --prefix PASTA`, `--no-system-packages`, `--uninstall` | Onde instalar; pular o gerenciador de pacotes; remover |
| `ROCKFACE_AI_DEVICE` | O dispositivo dos modelos de IA (cpu, directml, coreml) numa sessão |

## Como funciona

* Cada instalador leva o seu próprio Python e todas as bibliotecas: nada mais é instalado no computador, e os
  programas instalados não mudam um Python que você já tenha.
* A edição AI leva o ONNX Runtime (aplicar modelos; no Windows com o DirectML, que usa placas de vídeo NVIDIA, AMD e
  Intel; no macOS com o Core ML) e o PyTorch para o processador (treinamento). O NVIDIA CUDA não está nos
  instaladores desta versão.
* No Linux o AppImage roda em distribuições de 2022 em diante (glibc 2.35 ou mais nova). O Qt precisa de algumas
  bibliotecas do sistema (OpenGL, EGL, fontconfig, xkbcommon, as bibliotecas XCB); as distribuições de desktop já as
  têm, e o `install.sh` instala o que faltar com o gerenciador de pacotes da própria distribuição, depois de
  perguntar.
* As preferências ficam na pasta do usuário, de modo que uma versão nova instalada sobre a antiga as mantém.
* Cada arquivo tem uma soma SHA-256 na página de downloads (`SHA256SUMS.txt`): `sha256sum -c SHA256SUMS.txt
  --ignore-missing` no Linux, `shasum -a 256` no macOS, `certutil -hashfile <arquivo> SHA256` no Windows.

## Por script

```python
import rockface.api as rf

print(rf.installation())     # version, installed or from source, edition ("ai" or "standard"), system
```

Num terminal: `rockface --version`, `rockface ai info` (o dispositivo e a IA encontrados), `rockface selftest`.

## Limites e problemas comuns

* **Linux: "AppImages require FUSE".** Instale o `libfuse2` (Ubuntu 22.04: `sudo apt install libfuse2`; Ubuntu
  24.04 e mais novos: `sudo apt install libfuse2t64`), ou execute `./…AppImage --appimage-extract-and-run`, ou use o
  `.tar.gz`.
* **Linux: "could not load the Qt platform plugin xcb".** Falta uma biblioteca do sistema: execute o `install.sh` do
  `.tar.gz` (ele as instala), ou instale `libxcb-cursor0` e `libxkbcommon-x11-0` (Debian, Ubuntu) ou
  `xcb-util-cursor` e `libxkbcommon-x11` (Fedora, RHEL, openSUSE, Arch).
* **Um servidor ou um computador sem tela.** A linha de comando funciona sem tela: `QT_QPA_PLATFORM=offscreen
  rockface selftest`.
* **Linux ARM e sistemas de 32 bits** não têm instalador nesta versão.

## Cobertura

1.0 (instaladores para Windows, macOS e Linux, com e sem IA; ROADMAP).
