# helper functions...Use this module to read a csv file, turn into a pandas data frame, filter records, and enter them
# into the sql database. Remember to import session from sqlalchemy.

from app.reader import CsvReader


def filter_root(root_id, nodes):
    for node in nodes:
        if node.id == root_id:
            nodes.remove(node)
    return nodes


class Node:
    def __init__(self):
        self.parent = None
        self.children = []


class Tree:
    def __init__(self, root):
        self.root = root

    def add_node(self,parent,child):
        child.parent = parent
        parent.children.append(child)

    def find_comp(self):
        value = 1
        for child in self.root.children:
            if len(child.children) == 0:
                return value
            else: value += 1
        return value



if __name__ == "__main__":
    root = Node()
    tree = Tree(root)

    level1 = Node()
    level12 = Node()
    level23 = Node()
    level24 = Node()
    level25 = Node()

    tree.add_node(root,level1)
    tree.add_node(root, level12)

    tree.add_node(level1,level23)
    tree.add_node(level12, level24)
    tree.add_node(level23, level25)

    print(tree.find_comp())