from typing import List
from pathlib import Path
from .ankiaddonconfig import ConfigManager, ConfigWindow


def get_themes() -> List[str]:
    themes_dir = Path(__file__).parent / "themes"
    themes = []
    for child in themes_dir.iterdir():
        if child.is_dir():
            themes.append(child.name)
    return themes


# Main Config Window UI Code
############################


def setup_window(conf_window: ConfigWindow):
    conf_window.set_footer("Restart Anki for the changes to take effect")


def general_tab(conf_window: ConfigWindow):
    tab = conf_window.add_tab("General")

    themes = get_themes()
    tab.dropdown("theme", themes, themes, "Theme:", "Choose a gamification theme")
    tab.stretch()


conf = ConfigManager()
conf.use_custom_window()
conf.add_config_tab(general_tab)
conf.on_window_open(setup_window)
