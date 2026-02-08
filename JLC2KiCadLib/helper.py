import logging
import sys
from importlib.metadata import version as pkg_version


def get_user_agent():
    """Get the User-Agent header for API requests to EasyEDA."""
    try:
        version = pkg_version("JLC2KiCadLib")
    except Exception:
        version = "unknown"
    return f"JLC2KiCadLib/{version} (https://github.com/TousstNicolas/JLC2KiCad_lib)"


def set_logging(logging_level, logging_file):
    LOGGING_FILE = "JLC2KiCad_lib.log"

    if logging_file:
        logging.basicConfig(
            filename=LOGGING_FILE, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
