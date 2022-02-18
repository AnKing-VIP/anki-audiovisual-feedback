from typing import Literal
from pathlib import Path

from aqt.reviewer import Reviewer
from anki.cards import Card
from aqt.webview import WebContent

from .. import resource_url, theme_name, triggers, events
from .config import conf

SOUNDS_DIR = (Path(__file__).parent / "sounds").resolve()
THEME_NAME = theme_name(__file__)


def on_answer_card(reviewer: Reviewer, card: Card, ease: Literal[1, 2, 3, 4]):
    if ease == 1:
        ans = "again"
    elif ease == 2:
        ans = "hard"
    elif ease == 3:
        ans = "good"
    elif ease == 4:
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


triggers.reviewer_page(on_reviewer_page)
triggers.answer_card(on_answer_card)
events.will_use_audio_player()
