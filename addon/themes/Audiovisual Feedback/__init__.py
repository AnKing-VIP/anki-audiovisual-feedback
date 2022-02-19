from typing import Literal, Tuple
from pathlib import Path

from aqt.reviewer import Reviewer
from anki.cards import Card
from aqt.webview import WebContent
from aqt import gui_hooks

from .. import resource_url, theme_name, triggers, events, Ease
from .config import conf

SOUNDS_DIR = (Path(__file__).parent / "sounds").resolve()
THEME_NAME = theme_name(__file__)


def on_answer_card(reviewer: Reviewer, card: Card, ease: Ease):
    if ease == Ease.Again:
        ans = "again"
    elif ease == Ease.Hard:
        ans = "hard"
    elif ease == Ease.Good:
        ans = "good"
    elif ease == Ease.Easy:
        ans = "easy"

    # Play sound effect
    if conf[f"themes.{THEME_NAME}.sound_effect"]:
        audio_file = SOUNDS_DIR / f"{ans}.m4a"
        events.audio(audio_file)

    # Play visual effect
    if conf[f"themes.{THEME_NAME}.visual_effect"]:
        reviewer.web.eval(f"showVisualFeedback('{ans}')")


def on_reviewer_page(web: WebContent):
    conf.load()
    web.body += "<div id='visualFeedback'></div>"
    web.css.append(resource_url(__file__, "style.css"))
    web.js.append(resource_url(__file__, "script.js"))


def colorful_span(orig: str, color: str) -> str:
    return f"<span style='color: {color}'>{orig}</span>"


def color_answer_button(
    buttons_tuple: Tuple[Tuple[int, str], ...], reviewer: Reviewer, card: Card
) -> Tuple[Tuple[int, str], ...]:
    if not conf[f"themes.{THEME_NAME}.colorful_answer_button"]:
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


triggers.reviewer_page(on_reviewer_page)
triggers.answer_card(on_answer_card)
events.will_use_audio_player()

gui_hooks.reviewer_will_init_answer_buttons.append(color_answer_button)
