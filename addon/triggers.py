from typing import Any, Callable, Literal, Optional, Tuple, TypeVar, Generic, Union
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

    @staticmethod
    def from_num(ease: int, button_count: int) -> "Ease":
        if button_count == 2:
            if ease == 1:
                return Ease.Again
            else:
                return Ease.Good
        elif button_count == 3:
            if ease == 1:
                return Ease.Again
            elif ease == 2:
                return Ease.Good
            else:
                return Ease.Easy
        else:
            if ease == 1:
                return Ease.Again
            elif ease == 2:
                return Ease.Hard
            elif ease == 3:
                return Ease.Good
            else:
                return Ease.Easy


Func = TypeVar("Func")


class Trigger(Generic[Func]):
    _func: Optional[Func] = None

    def __call__(self, func: Func) -> None:
        self._func = func

    def trigger(self, *args: Any, **kwargs: Any) -> None:
        if self._func is not None:
            self._func(*args, **kwargs)  # type: ignore


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
) -> None:
    if isinstance(context, aqt.reviewer.Reviewer):
        reviewer_page.trigger(web)


def _on_answer_card(
    ease_tuple: Tuple[bool, Literal[1, 2, 3, 4]],
    reviewer: "aqt.reviewer.Reviewer",
    card: "anki.cards.Card",
) -> Tuple[bool, Literal[1, 2, 3, 4]]:
    button_count = mw.col.sched.answerButtons(card)
    ease_num = ease_tuple[1]
    ease = Ease.from_num(ease_num, button_count)

    answer_card.trigger(reviewer, card, ease)
    return ease_tuple


gui_hooks.reviewer_will_answer_card.append(_on_answer_card)
gui_hooks.webview_did_inject_style_into_page.append(_on_page_rendered)
gui_hooks.webview_will_set_content.append(_on_webview_set_content)
