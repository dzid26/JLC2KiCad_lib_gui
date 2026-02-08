from __future__ import print_function
import traceback


try:
    from .JLC2KiCad_gui import JLC2KiCad_GUI
    JLC2KiCad_GUI().register()
except Exception as exc:
    traceback.print_exc()
