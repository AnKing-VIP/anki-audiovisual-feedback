from pathlib import Path
from typing import Literal, Union

from aqt import mw, gui_hooks
from aqt.webview import AnkiWebView, WebContent
import aqt.sound

try:  # 2.1.50+
    from anki.utils import is_win
except:
    from anki.utils import isWin as is_win

audio_player = None


def _setup_audio_player():
    """Create and setup an audio player.
    Call after collection is loaded

    Modified from aqt.sound.setup_audio
    """
    global audio_player
    audio_player = aqt.sound.AVPlayer()

    taskman = mw.taskman
    base_folder = mw.pm.base
    media_folder = mw.col.media.dir()

    try:
        try:  # 2.1.50+
            mpvManager = aqt.sound.MpvManager(base_folder, media_folder)
        except TypeError:
            mpvManager = aqt.sound.MpvManager(base_folder)
    except FileNotFoundError:
        print("mpv not found, reverting to mplayer")
    except aqt.mpv.MPVProcessError:
        print("mpv too old, reverting to mplayer")

    if mpvManager is not None:
        audio_player.players.append(mpvManager)

        if is_win:
            try:  # 2.1.50+
                mpvPlayer = aqt.sound.SimpleMpvPlayer(
                    taskman, base_folder, media_folder
                )
            except TypeError:
                mpvPlayer = aqt.sound.SimpleMpvPlayer(taskman, base_folder)
            audio_player.players.append(mpvPlayer)
    else:
        try:
            mplayer = aqt.sound.SimpleMplayerSlaveModePlayer(taskman, media_folder)
        except TypeError:  # 2.1.50+
            mplayer = aqt.sound.SimpleMplayerSlaveModePlayer(taskman)
        audio_player.players.append(mplayer)


def will_use_audio_player():
    gui_hooks.collection_did_load.append(lambda _: _setup_audio_player())
    gui_hooks.profile_will_close.append(lambda: audio_player.shutdown())


def audio(file: Path):
    audio_player.play_file(str(file))


def add_script(web: Union[AnkiWebView, WebContent], js: str):
    """Add script to the end of the body to be executed after Anki's code"""
    if isinstance(web, AnkiWebView):
        js.replace(r"`", r"\`")
        web.eval(
            """
        (() => {
            const script = document.createElement("script")
            script.innerHTML = `%s`
            document.body.appendChild(script)
        })()
        """
            % js
        )
    else:
        web.body += "<script>%s</script>" % js
    return


def add_style(web: Union[AnkiWebView, WebContent], css: str):
    """Add style to the end of the head"""
    if isinstance(web, AnkiWebView):
        css.replace(r"`", r"\`")
        web.eval(
            """
        (() => {
            const style = document.createElement("style")
            style.innerHTML = `%s`
            document.head.appendChild(style)
        })()
        """
            % css
        )
    else:
        web.head += "<style>%s</style>" % css


def add_html(
    web: Union[AnkiWebView, WebContent],
    html: str,
    to: Literal["top", "bottom"] = "bottom",
):
    """Add HTML to top/bottom of existing content (div#main)"""
    if isinstance(web, AnkiWebView):
        html.replace(r"`", r"\`")
        web.eval(
            """
        (() => {
            const div = document.createElement("div")
            div.innerHTML = `%s`

            const to = `%s`
            const main = document.getElementById("main")
            const parent = main.parentNode
            while(div.childNodes.length > 0) {
                const childNode = div.childNodes[0]
                if (to === "top") {
                    parent.insertBefore(childNode, main)
                } else {
                    document.body.appendChild(childNode)
                }
            }
        })()
        """
            % (html, to)
        )
    else:
        if to == "top":
            web.body = html + web.body
        else:
            web.body = web.body + html
