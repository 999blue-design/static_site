# class HTMLNode:
#     def __init__(
#         self,
#         tag: str | None = None,
#         value: str | None = None,
#         children: list["HTMLNode"] | None = None,
#         props: dict[str, str] | None = None,
#     ) -> None:
#         self.tag = tag
#         self.value = value
#         self.children = children  # if children is not None else []
#         self.props = props  # if props is not None else {}

#     def to_html(self) -> str:
#         raise NotImplementedError("to_html method must be implemented in subclasses")

#     def props_to_html(self) -> str:
#         return " ".join(f'{key}="{value}"' for key, value in self.props.items())

#     def __repr__(self):
#         return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list["HTMLNode"] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
