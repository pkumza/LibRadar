# -*- coding: utf-8 -*-
"""
    DEX Tree

    This script is used to implement the tree node and tree structure.
    :copyright: (c) 2016 by Zachary Ma
    : Project: LibRadar

"""

from _settings import *
import binascii
import hashlib
import csv
import redis

# Databases
db_feature_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_COUNT)
db_feature_weight = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_WEIGHT)
db_un_ob_pn = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN)
db_un_ob_pn_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN_COUNT)

# tag_rules
labeled_libs = list()
no_lib = list()

with open(FILE_RULE, 'r') as file_rules:
    csv_rules_reader = csv.reader(file_rules, delimiter=',', quotechar='|')
    for row in csv_rules_reader:
        if row[1] == "no":
            no_lib.append(row)
        else:
            labeled_libs.append(row)


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
            self.md5 = md5
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

    @staticmethod
    def _cal_md5(node):
        # Ignore Leaf Node
        if len(node.children) == 0 and node.md5 != "":
            return
        # Test bug: Wrong Node
        if len(node.children) == 0:
            logger.error("Md5 is not empty but no child")
        # Test bug: Wrong Node
        if node.md5 != "":
            logger.error("Children exist but md5 is not empty")
        # Everything seems Okay.
        cur_md5 = hashlib.md5()
        md5_list = list()
        for child in node.children:
            md5_list.append(node.children[child].md5)
        md5_list.sort()
        for md5_item in md5_list:
            cur_md5.update(md5_item)
        node.md5 = cur_md5.digest()
        # you could see node.pn here. e.g. Lcom/tencent/mm/sdk/modelpay

    def cal_md5(self):
        """
        Calculate md5 for every package
        :return:
        """
        self.post_order(visit=self._cal_md5)

    @staticmethod
    def _match(node):
        a = db_un_ob_pn.get(node.md5)
        w = db_feature_weight.get(node.md5)
        c = db_feature_count.get(node.md5)
        u = db_un_ob_pn_count.get(node.md5)
        """ Debug Log
        if a is not None:
            print "----"
            print "Potential Name: " + a
            print "Package Name  :" + node.pn
            print "Count: " + u + '/' + c
            print str(node.weight) + " " + str(w)
        """
        # if could not find this package in database, search its children.
        if a is None:
            return 1
        # CRITICAL PROBLEM
        if int(w) != node.weight:
            logger.critical("Same Md5, Diff Weight: %s" % (binascii.hexlify(node.md5)))
        # Potential Name is not convincing enough.
        if u < 8 or float(u) / float(c) < 0.3:
            return 2
        for lib in labeled_libs:
            # if the potential package name is the same as full lib path
            # do not search its children
            if lib[0] == a:
                node.match.append([lib, node.weight])
                return -1
            # If they have the same length but not equal to each other, just continue
            if len(lib[0]) == len(a):
                continue
            # if the potential package name is part of full lib path, search its children
            #   e.g. a is Lcom/google, we could find it as a part of Lcom/google/android/gms, so search its children for
            #       more details
            if len(a) < len(lib[0]) and a == lib[0][:len(a)]:
                return 3
            # If the lib path is part of potential package name, add some count into parent's match list.
            if len(a) > len(lib[0]) and lib[0] == a[:len(lib[0])]:
                depth_diff = a.count('/') - lib[0].count('/')
                cursor = node
                for i in range(depth_diff):
                    # cursor should not be the root, so cursor's parent should not be None.
                    if cursor.parent.parent != None:
                        cursor = cursor.parent
                    else:
                        # root's parent is None
                        #   This situation exists
                        #   For Example: If it takes Lcom/a/b as Lcom/google/android/gms/ads/mediation/customevent,
                        #   It will find its ancestor until root or None.
                        return 4
                flag = False
                for matc in cursor.match:
                    # if matc[0][0] == lib[0]:
                    if matc[0] == lib:
                        matc[1] += node.weight
                        flag = True
                if not flag:
                    cursor.match.append([lib, node.weight])
        # Never find a good match, search its children.
        return 5

    def match(self):
        self.pre_order(visit=self._match)

    @staticmethod
    def _get_lib(node):
        for matc in node.match:
            print("----")
            print("Package: %s" % node.pn)
            print("Library: %s" % matc[0][1])
            print("Standard Package: %s" % matc[0][0])
            print("Type: %s" % matc[0][2])
            print("Website: %s" % matc[0][3])
            print("Similarity: %d/%d" % (matc[1], node.weight))
            continue
            if matc[1] * 2 > node.weight * 1:
                print matc[0]
                return -1
        return 0

    def get_lib(self):
        self.pre_order(visit=self._get_lib)


if __name__ == '__main__':
    print " === Test starts ===="
    pass
    """
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
    """
    print " === Test ends   ===="
