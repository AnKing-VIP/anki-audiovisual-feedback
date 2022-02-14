# firstrun.py v1.1

from typing import Type
from pathlib import Path
import os

from aqt import mw

from .compat import compat


VERSION_ENV_VAR = "GAMIFY_ANKI_VERSION"

config = mw.addonManager.getConfig(__name__)


class Version:
    @classmethod
    def from_string(cls: Type["Version"], ver_str: str) -> "Version":
        ver = [int(i) for i in ver_str.split(".")]
        version = Version(from_config=False)
        version.set_version(ver[0], ver[1])
        return version

    def __init__(self, from_config: bool = True) -> None:
        if from_config:
            self.load()

    def load(self) -> None:
        self.set_version(config["version"]["major"], config["version"]["minor"])

    def set_version(self, major: int, minor: int) -> None:
        self.major = major
        self.minor = minor

    def __eq__(self, other: str) -> bool:  # type: ignore
        ver = [int(i) for i in other.split(".")]
        return self.major == ver[0] and self.minor == ver[1]

    def __gt__(self, other: str) -> bool:
        ver = [int(i) for i in other.split(".")]
        return self.major > ver[0] or (self.major == ver[0] and self.minor > ver[1])

    def __lt__(self, other: str) -> bool:
        ver = [int(i) for i in other.split(".")]
        return self.major < ver[0] or (self.major == ver[0] and self.minor < ver[1])

    def __ge__(self, other: str) -> bool:
        return self == other or self > other

    def __le__(self, other: str) -> bool:
        return self == other or self < other


def save_current_version_to_conf() -> None:
    # For debugging
    version_string = os.environ.get(VERSION_ENV_VAR)
    if not version_string:
        version_file = Path(__file__).parent / "VERSION"
        version_string = version_file.read_text()
    if version_string != prev_version:
        config["version"]["major"] = int(version_string.split(".")[0])
        config["version"]["minor"] = int(version_string.split(".")[1])
        mw.addonManager.writeConfig(__name__, config)


# version of the add-on prior to running this script
prev_version = Version()

save_current_version_to_conf()

compat(prev_version)
