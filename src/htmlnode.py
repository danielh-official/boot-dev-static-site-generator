class HTMLNode:
    def __init__(
        self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self):
        if self.children:
            content = "".join(child.to_html() for child in self.children)
        else:
            content = self.value or ""

        if self.tag is None:
            return content

        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"
    
    def props_to_html(self) -> str:
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self) -> None:
        print(self)
        
    
