from pathlib import Path

from aqt import mw
from .triggers import Ease


def resource_url(file: str, resource: str) -> str:
    """
    - file: __file__
    - resource: relative path from its theme directory
    """
    theme = theme_name(file)
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/themes/{theme}/{resource}"


def theme_name(file: str) -> str:
    """
    - file: __file__
    """
    script_path = Path(file)
    return script_path.relative_to(Path(__file__).parent).parts[0]


mw.addonManager.setWebExports(__name__, r"themes/.*")
