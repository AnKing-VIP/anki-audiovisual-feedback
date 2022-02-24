from typing import Tuple
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
    web.css.append(resource_url("reviewer.css"))
    web.js.append(resource_url("reviewer.js"))


# Kitten Rewards
##################


def random_image() -> str:
    """Returns random cat image url"""
    dir = Path(__file__).parent / "user_files" / "themes" / conf["theme"] / "images"
    files = list(dir.glob("**/*"))
    file = random.choice(files)
    rel_path = file.relative_to(dir)
    return resource_url(f"images/{str(rel_path)}")


def on_congrats(web: AnkiWebView) -> None:
    """Insert cat image onto Congrats page"""
    if not conf["kitten_rewards"]:
        return

    image_url = random_image()
    html = (
        """
<div id="cat-container">
    <img id="cat-image" src="%s">
</div>
    """
        % image_url
    )
    style = """
#cat-container {
    display: flex;
    justify-content: center;
}
#cat-image {
    max-width: 30em;
    margin: auto 0;
}
    """

    events.add_style(web, style)
    events.add_html(web, html, to="top")


events.will_use_audio_player()
triggers.answer_card(on_answer_card)
triggers.reviewer_page(on_reviewer_page)
triggers.congrats_page(on_congrats)
