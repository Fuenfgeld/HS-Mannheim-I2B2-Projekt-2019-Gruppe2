from anytree import Node





class node_with_value(Node):



    def __init__(self, name, fullname, pfad, size=0, parent=None, children=None, **kwargs):

        Node.__init__(self, name, parent, children, **kwargs)

        self.fullname = fullname

        self.pfad = pfad

        self.size = size

    def __eq__(self, other):
        if not isinstance(other, node_with_value):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.name == other.name and self.fullname == other.fullname and self.pfad == other.pfad and self.size==other.size,
                self.parent==other.parent, self.children==other.children)

def checkNameVonKnoten(self,name,fullname,erwarteterName):
        nameK= node_with_value.__init__(self,name=name,fullname=fullname,pfad=None)
        assert nameK==erwarteterName
def test_Name():
    checkNameVonKnoten('miau','root','miau','miau')
