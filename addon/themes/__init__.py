from pathlib import Path

from aqt import mw
from . import triggers


def resource_url(file: str, resource: str) -> str:
    """
    - file: pass __file__
    - resource: relative path from its theme directory
    """
    script_path = Path(file)
    theme = script_path.relative_to(Path(__file__).parent).parts[0]
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/themes/{theme}/{resource}"


mw.addonManager.setWebExports(__name__, r"themes/.*")
