import os
import random
from pathlib import Path

from aqt.webview import AnkiWebView

from .. import resourse_url, triggers, events


def random_image() -> str:
    """Returns random cat image url"""
    dir = Path(__file__).parent / "images"
    files = list(dir.glob("**/*"))
    file = random.choice(files)
    rel_path = file.relative_to(dir)
    return resourse_url(__file__, f"images/{str(rel_path)}")


def on_congrats(web: AnkiWebView):
    """Insert cat image onto Congrats page"""
    image_url = random_image()
    html = (
        """
<div id="cat-container">
    <img id="cat-image" src="%s">
</div>
    """
        % image_url
    )
    style = """
#cat-container {
    display: flex;
    justify-content: center;
}
#cat-image {
    max-width: 30em;
    margin: auto 0;
}
    """

    events.add_style(web, style)
    events.add_html(web, html, to="top")


triggers.congrats_page(on_congrats)
