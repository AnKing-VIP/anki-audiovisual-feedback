from pathlib import Path
from typing import Literal, Union

from aqt import mw, gui_hooks
from aqt.webview import AnkiWebView, WebContent
import aqt.sound
from aqt.sound import SoundOrVideoTag, AVPlayer

try:  # 2.1.50+
    from anki.utils import is_win
except:
    from anki.utils import isWin as is_win


class CustomAVPlayer(AVPlayer):
    no_interrupt = False

    def _on_play_without_interrupt_finished(self):
        self.no_interrupt = False
        self._on_play_finished()

    def _stop_if_playing(self):
        if self.current_player and not self.no_interrupt:
            self.current_player.stop()

    def play_without_interrupt(self, file: Path):
        """Audio played with this function will not be interrupted by other audio
        except audio played through this function.
        This function does not clear existing audio queue created by other play methods.
        """
        if self.current_player:
            self.current_player.stop()

        self.no_interrupt = True
        tag = SoundOrVideoTag(filename=str(file.resolve()))
        best_player = self._best_player_for_tag(tag)
        if best_player:
            self.current_player = best_player
            gui_hooks.av_player_will_play(tag)
            self.current_player.play(tag, self._on_play_without_interrupt_finished)
        else:
            print(f"ERROR: no players found for {tag}")


def will_use_audio_player():
    aqt.sound.av_player.no_interrupt = False
    AVPlayer._on_play_without_interrupt_finished = (
        CustomAVPlayer._on_play_without_interrupt_finished
    )
    AVPlayer._stop_if_playing = CustomAVPlayer._stop_if_playing
    AVPlayer.play_without_interrupt = CustomAVPlayer.play_without_interrupt


def audio(file: Path):
    aqt.sound.av_player.play_without_interrupt(file)


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
