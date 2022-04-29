from typing import List
from pathlib import Path

from aqt.qt import QPushButton
from aqt.utils import openFolder

from .ankiaddonconfig import ConfigManager, ConfigWindow

THEMES_DIR = Path(__file__).parent / "user_files" / "themes"


def open_theme_dir() -> None:
    theme_dir = THEMES_DIR / conf["theme"]
    openFolder(theme_dir)


def get_themes() -> List[str]:
    themes = []
    for child in THEMES_DIR.iterdir():
        if child.is_dir():
            themes.append(child.name)
    return themes


def general_tab(conf_window: ConfigWindow) -> None:
    conf_window.resize(400, 200)

    tab = conf_window.add_tab("General")

    themes = get_themes()
    tab.dropdown("theme", themes, themes, "Theme:", "Choose a gamification theme")

    tab.checkbox(
        "sound_effect",
        "Play sound effect ",
    )
    tab.checkbox("start_effect", "On review start ")
    tab.checkbox("review_effect", "During review ")
    tab.checkbox("congrats_effect", "On completing deck ")

    btn_lay = tab.hlayout()
    btn = QPushButton("Open Theme Folder")
    btn.clicked.connect(lambda _: open_theme_dir())
    btn.setToolTip(
        "You can customize themes by modifying files in the theme directory."
    )
    btn_lay.addWidget(btn)
    btn_lay.stretch()

    tab.stretch()


conf = ConfigManager()
conf.use_custom_window()
conf.add_config_tab(general_tab)
