from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child node")
        return (
                f"<{self.tag}{self.props_to_html()}>"
                + "".join(child.to_html() for child in self.children)
                + f"</{self.tag}>"
        )

    def __repr__(self):
        children_repr = [child.tag for child in self.children]
        return (f"ParentNode(tag={repr(self.tag)}, "
                f"props={repr(self.props)}, children={children_repr})")
