# -*- coding: utf-8 -*-
"""
    DEX Tree

    This script is used to implement the tree node and tree structure.
    :copyright: (c) 2016 by Zachary Ma
    : Project: LibRadar

"""

from _settings import logger
import binascii


class TreeNode(object):
    """
    Tree Node Structure
    {
        md5     : 02b018f5b94c5fbc773ab425a15b8bbb              // In fact md5 is the non-hex one
        weight  : 1023                                          // How many APIs in this Node
        pn      : Lcom/facebook/internal                        // Current package name
        parent  : <TreeNode>                                    // Parent node
        children: dict("pn": <TreeNode>)                              // Children nodes
        match   : list( tuple(package_name, match_weight) )     // match lib list
    }
    """
    def __init__(self, n_weight=-1, n_pn="", n_parent=None):
        # TODO exam : import binascii hexlify
        self.md5 = ""
        self.weight = n_weight
        self.pn = n_pn
        self.parent = n_parent
        self.children = dict()
        self.match = list()

    def insert(self, package_name, weight, md5):
        current_depth = 0 if self.pn == "" else self.pn.count('/') + 1
        target_depth = package_name.count('/') + 1
        if current_depth == target_depth:
            return "F: %s" % package_name
        target_package_name = '/'.join(package_name.split('/')[:current_depth + 1])
        if target_package_name in self.children:
            self.children[target_package_name].weight += weight
            return self.children[target_package_name].insert(package_name, weight, md5)
        else:
            self.children[target_package_name] = TreeNode(n_weight=weight, n_pn=target_package_name, n_parent=self)
            return self.children[target_package_name].insert(package_name, weight, md5)

    def get_node(self, package_name):
        current_depth = 0 if self.pn == "" else self.pn.count('/') + 1
        target_depth = package_name.count('/') + 1
        if current_depth == target_depth:
            return self
        target_package_name = '/'.join(package_name.split('/')[:current_depth + 1])
        if target_package_name in self.children:
            return self.children[target_package_name].get_node(package_name)
        else:
            return None

    def to_string(self):
        print("---- TreeNode toString ----")
        print("md5:%s" % binascii.hexlify(self.md5))
        print("weight:%d" % self.weight)
        print("pn:%s" % self.pn)
        print("---- print parent Later----")



class Tree(object):
    """
    Tree
    """
    def __init__(self):
        self.root = TreeNode()
        pass

    def insert(self, package_name, weight, md5):
        self.root.insert(package_name, weight, md5)

    def get_node(self, package_name):
        """
        Used for update.
        :param package_name:
        :return:
        """
        return self.root.get_node(package_name)

    def pre_order(self, visit):
        self._pre_order(self.root, visit)

    def _pre_order(self, node, visit):
        if node is None:
            return
        ret = visit(node)
        if ret < 0:
            return
        else:
            for child_pn in node.children:
                self._pre_order(node.children[child_pn], visit)

    def post_order(self, visit):
        self._post_order(self.root, visit)

    def _post_order(self, node, visit):
        if node is None:
            return
        for child_pn in node.children:
            self._post_order(node.children[child_pn], visit)
        visit(node)

    def print_node(self, package_name):
        node = self.get_node(package_name)
        if isinstance(node, TreeNode):
            node.to_string()
        else:
            logger.error("Wrong node to be printed.")


if __name__ == '__main__':
    print " === Test starts ===="

    tn = Tree()
    tn.insert("a/b", 12, "")
    tn.insert("a/c", 14, "")
    tn.insert("b/a/s", 16, "")
    tn.insert("b/h", 16, "")
    tn.insert("c/b", 414, "")
    tn.insert("b/a/e", 16, "")
    tn.insert("b/e", 16, "")
    tn.insert("b/a/s/cse", 16, "")
    tn.insert("b/a/s/cst", 16, "")
    tn.insert("b/a/s/csa", 16, "")
    def vis(node):
        if node.parent is None:
            pass
        else:
            print "L: " + node.pn + " P: " + node.parent.pn
        print node.weight
        return 0
    tn.post_order(vis)
    print "CS:"
    print tn.get_node("b/a/s").pn
    print " === Test ends   ===="
