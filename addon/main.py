from typing import Any, Callable, Iterable, List, Literal, Optional, Tuple, Union
from pathlib import Path
import random
import json
import os

from aqt.reviewer import Reviewer
from anki.cards import Card
from aqt.webview import WebContent, AnkiWebView
from aqt import mw, gui_hooks
from anki.hooks import wrap
import aqt
import anki

from . import audios
from .anking_menu import setup_menu
from .ease import Ease
from .ankiaddonconfig import ConfigManager


conf = ConfigManager()

THEME_DIR: Path = Path(__file__).parent / "user_files" / "themes" / conf["theme"]

mw.addonManager.setWebExports(__name__, r"user_files/themes/.*")

# TODO: maybe refactor these into a class
disableShowAnswer = False  # Hide buttons on bottom bar
isReviewStart = False
intermission_limit = random.randrange(3, 8)
last_did = 0
was_hard = False
last_intermission_sound = None


def resource_url(resource: str) -> str:
    """resource: relative path from its theme directory"""
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/user_files/themes/{conf['theme']}/{resource}"


def maybe_play_audio(name: str) -> Optional[Path]:
    if not conf["sound_effect"]:
        return None
    audio_dir = THEME_DIR / "sounds" / name
    file = random_file(audio_dir)
    if file is not None:
        audios.audio(file)
    return file


def refresh_conf() -> None:
    global THEME_DIR
    conf.load()
    THEME_DIR = Path(__file__).parent / "user_files" / "themes" / conf["theme"]


def has_reviews() -> bool:
    counts = list(mw.col.sched.counts())
    return sum(counts) != 0


def reached_limit_breaker() -> bool:
    limit_breaker = conf["limit_breaker"]
    if (
        limit_breaker
        and was_hard
        and intermission_limit >= limit_breaker
        and has_reviews()
    ):
        return True
    return False


def on_answer_card(
    ease_tuple: Tuple[bool, Literal[1, 2, 3, 4]], reviewer: Reviewer, card: Card
) -> Tuple[bool, Literal[1, 2, 3, 4]]:
    if not conf["review_effect"]:
        return ease_tuple
    button_count = mw.col.sched.answerButtons(card)
    ease_num = ease_tuple[1]
    ease = Ease.from_num(ease_num, button_count)

    if ease == Ease.Again:
        ans = "again"
    elif ease == Ease.Hard:
        ans = "hard"
    elif ease == Ease.Good:
        ans = "good"
    elif ease == Ease.Easy:
        ans = "easy"

    # Play visual effect
    def cb(supports_intermission: bool) -> None:
        global intermission_limit, was_hard, last_intermission_sound
        intermission_limit += 1 if card.queue == 1 else 4 - ease_num
        was_hard = ease_num <= 2
        if supports_intermission and reached_limit_breaker():
            intermission_limit = random.randrange(0, 10)
            last_intermission_sound = maybe_play_audio("break")
            reviewer.web.eval("avfIntermission('%(ans)s');")
        else:
            maybe_play_audio(ans)
            reviewer.web.eval(
                f"if (typeof avfAnswer === 'function') avfAnswer('{ans}')"
            )

    reviewer.web.evalWithCallback("if (typeof avfIntermission === 'function') true", cb)

    return ease_tuple


def on_reviewer() -> None:
    global disableShowAnswer, isReviewStart
    disableShowAnswer = False
    isReviewStart = True


def on_reviewer_web_setup(web: WebContent) -> None:
    global isReviewStart
    refresh_conf()
    if conf["review_effect"]:
        if (THEME_DIR / "web" / "reviewer.css").is_file():
            web.css.append(resource_url("web/reviewer.css"))
        if (THEME_DIR / "web" / "reviewer.js").is_file():
            web.js.append(resource_url("web/reviewer.js"))

    if isReviewStart:
        isReviewStart = False
        if conf["start_effect"]:
            maybe_play_audio("start")
            script = "if (typeof avfReviewStart === 'function') avfReviewStart();"
            web.body += f"<script>{script}</script>"


def files_in_dir(dir: Path) -> Iterable[Path]:
    "Get all files in dir, without automatic hidden files such as '.DS_Store'"
    return filter(
        lambda file: file.name[0] != "."
        and file.name not in ("desktop.ini", "Thumbs.db", "ehthumbs.db", "__MACOSX")
        and file.suffix not in ("sys", "desktop"),
        dir.glob("**/*"),
    )


def random_file(dir: Path) -> Optional[Path]:
    files = list(files_in_dir(dir))
    if len(files) == 0:
        return None
    else:
        return random.choice(files)


def random_file_url(dir: Path) -> Optional[str]:
    """Returns random cat image url"""
    file = random_file(dir)
    if file is None:
        return None

    rel_path = file.relative_to(THEME_DIR)
    return resource_url(f"{str(rel_path)}")


def all_files_url(dir: Path) -> List[str]:
    "May return an empty list"
    return list(
        map(
            lambda file: resource_url(str(file.relative_to(THEME_DIR))),
            files_in_dir(dir),
        )
    )


def on_congrats_page(web: AnkiWebView) -> None:
    refresh_conf()
    if not conf["congrats_effect"]:
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
    maybe_play_audio("congrats")


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

    elif body == "replayIntermissionSound":
        if last_intermission_sound:
            audios.audio(last_intermission_sound)
        return (True, None)

    elif body.startswith("resumeReview#"):
        if not isinstance(context, Reviewer):
            return (False, None)

        answer = body[len("resumeReview#") :]
        audios.force_stop_audio()
        maybe_play_audio(answer)
        context.web.eval(f"if (typeof avfAnswer === 'function') avfAnswer('{answer}')")
        disableShowAnswer = False
        context.bottom.web.eval(
            """document.getElementById("innertable").style.visibility = "visible";"""
        )

        return (True, None)

    else:
        print(f"Invalid pycmd message for Audiovisual Feedback: {body}")

    return handled


def on_state_will_change(new_state: str, old_state: str) -> None:
    audios.force_stop_audio()
    if new_state == "review":
        on_reviewer()

    if not mw.col:
        return

    global last_did, intermission_limit, was_hard
    # Lower limit break when jumping to a different deck
    did = mw.col.decks.selected()
    if did != last_did:
        last_did = did
        intermission_limit = max(4, int(intermission_limit // 1.2))
    was_hard = False


def _on_page_rendered(web: AnkiWebView) -> None:
    path = web.page().url().path()  # .path() removes "#night"
    # "congrats.html" on older versions, "congrats" on v2024.06+
    name = os.path.basename(path)
    name = name.split(".")[0]
    if name == "congrats":
        on_congrats_page(web)


def _on_webview_set_content(
    web: "aqt.webview.WebContent", context: Union[object, None]
) -> None:
    if isinstance(context, aqt.reviewer.Reviewer):
        on_reviewer_web_setup(web)


def patched_reviewer_show_answer(
    reviewer: Reviewer, _old: Callable[[Reviewer], None]
) -> None:
    if disableShowAnswer == False:
        return _old(reviewer)


audios.will_use_audio_player()
gui_hooks.webview_did_receive_js_message.append(on_pycmd)
gui_hooks.state_will_change.append(on_state_will_change)
gui_hooks.reviewer_will_answer_card.append(on_answer_card)
gui_hooks.webview_did_inject_style_into_page.append(_on_page_rendered)
gui_hooks.webview_will_set_content.append(_on_webview_set_content)
Reviewer._showAnswer = wrap(  # type: ignore
    Reviewer._showAnswer, patched_reviewer_show_answer, "around"
)

setup_menu()
