from typing import Any, Tuple
from pathlib import Path
import random

from aqt.reviewer import Reviewer
from anki.cards import Card
from aqt.webview import WebContent, AnkiWebView
from aqt import mw, gui_hooks


from . import events, triggers
from .triggers import Ease
from .config import conf

THEME_DIR: Path = Path(__file__).parent / "user_files" / "themes" / conf["theme"]
SOUNDS_DIR = THEME_DIR / "sounds"


mw.addonManager.setWebExports(__name__, r"user_files/themes/.*")


def resource_url(resource: str) -> str:
    """resource: relative path from its theme directory"""
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/user_files/themes/{conf['theme']}/{resource}"


def on_answer_card(reviewer: Reviewer, card: Card, ease: Ease) -> None:
    if ease == Ease.Again:
        ans = "again"
    elif ease == Ease.Hard:
        ans = "hard"
    elif ease == Ease.Good:
        ans = "good"
    elif ease == Ease.Easy:
        ans = "easy"

    # Play sound effect
    if conf["sound_effect"]:
        audio_file = SOUNDS_DIR / f"{ans}.m4a"
        events.audio(audio_file)

    # Play visual effect
    if conf["visual_effect"]:
        reviewer.web.eval(f"showVisualFeedback('{ans}')")


def on_reviewer_page(web: WebContent) -> None:
    conf.load()
    web.css.append(resource_url("web/reviewer.css"))
    web.js.append(resource_url("web/reviewer.js"))


# Kitten Rewards
##################


def random_file_url(dir: Path) -> str:
    """Returns random cat image url"""
    files = list(dir.glob("**/*"))
    file = random.choice(files)
    rel_path = file.relative_to(THEME_DIR)
    return resource_url(f"{str(rel_path)}")


def on_congrats(web: AnkiWebView) -> None:
    """Insert cat image onto Congrats page"""
    dir = THEME_DIR / "images" / "congrats"
    if not dir.is_dir():
        return

    css_file = THEME_DIR / "web" / "congrats.css"
    if css_file.is_file():
        web.eval(
            """
                (() => {
                const style = document.createElement("link")
                style.rel = "stylesheet"
                style.type = "text/css"
                style.href = `%s`
                document.head.appendChild(style)
            })()
            """
            % resource_url("web/congrats.css")
        )

    js_file = THEME_DIR / "web" / "congrats.js"
    if js_file.is_file():
        web.eval(
            """
                (() => {
                const script = document.createElement("script")
                script.src = `%s`
                document.head.appendChild(script)
            })()
            """
            % resource_url("web/congrats.js")
        )


def on_pycmd(handled: Tuple[bool, Any], message: str, context: Any) -> Tuple[bool, Any]:
    addon_key = "audiovisualFeedback#"
    if not message.startswith(addon_key):
        return handled

    body = message[len(addon_key) :]
    if body.startswith("randomFile#"):
        path = body[len("randomFile#") :]
        value = random_file_url(THEME_DIR / path)
        print("randomFile")
        print(value)
        return (True, value)

    return handled


gui_hooks.webview_did_receive_js_message.append(on_pycmd)
events.will_use_audio_player()
triggers.answer_card(on_answer_card)
triggers.reviewer_page(on_reviewer_page)
triggers.congrats_page(on_congrats)
