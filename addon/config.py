from typing import List
from pathlib import Path

from .ankiaddonconfig import ConfigManager, ConfigWindow


def get_themes() -> List[str]:
    themes_dir = Path(__file__).parent / "user_files" / "themes"
    themes = []
    for child in themes_dir.iterdir():
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
    tab.checkbox("review_effect", "During review ")
    tab.checkbox("congrats_effect", "On completing deck ")
    tab.stretch()


conf = ConfigManager()
conf.use_custom_window()
conf.add_config_tab(general_tab)
