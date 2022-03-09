from typing import Any, Callable, List, Tuple
from pathlib import Path
import random
import json

from aqt.reviewer import Reviewer
from anki.cards import Card
from aqt.webview import WebContent, AnkiWebView
from aqt import mw, gui_hooks
from anki.hooks import wrap


from . import events, triggers
from .triggers import Ease
from .config import conf

THEME_DIR: Path = Path(__file__).parent / "user_files" / "themes" / conf["theme"]


mw.addonManager.setWebExports(__name__, r"user_files/themes/.*")

disableShowAnswer = False


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
        audio_dir = THEME_DIR / "sounds" / ans
        events.audio(random_file(audio_dir))

    # Play visual effect
    if conf["visual_effect"]:
        reviewer.web.eval(f"showVisualFeedback('{ans}')")


def on_reviewer_page(web: WebContent) -> None:
    conf.load()
    web.css.append(resource_url("web/reviewer.css"))
    web.js.append(resource_url("web/reviewer.js"))


def random_file(dir: Path) -> Path:
    files = list(dir.glob("**/*"))
    return random.choice(files)


def random_file_url(dir: Path) -> str:
    """Returns random cat image url"""
    files = list(dir.glob("**/*"))
    file = random.choice(files)
    rel_path = file.relative_to(THEME_DIR)
    return resource_url(f"{str(rel_path)}")


def all_files_url(dir: Path) -> List[str]:
    files = list(
        map(
            lambda file: resource_url(str(file.relative_to(THEME_DIR))),
            dir.glob("**/*"),
        )
    )
    return files


def on_congrats(web: AnkiWebView) -> None:
    """Insert cat image onto Congrats page"""
    dir = THEME_DIR / "images" / "congrats"
    if not dir.is_dir():
        return

    css_file = THEME_DIR / "web" / "congrats.css"
    if css_file.is_file():
        # Sometimes this function is triggered twice.
        # So check if it has already been run by checking if element already exist
        web.eval(
            """
            (() => {
                const id = "audiovisualFeedbackStyle"
                if (document.getElementById(id)) { return }

                const style = document.createElement("link")
                style.id = id
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
                const id = "audiovisualFeedbackScript"
                if (document.getElementById(id)) { return }
                  
                const script = document.createElement("script")
                script.id = id
                script.src = `%s`
                document.head.appendChild(script)
            })()
            """
            % resource_url("web/congrats.js")
        )
    audio_dir = THEME_DIR / "sounds" / "congrats"
    if audio_dir.is_dir():
        events.audio(random_file(audio_dir))


def on_pycmd(handled: Tuple[bool, Any], message: str, context: Any) -> Tuple[bool, Any]:
    global disableShowAnswer

    addon_key = "audiovisualFeedback#"
    if not message.startswith(addon_key):
        return handled

    body = message[len(addon_key) :]
    if body.startswith("randomFile#"):
        path = body[len("randomFile#") :]
        return (True, random_file_url(THEME_DIR / path))

    elif body.startswith("files#"):
        path = body[len("files#") :]
        value = all_files_url(THEME_DIR / path)
        return (True, json.dumps(value))

    elif body == "disableShowAnswer":
        if not isinstance(context, Reviewer):
            return (False, None)

        disableShowAnswer = True
        context.bottom.web.eval(
            """document.getElementById("innertable").style.visibility = "hidden";"""
        )
        return (True, None)

    elif body == "enableShowAnswer":
        if not isinstance(context, Reviewer):
            return (False, None)

        disableShowAnswer = False
        context.bottom.web.eval(
            """document.getElementById("innertable").style.visibility = "visible";"""
        )
        return (True, None)
    else:
        print(f"Invalid pycmd message for Audiovisual Feedback: {body}")

    return handled


def patched_reviewer_show_answer(
    reviewer: Reviewer, _old: Callable[[Reviewer], None]
) -> None:
    if disableShowAnswer == False:
        return _old(reviewer)


def on_state_will_change(new_state: str, old_state: str) -> None:
    """Reset disableShowAnswer when starting a review session."""
    global disableShowAnswer
    if new_state == "review":
        disableShowAnswer = False


gui_hooks.webview_did_receive_js_message.append(on_pycmd)
gui_hooks.state_will_change.append(on_state_will_change)
events.will_use_audio_player()
triggers.answer_card(on_answer_card)
triggers.reviewer_page(on_reviewer_page)
triggers.congrats_page(on_congrats)

Reviewer._showAnswer = wrap(  # type: ignore
    Reviewer._showAnswer, patched_reviewer_show_answer, "around"
)
