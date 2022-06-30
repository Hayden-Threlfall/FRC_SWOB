
class HTMLElement:
    def __init__(self, tag=None, children=None, attrs=None, parent=None, _class=None):

        if parent is not None:
            parent.append_child(self)

        self.tag = tag
        self.attrs = attrs if attrs is not None else {}

        if children is None:
            self.children = []
        elif isinstance(children, list):
            self.children = children
        else:
            self.children = [children]

        if _class is not None:
            self.add_class(_class)
        self.init()

    def init(self):
        pass

    def set_attr(self, key, val):
        self.attrs[key] = val
        return self

    def add_class(self, c):
        if "class" not in self.attrs:
            self.attrs["class"] = c
        else:
            self.attrs["class"] += " "+c

    def append_child(self, child):
        self.children.append(child)
        return self

    def __str__(self):
        attrHTML = " ".join('{}="{}"'.format(key, self.attrs[key]) for key in self.attrs)
        innerHTML = "\n".join(str(child) for child in self.children)
        html = "<{0} {1}>{2}</{0}>".format(self.tag, attrHTML, innerHTML)
        return html


class TRElement(HTMLElement):
    def init(self):
        self.tag = "tr"

    def add_td(self, content=""):
        self.append_child(TDElement(children=content))


class TDElement(HTMLElement):
    def init(self):
        self.tag = "td"


class THElement(HTMLElement):
    def init(self):
        self.tag = "th"


class TableElement(HTMLElement):
    def init(self):
        self.tag = "table"


class PElement(HTMLElement):
    def init(self):
        self.tag = "p"


class UlElement(HTMLElement):
    def init(self):
        self.tag = "ul"


class LiElement(HTMLElement):
    def init(self):
        self.tag = "li"


class DivElement(HTMLElement):
    def init(self):
        self.tag = "div"


class AElement(HTMLElement):
    def init(self):
        self.tag = "a"


class SectionElement(HTMLElement):
    def init(self):
        self.tag = "section"


class H3Element(HTMLElement):
    def init(self):
        self.tag = "h3"


class H1Element(HTMLElement):
    def init(self):
        self.tag = "h1"
