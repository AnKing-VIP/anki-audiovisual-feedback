from typing import Callable, Literal, Optional, TypeVar, Generic, Union
import os

import anki
import aqt
from aqt import gui_hooks

Func = TypeVar("Func")


class Trigger(Generic[Func]):
    _func: Optional[Func] = None

    def __call__(self, func: Func):
        self._func = func

    def trigger(self, *args, **kwargs):
        if self._func is not None:
            self._func(*args, **kwargs)


class AnswerCardTrigger(
    Trigger[
        Callable[
            ["aqt.reviewer.Reviewer", "anki.cards.Card", Literal[1, 2, 3, 4]], None
        ]
    ]
):
    """When answering(rating) card.
    # Arguments
    reviewer, card, ease (1,2,3,4)
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


gui_hooks.reviewer_did_answer_card.append(answer_card.trigger)
gui_hooks.webview_did_inject_style_into_page.append(_on_page_rendered)
gui_hooks.webview_will_set_content.append(_on_webview_set_content)
