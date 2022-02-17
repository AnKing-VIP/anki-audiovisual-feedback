from pathlib import Path
from typing import Literal

import aqt.sound
from aqt.webview import AnkiWebView


def sound(path: Path):
    """Play sound file"""
    path = path.resolve()
    aqt.sound.play(str(path))


def add_script(web: AnkiWebView, js: str):
    """Add script to the end of the body to be executed after Anki's code"""
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
    return


def add_style(web: AnkiWebView, css: str):
    """Add style to the end of the head"""
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


def add_html(web: AnkiWebView, html: str, to: Literal["top", "bottom"] = "bottom"):
    """Add HTML to top/bottom of existing content (div#main)"""
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
