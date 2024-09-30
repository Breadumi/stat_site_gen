class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        attrs = self.props.items()
        html_string = ""

        for k in attrs:
            html_string = html_string + f" {k[0]}=" + '"' + f"{k[1]}" + '"'

        return html_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.children is not None:
            raise ValueError("LeafNode cannot have children")
        
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        if self.value is not None:
            raise ValueError("ParentNode cannot have a value")
        
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        html_to_inject = ""

        for node in self.children:
            html_to_inject += node.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_to_inject}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"