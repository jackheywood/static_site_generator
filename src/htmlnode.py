class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return "".join(f' {key}="{val}"' for key, val in self.props.items())

    def __repr__(self):
        children_repr = [child.tag for child in self.children]
        return (f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, "
                f"props={repr(self.props)}, children={children_repr})")
