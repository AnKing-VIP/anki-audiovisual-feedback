import os

from aqt import mw, gui_hooks
from aqt.webview import AnkiWebView
from .themes import triggers

def on_page_rendered(web: AnkiWebView) -> None:
    path = web.page().url().path() # .path() removes "#night"
    name = os.path.basename(path)
    if name == "congrats.html":
        triggers.congrats_page.trigger(web)

gui_hooks.reviewer_did_answer_card.append(triggers.answer_card.trigger)
gui_hooks.webview_did_inject_style_into_page.append(on_page_rendered)