import re


def render_bold(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def render_italic(text):
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    return text


def parse_inline_markdown(text):
    text = render_bold(text)
    text = render_italic(text)
    return text


print(
    parse_inline_markdown(
        "This is **bold** and this is _italic_ and this is **bold and _italic_**"
    )
)

print(
    parse_inline_markdown(
        "This is **bold** and this is _italic_ and this is  _italic and **bold**_"
    )
)
