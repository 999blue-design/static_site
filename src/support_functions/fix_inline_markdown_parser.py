import re

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


class LeafNode:
    def __init__(self, tag, value, props=None):
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value

        props_text = ""
        if self.props is not None:
            for key, value in self.props.items():
                props_text += f' {key}="{value}"'

        return f"<{self.tag}{props_text}>{self.value}</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type == TEXT_TYPE_TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TEXT_TYPE_BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TEXT_TYPE_ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TEXT_TYPE_CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TEXT_TYPE_LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TEXT_TYPE_IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError("invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        index = 0
        while index < len(parts):
            part = parts[index]
            if part != "":
                if index % 2 == 0:
                    new_nodes.append(TextNode(part, TEXT_TYPE_TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
            index += 1
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        while remaining_text != "":
            match = re.search(pattern, remaining_text)
            if match is None:
                new_nodes.append(TextNode(remaining_text, TEXT_TYPE_TEXT))
                break

            if match.start() > 0:
                new_nodes.append(
                    TextNode(remaining_text[: match.start()], TEXT_TYPE_TEXT)
                )

            alt_text = match.group(1)
            image_url = match.group(2)
            new_nodes.append(TextNode(alt_text, TEXT_TYPE_IMAGE, image_url))
            remaining_text = remaining_text[match.end() :]

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        if node.text_type != TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        while remaining_text != "":
            match = re.search(pattern, remaining_text)
            if match is None:
                new_nodes.append(TextNode(remaining_text, TEXT_TYPE_TEXT))
                break

            if match.start() > 0:
                new_nodes.append(
                    TextNode(remaining_text[: match.start()], TEXT_TYPE_TEXT)
                )

            link_text = match.group(1)
            link_url = match.group(2)
            new_nodes.append(TextNode(link_text, TEXT_TYPE_LINK, link_url))
            remaining_text = remaining_text[match.end() :]

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TEXT_TYPE_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TEXT_TYPE_BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TEXT_TYPE_ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TEXT_TYPE_CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


# TESTING


run_cases = [
    (
        "Hi **there** and _friend_",
        [
            ("text", "Hi ", None),
            ("bold", "there", None),
            ("text", " and ", None),
            ("italic", "friend", None),
        ],
        ["Hi ", "<b>there</b>", " and ", "<i>friend</i>"],
    ),
    (
        "Use `print()` then visit [docs](https://example.com)",
        [
            ("text", "Use ", None),
            ("code", "print()", None),
            ("text", " then visit ", None),
            ("link", "docs", "https://example.com"),
        ],
        [
            "Use ",
            "<code>print()</code>",
            " then visit ",
            '<a href="https://example.com">docs</a>',
        ],
    ),
]

submit_cases = run_cases + [
    (
        "Look at ![logo](logo.png)",
        [
            ("text", "Look at ", None),
            ("image", "logo", "logo.png"),
        ],
        ["Look at ", '<img src="logo.png" alt="logo"></img>'],
    ),
    (
        "Just plain text",
        [("text", "Just plain text", None)],
        ["Just plain text"],
    ),
    (
        "Start **bold** mid _italics_ and `code` then ![pic](a.png) plus [link](https://x.y) end",
        [
            ("text", "Start ", None),
            ("bold", "bold", None),
            ("text", " mid ", None),
            ("italic", "italics", None),
            ("text", " and ", None),
            ("code", "code", None),
            ("text", " then ", None),
            ("image", "pic", "a.png"),
            ("text", " plus ", None),
            ("link", "link", "https://x.y"),
            ("text", " end", None),
        ],
        [
            "Start ",
            "<b>bold</b>",
            " mid ",
            "<i>italics</i>",
            " and ",
            "<code>code</code>",
            " then ",
            '<img src="a.png" alt="pic"></img>',
            " plus ",
            '<a href="https://x.y">link</a>',
            " end",
        ],
    ),
]


def get_node_signatures(nodes):
    signatures = []
    for node in nodes:
        signatures.append((node.text_type, node.text, node.url))
    return signatures


def get_html_signatures(nodes):
    html = []
    for node in nodes:
        html.append(text_node_to_html_node(node).to_html())
    return html


def format_lines(items):
    lines = []
    for item in items:
        lines.append(f"  {item}")
    return "\n".join(lines)


def test(markdown_text, expected_nodes, expected_html):
    print("---------------------------------")
    print(f"Input: {markdown_text}")
    print("")

    result_nodes = text_to_textnodes(markdown_text)
    actual_nodes = get_node_signatures(result_nodes)
    actual_html = get_html_signatures(result_nodes)

    print("Expected text nodes:")
    print(format_lines(expected_nodes))
    print("Actual text nodes:")
    print(format_lines(actual_nodes))
    print("")
    print("Expected HTML:")
    print(format_lines(expected_html))
    print("Actual HTML:")
    print(format_lines(actual_html))

    if actual_nodes == expected_nodes and actual_html == expected_html:
        return True
    return False


def main():
    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)
    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
            print("Pass")
        else:
            failed += 1
            print("Fail")
    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")
    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()
