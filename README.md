# JLC2KiCad - KiCad GUI Plugin

This repository is a simple KiCad plugin GUI wrapper.

## Installation

1. In PCB Editor, open `Tools -> External Plugins -> Open Plugin Directory`.
2. Clone this repository:

```bash
git clone https://github.com/dzid26/JLC2KiCad_lib_gui.git
```

3. Launch Kicad and PCB Editor
On first launch you will be asked to install JLC2KiCadLib in KiCad's Python environment.


4. In KiCad PCB Editor, click `Tools -> External Plugins -> Refresh Plugins`.


## Upgrade JLC2KiCad library

In-app update:

- Open the plugin dialog and click `Check for updates`.


If needed, you can install/update manually, e.g.:

```bash
git pull
"c:/Program Files/KiCad/9.0/bin/python.exe" -m pip install --upgrade JLC2KiCadLib
```
