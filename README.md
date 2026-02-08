# JLC2KiCad - KiCad GUI Plugin

This repository is a simple KiCad plugin GUI wrapper.

## Installation

1. In PCB Editor, open `Tools -> External Plugins -> Open Plugin Directory`.
2. Clone this repository:

```bash
git clone https://github.com/dzid26/JLC2KiCad_lib_gui.git
```

3. Install the core library into KiCad's Python:

```bash
"c:/Program Files/KiCad/9.0/bin/python.exe" -m pip install JLC2KiCadLib
```

4. In KiCad, run `Tools -> External Plugins -> Refresh Plugins`.

## Update

When updating the plugin repo:

```bash
git pull
"c:/Program Files/KiCad/9.0/bin/python.exe" -m pip install --upgrade JLC2KiCadLib
```
