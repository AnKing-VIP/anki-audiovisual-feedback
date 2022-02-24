from ....config import conf, ConfigWindow  # type: ignore
from ....triggers import Ease  # type: ignore

from typing import Tuple

from aqt import gui_hooks
from aqt.reviewer import Reviewer
from anki.cards import Card


THEME_NAME = __name__.split(".")[-1]
DEFAULT_CONFIGS = {"colorful_answer_button": True}


# Theme Config
#######################


def ensure_config_exists() -> None:
    for config in DEFAULT_CONFIGS:
        config_key = f"themes.{THEME_NAME}.{config}"
        if conf.get(config_key, None) is None:
            conf[config_key] = DEFAULT_CONFIGS[config]


def theme_tab(conf_window: ConfigWindow) -> None:
    tab = conf_window.add_tab(THEME_NAME)
    tab.checkbox(
        f"themes.{THEME_NAME}.colorful_answer_button", "Colorful answer button "
    )
    tab.stretch()


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


ensure_config_exists()
conf.add_config_tab(theme_tab)
gui_hooks.reviewer_will_init_answer_buttons.append(color_answer_button)
