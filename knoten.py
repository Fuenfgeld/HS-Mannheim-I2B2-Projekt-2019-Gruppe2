from anytree import Node


class node_with_value(Node):

    def __init__(self, name, fullname, pfad, size=0, parent=None, children=None, **kwargs):
        Node.__init__(self, name, parent, children, **kwargs)
        self.fullname = fullname
        self.pfad = pfad
        self.size = int(size)
