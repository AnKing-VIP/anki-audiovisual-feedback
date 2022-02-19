from .. import theme_name
from ...config import conf, ConfigWindow


def theme_tab(conf_window: ConfigWindow):
    theme = theme_name(__file__)
    tab = conf_window.add_tab(theme)
    tab.checkbox(
        f"themes.{theme}.sound_effect",
        "Play sound effect ",
        "Plays sound effect on answer",
    )
    tab.checkbox(
        f"themes.{theme}.visual_effect",
        "Play visual effect ",
        "Play visual effect on answer",
    )
    tab.checkbox(f"themes.{theme}.colorful_answer_button", "Colorful answer button ")
    tab.stretch()


conf.add_config_tab(theme_tab)
