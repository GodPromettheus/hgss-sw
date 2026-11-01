# Windows graphical builder

The window is a local front end for `tools/switch/build_game.sh`. It needs the
repository checkout and the Linux build environment used by that script.
It does not install system packages or download ROMs.

## Requirements

- Windows 10/11 with WSL2 and Ubuntu 24.04.
- In Ubuntu: Git, CMake, Ninja, Python 3, and devkitPro's `switch-dev` and
  `switch-sdl2` packages. Docker with the official devkitPro image can be used
  instead of a local devkitPro toolchain.
- Python 3 with Tk support on Windows.

Install the Ubuntu packages and devkitPro using the instructions linked from
the main project build guide. Start Ubuntu once after installing WSL.

## Open the window

From the root of this repository in PowerShell:

```powershell
py tools/switch/windows_builder.py
```

Choose a supported game or package, select your own `.nds` file, and click
**Gerar arquivos do Switch**. The window calls WSL and displays the build log.

Supported choices:

- SoulSilver + HeartGold: supply a US SoulSilver ROM.
- Black 2, White 2, Black, or White: supply that game's supported English ROM.
- All six games: supply a US SoulSilver ROM.

The generated SD-card folder is `build-sd/switch/` under this checkout. Copy
the resulting folder to your SD card, then place the ROMs in the locations
shown by the project's README. The builder does not include ROMs in its output.

## Local data and project scope

The selected ROM is read from its existing path by WSL. It is not uploaded by
the builder. The repository ignores `*.nds`, generated source in `gen/`,
build directories, and `build-sd/`; keep all ROM-derived output on your own
computer and do not force-add ignored files to Git.

A private directory cannot be created inside a public GitHub repository. This
GUI source and its instructions are generic public project files. ROMs and
build output stay local.

This builds the project's current Switch homebrew implementation, which uses
the melonDS core. It does not create a native port that removes melonDS.
