from . import firstrun
from .config import conf
from . import main

from importlib import import_module
from aqt.utils import showWarning

theme = conf["theme"]
if "." not in theme:
    import_module(f"{__name__}.user_files.themes.{theme}")  # Works with whitespace
else:
    showWarning(
        (
            "<h3>Gamify Anki Add-on Error</h3>"
            "Full stop (.) is not aloowed in theme name.<br />"
            f"current theme: {conf['theme']}"
        ),
        title="Gamify Anki Addon Error",
        textFormat="rich",
    )
