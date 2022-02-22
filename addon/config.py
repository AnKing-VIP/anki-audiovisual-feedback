from .ankiaddonconfig import ConfigManager, ConfigWindow


def general_tab(conf_window: ConfigWindow) -> None:
    tab = conf_window.add_tab("General")
    tab.checkbox(
        "sound_effect",
        "Play sound effect ",
        "Plays sound effect on answer",
    )
    tab.checkbox(
        "visual_effect",
        "Play visual effect ",
        "Play visual effect on answer",
    )
    tab.checkbox("colorful_answer_button", "Colorful answer button ")
    tab.checkbox(
        "kitten_rewards", "Kitten rewards", "Show cat images after finishing deck"
    )
    tab.stretch()


conf = ConfigManager()
conf.use_custom_window()
conf.add_config_tab(general_tab)
