from typing import Callable, Literal, Optional, TypeVar, Generic
import anki
import aqt

Func = TypeVar("Func")

class Trigger(Generic[Func]):
    _func: Optional[Func] = None

    def __call__(self, func: Func):
        self._func = func

    def trigger(self, *args, **kwargs):
        if self._func is not None:
            self._func(*args, **kwargs)


class AnswerCardTrigger(Trigger[Callable[["aqt.reviewer.Reviewer", "anki.cards.Card", Literal[1, 2, 3, 4]], None]]):
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