from __future__ import print_function
import pprint
import sys
import traceback


def _show_load_error(message):
    try:
        import wx
        wx.MessageBox(message, "JLC2KiCad Plugin Load Error", wx.OK | wx.ICON_ERROR)
    except Exception:
        pass


try:
    print("Starting JLC2KiCad_GUI")
    from .JLC2KiCad_gui import JLC2KiCad_GUI
    JLC2KiCad_GUI().register()
except Exception as e:
    traceback.print_exc(file=sys.stdout)
    error_hint = ""
    if isinstance(e, ModuleNotFoundError):
        error_hint = (
            "Core library missing.\n"
            "Install JLC2KiCadLib in KiCad Python.\n\n"
        )
        print(error_hint.strip())

    _show_load_error(
        f"{error_hint}Exception: {type(e).__name__}: {e}\n\n"
        "Check KiCad Scripting Console for full traceback."
    )
    pprint.pprint(e)
