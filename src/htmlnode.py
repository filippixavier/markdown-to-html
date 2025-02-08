class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children is not None and not isinstance(children, list):
            raise TypeError("children argument must be a list")

        if props is not None and not isinstance(props, dict):
            raise NotImplementedError("to_html method not implemented")

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        return " " + " ".join(map(lambda attr: f"{attr[0]}=\"{attr[1]}\"" , self.props.items()))

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"