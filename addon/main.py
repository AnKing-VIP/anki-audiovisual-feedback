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

SOUNDS_DIR = (Path(__file__).parent / "sounds").resolve()


mw.addonManager.setWebExports(__name__, r".*")


def resource_url(resource: str) -> str:
    """resource: relative path from its theme directory"""
    return f"/_addons/{mw.addonManager.addonFromModule(__name__)}/{resource}"


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
    web.body += "<div id='visualFeedback'></div>"
    web.css.append(resource_url("web/reviewer.css"))
    web.js.append(resource_url("web/reviewer.js"))


# Colorful Answer Buttons
###########################


def colorful_span(orig: str, color: str) -> str:
    return f"<span style='color: {color}'>{orig}</span>"


def color_answer_button(
    buttons_tuple: Tuple[Tuple[int, str], ...], reviewer: Reviewer, card: Card
) -> Tuple[Tuple[int, str], ...]:
    if not conf["colorful_answer_button"]:
        return buttons_tuple

    buttons = []
    for button in buttons_tuple:
        ease = Ease.from_num(button[0], len(buttons_tuple))
        if ease == Ease.Again:
            html = colorful_span(button[1], "#f00")
        elif ease == Ease.Hard:
            html = colorful_span(button[1], "#f90")
        elif ease == Ease.Good:
            html = colorful_span(button[1], "#0e0")
        else:
            html = colorful_span(button[1], "#09f")
        buttons.append((button[0], html))
    return tuple(buttons)


# Kitten Rewards
##################


def random_image() -> str:
    """Returns random cat image url"""
    dir = Path(__file__).parent / "images"
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
gui_hooks.reviewer_will_init_answer_buttons.append(color_answer_button)
