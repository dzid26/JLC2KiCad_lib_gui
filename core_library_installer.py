import json
import os
import shutil
import subprocess
import sys
from urllib.request import urlopen

try:
    from importlib.metadata import PackageNotFoundError, version as package_version
except Exception:
    PackageNotFoundError = Exception
    package_version = None


REPO_URL = "https://github.com/dzid26/JLC2KiCad_lib_gui"
CORE_PACKAGE = "JLC2KiCadLib"
PYPI_JSON_URL = f"https://pypi.org/pypi/{CORE_PACKAGE}/json"


def _show_message(message, title, style):
    try:
        import wx
        wx.MessageBox(message, title, style)
    except Exception:
        pass


def show_error(message):
    try:
        import wx
        style = wx.OK | wx.ICON_ERROR
    except Exception:
        style = 0
    _show_message(message, "JLC2KiCad", style)


def show_info(message):
    try:
        import wx
        style = wx.OK | wx.ICON_INFORMATION
    except Exception:
        style = 0
    _show_message(message, "JLC2KiCad", style)


def resolve_python_for_pip():
    exe = sys.executable or ""
    candidates = []

    # Some KiCad builds set sys.executable to kicad.exe, not python.exe.
    if exe:
        candidates.append(exe)
        base_dir = os.path.dirname(exe)
        candidates.extend(
            [
                os.path.join(base_dir, "python.exe"),
                os.path.join(base_dir, "python3.exe"),
                os.path.join(base_dir, "python"),
                os.path.join(base_dir, "python3"),
            ]
        )

    # Prefer known KiCad python locations on Windows.
    candidates.extend(
        [
            r"C:\Program Files\KiCad\9.0\bin\python.exe",
            r"C:\Program Files\KiCad\8.0\bin\python.exe",
        ]
    )

    which_python = shutil.which("python")
    if which_python:
        candidates.append(which_python)

    seen = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        name = os.path.basename(candidate).lower()
        if "kicad" in name:
            continue
        if "python" not in name:
            continue
        if os.path.isfile(candidate) or candidate == which_python:
            return candidate

    return None


def get_core_version():
    if package_version is None:
        return None
    try:
        return package_version(CORE_PACKAGE)
    except PackageNotFoundError:
        return None
    except Exception:
        return None


def get_latest_core_version(timeout=4):
    try:
        with urlopen(PYPI_JSON_URL, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
        data = json.loads(payload)
    except Exception:
        return None
    return data.get("info", {}).get("version")


def install_or_upgrade_core(prompt_reason="update", prompt_user=True):
    try:
        import wx
    except Exception:
        return False

    current_version = get_core_version()
    current_version_label = current_version or "not installed"
    latest_version = get_latest_core_version()

    if prompt_user:
        if prompt_reason == "missing":
            prompt = (
                "JLC2KiCad library is missing.\n\n"
                "Install JLC2KiCadLib now using KiCad's Python environment?"
            )
        else:
            prompt = (
                "Upgrade JLC2KiCad library now?\n"
                f"Current version: {current_version_label}"
            )
            if latest_version:
                prompt += f"\nLatest version: {latest_version}"

        answer = wx.MessageBox(
            prompt,
            "JLC2KiCad GUI Plugin",
            wx.YES_NO | wx.ICON_QUESTION,
        )
        if answer != wx.YES:
            return False

    python_exe = resolve_python_for_pip()
    if not python_exe:
        show_error(
            "Could not find a Python executable for pip.\n\n"
            f"Install manually using README.md or visit:\n{REPO_URL}"
        )
        return False

    cmd = [python_exe, "-m", "pip", "install", "--upgrade", CORE_PACKAGE]
    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as install_error:
        show_error(
            "Automatic install failed.\n"
            f"Reason: {type(install_error).__name__}: {install_error}\n\n"
            f"Install manually using README.md or visit:\n{REPO_URL}"
        )
        return False

    if result.returncode == 0:
        new_version = get_core_version() or current_version_label
        if prompt_reason == "missing":
            show_info(
                f"JLC2KiCad library installed (v{new_version})."
            )
        else:
            if current_version and new_version == current_version:
                show_info(f"JLC2KiCad library is already up to date (v{new_version}).")
            else:
                show_info(
                    "JLC2KiCad library upgraded.\n"
                    f"Version: {current_version_label} -> {new_version}\n"
                    "Restart KiCad to load the new version."
                )
        return True

    stderr_tail = (result.stderr or "").strip()[-600:]
    show_error(
        "Automatic install/update did not complete successfully.\n\n"
        f"pip exit code: {result.returncode}\n"
        f"{stderr_tail}\n\n"
        f"Install manually using README.md or visit:\n{REPO_URL}"
    )
    return False
