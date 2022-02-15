from . import firstrun
from . import config

# Import theme module
from importlib import import_module

from aqt.utils import showWarning
from aqt import mw

theme = mw.addonManager.getConfig(__name__)["theme"]
if "." not in theme:
    import_module(f"{__name__}.themes.{theme}")  # Works with whitespace
else:
    showWarning(
        (
            "<h3>Gamify Anki Add-on Error</h3>"
            "Full stop (.) is not aloowed in theme name."
        ),
        title="Gamify Anki Addon Error",
        textFormat="rich",
    )
