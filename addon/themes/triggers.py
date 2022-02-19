from typing import Callable, Literal, Optional, Tuple, TypeVar, Generic, Union
from enum import Enum
import os

import anki
import aqt
from aqt import gui_hooks, mw


class Ease(Enum):
    Again = 1
    Hard = 2
    Good = 3
    Easy = 4


Func = TypeVar("Func")


class Trigger(Generic[Func]):
    _func: Optional[Func] = None

    def __call__(self, func: Func):
        self._func = func

    def trigger(self, *args, **kwargs):
        if self._func is not None:
            self._func(*args, **kwargs)


class AnswerCardTrigger(
    Trigger[Callable[["aqt.reviewer.Reviewer", "anki.cards.Card", Ease], None]]
):
    """When answering(rating) card.
    # Arguments
    reviewer, card, ease
    """

    pass


answer_card = AnswerCardTrigger()


class CongratsPageTrigger(Trigger[Callable[["aqt.webview.AnkiWebView"], None]]):
    """Triggered when in congrats page
    # Arguments
    webview
    """

    pass


congrats_page = CongratsPageTrigger()


class ReviewerPageTrigger(Trigger[Callable[["aqt.webview.WebContent"], None]]):
    """Triggered when reviewer web is loaded.
    Anki reloads its webview every ~1000 reviews,
    so it may be called multiple times during single review session.

    # Arguments
    webview
    """

    pass


reviewer_page = ReviewerPageTrigger()


# Trigger the above triggers
############################


def _on_page_rendered(web: "aqt.webview.AnkiWebView") -> None:
    path = web.page().url().path()  # .path() removes "#night"
    name = os.path.basename(path)
    if name == "congrats.html":
        congrats_page.trigger(web)


def _on_webview_set_content(
    web: "aqt.webview.WebContent", context: Union[object, None]
):
    if isinstance(context, aqt.reviewer.Reviewer):
        reviewer_page.trigger(web)


def _on_answer_card(
    ease_tuple: Tuple[bool, Literal[1, 2, 3, 4]],
    reviewer: "aqt.reviewer.Reviewer",
    card: "anki.card.Card",
) -> Tuple[bool, Literal[1, 2, 3, 4]]:
    button_count = mw.col.sched.answerButtons(card)
    ease_num = ease_tuple[1]
    if button_count == 2:
        if ease_num == 1:
            ease = Ease.Again
        else:
            ease = Ease.Good
    elif button_count == 3:
        if ease_num == 1:
            ease = Ease.Again
        elif ease_num == 2:
            ease = Ease.Good
        else:
            ease = Ease.Easy
    else:
        if ease_num == 1:
            ease = Ease.Again
        elif ease_num == 2:
            ease = Ease.Hard
        elif ease_num == 3:
            ease = Ease.Good
        else:
            ease = Ease.Easy

    answer_card.trigger(reviewer, card, ease)

    return ease_tuple


gui_hooks.reviewer_will_answer_card.append(_on_answer_card)
gui_hooks.webview_did_inject_style_into_page.append(_on_page_rendered)
gui_hooks.webview_will_set_content.append(_on_webview_set_content)
