from aqt import mw

def resourse_url(file: str) -> str:
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/themes/{file}"

mw.addonManager.setWebExports(__name__, r"themes/.*")