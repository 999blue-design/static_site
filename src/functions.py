from textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == text_type:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    new_nodes.append(TextNode(part, text_type))
                if i < len(parts) - 1:
                    new_nodes.append(TextNode(delimiter, TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes


split_nodes_delimiter.__doc__ = (
    """Splits a list of TextNode objects by a given delimiter and text type."""
)

split_nodes_delimiter.__annotations__ = {
    "old_nodes": list[TextNode],
    "delimiter": str,
    "text_type": TextType,
    "return": list[TextNode],
}


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts all markdown image links from a given text.

    Args:
        text (str): The input text containing markdown image links.
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts all markdown links from a given text.

    Args:
        text (str): The input text containing markdown links.
        "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)


# print(
#     extract_markdown_links(
#         "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
#     )
# )
# print(
#     extract_markdown_images(
#         "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#     )
# )


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            if images:
                last_index = 0
                for image_text, image_url in images:
                    start_index = node.text.find(
                        f"![{image_text}]({image_url})", last_index
                    )
                    if start_index != -1:
                        if start_index > last_index:
                            new_nodes.append(
                                TextNode(
                                    node.text[last_index:start_index], TextType.TEXT
                                )
                            )
                        new_nodes.append(
                            TextNode(image_text, TextType.IMAGE, image_url)
                        )
                        last_index = start_index + len(f"![{image_text}]({image_url})")
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if links:
                last_index = 0
                for link_text, link_url in links:
                    start_index = node.text.find(
                        f"[{link_text}]({link_url})", last_index
                    )
                    if start_index != -1:
                        if start_index > last_index:
                            new_nodes.append(
                                TextNode(
                                    node.text[last_index:start_index], TextType.TEXT
                                )
                            )
                        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                        last_index = start_index + len(f"[{link_text}]({link_url})")
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes
