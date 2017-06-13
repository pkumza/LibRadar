# -*- coding: utf-8 -*-

#   Copyright 2017 Zachary Marv (马子昂)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


#   DEX Tree
#
#   This script is used to implement the tree node and tree structure.


from _settings import *
from collections import Counter
import hashlib
import csv
import redis
import zlib
import rputil


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
        sha256  : 02b018f5b94c5fbc773ab425a15b8bbb              // In fact sha256 is the non-hex one
        weight  : 1023                                          // How many APIs in this Node
        pn      : Lcom/facebook/internal                        // Current package name
        parent  : <TreeNode>                                    // Parent node
        children: dict("pn": <TreeNode>)                              // Children nodes
        match   : list( tuple(package_name, match_weight) )     // match lib list
    }
    """
    def __init__(self, n_weight=-1, n_pn="", n_parent=None):
        self.sha256 = ""
        self.weight = n_weight
        self.pn = n_pn
        self.parent = n_parent
        self.children = dict()
        self.match = list()
        self.permissions = set()
        self.db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID, password=DB_PSWD)
        self.api_id_list = []

    def insert(self, package_name, weight, sha256, permission_list, api_id_list):
        # no matter how deep the package is, add permissions here.
        for permission in permission_list:
            self.permissions.add(permission)
        # no matter how deep the package is, add api_id_list
        # self.api_id_list = self.api_id_list + api_id_list
        current_depth = 0 if self.pn == "" else self.pn.count('/') + 1
        target_depth = package_name.count('/') + 1
        if current_depth == target_depth:
            self.sha256 = sha256
            self.api_id_list = api_id_list
            return "F: %s" % package_name
        target_package_name = '/'.join(package_name.split('/')[:current_depth + 1])
        if target_package_name in self.children:
            self.children[target_package_name].weight += weight
            return self.children[target_package_name].insert(package_name, weight, sha256, permission_list, api_id_list)
        else:
            self.children[target_package_name] = TreeNode(n_weight=weight, n_pn=target_package_name, n_parent=self)
            return self.children[target_package_name].insert(package_name, weight, sha256, permission_list, api_id_list)

    def brand(self, package_name, standard_package):
        current_depth = 0 if self.pn == "" else self.pn.count('/') + 1
        target_depth = package_name.count('/') + 1
        if current_depth == target_depth:
            yes_or_no = raw_input("Warning: Brand %s as a new library? (Y/n)" % self.pn)
            if yes_or_no == 'Y' or yes_or_no == 'y':
                try:
                    self.db.hincrby(name=DB_FEATURE_CNT, key=self.sha256, amount=10000000)
                    self.db.hset(name=DB_FEATURE_WEIGHT, key=self.sha256, value=self.weight)
                    self.db.hset(name=DB_UN_OB_PN, key=self.sha256, value=standard_package)
                    self.db.hset(name=DB_FEATURE_CNT, key=self.sha256, value=100000000)
                except:
                    return "Error in database."
                return "Success."
            else:
                return "Did nothing. Bye~"
        else:
            target_package_name = '/'.join(package_name.split('/')[:current_depth + 1])
            if target_package_name in self.children:
                return self.children[target_package_name].brand(package_name, standard_package)
            else:
                return "Package Not found in this APK."


class Tree(object):
    """
    Tree
    """
    def __init__(self):
        self.root = TreeNode()
        self.db = None
        self.feature = None
        self.db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID, password=DB_PSWD)
        self.db_rep = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID_REP, password=DB_PSWD)

    def insert(self, package_name, weight, sha256, permission_list, api_id_list):
        self.root.insert(package_name, weight, sha256, permission_list, api_id_list)

    def brand(self, package_name, standard_package):
        return self.root.brand(package_name, standard_package)

    def pre_order_res(self, visit, res):
        self._pre_order_res(node=self.root, visit=visit, res=res)

    def _pre_order_res(self, node, visit, res):
        ret = visit(node, res)
        if ret < 0:
            return
        else:
            for child_pn in node.children:
                self._pre_order_res(node.children[child_pn], visit, res)

    def pre_order_res_ret(self, visit, res, ret):
        self._pre_order_res_ret(node=self.root, visit=visit, res=res, ret=ret)

    def _pre_order_res_ret(self, node, visit, res, ret):
        retu = visit(node, res, ret)
        if retu < 0:
            return
        else:
            for child_pn in node.children:
                self._pre_order_res_ret(node.children[child_pn], visit, res, ret)

    def pre_order(self, visit):
        self._pre_order(self.root, visit)

    def _pre_order(self, node, visit):
        ret = visit(node)
        if ret < 0:
            return
        else:
            for child_pn in node.children:
                self._pre_order(node.children[child_pn], visit)

    def post_order(self, visit):
        self._post_order(self.root, visit)

    def _post_order(self, node, visit):
        for child_pn in node.children:
            self._post_order(node.children[child_pn], visit)
        visit(node)

    @staticmethod
    def _cal_sha256(node):
        # Ignore Leaf Node
        if len(node.children) == 0 and node.sha256 != "":
            return
        # Everything seems Okay.
        cur_sha256 = hashlib.sha256()
        sha256_list = list()
        for child in node.children:
            sha256_list.append(node.children[child].sha256)
        sha256_list.sort()
        for sha256_item in sha256_list:
            cur_sha256.update(sha256_item)
        node.sha256 = cur_sha256.hexdigest()
        # you could see node.pn here. e.g. Lcom/tencent/mm/sdk/modelpay

    def cal_sha256(self):
        """
        Calculate sha256 for every package
        :return:
        """
        self.post_order(visit=self._cal_sha256)

    def _match(self, node):
        a, c, u = None, None, None
        pipe = self.db.pipeline()
        pipe.hget(name=DB_UN_OB_PN, key=node.sha256)
        pipe.hget(name=DB_FEATURE_CNT, key=node.sha256)
        pipe.hget(name=DB_UN_OB_CNT, key=node.sha256)
        pipe_res = pipe.execute()
        a, c, u = pipe_res

        # if could not find this package in database, search its children.
        if a is None:
            return 1
        # Potential Name is not convincing enough.
        if u < 8 or float(u) / float(c) < 0.3:
            return 2
        flag_not_deeper = False
        for lib in labeled_libs:
            # if the potential package name is the same as full lib path
            # do not search its children
            if lib[0] == a:
                node.match.append([lib, node.weight, int(c)])
                continue
            # If they have the same length but not equal to each other, just continue
            if len(lib[0]) == len(a):
                continue
            # if the potential package name is part of full lib path, search its children
            #   e.g. a is Lcom/google, we could find it as a part of Lcom/google/android/gms, so search its children for
            #       more details
            if len(a) < len(lib[0]) and a == lib[0][:len(a)] and lib[0][len(a)] == '/':
                continue
            # If the lib path is part of potential package name, add some count into parent's match list.
            if len(a) > len(lib[0]) and lib[0] == a[:len(lib[0])] and a[len(lib[0])] == '/':
                depth_diff = a.count('/') - lib[0].count('/')
                cursor = node
                for i in range(depth_diff):
                    # cursor should not be the root, so cursor's parent should not be None.
                    if cursor.parent.parent is not None:
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
                        flag = True
                        if matc[1] != cursor.weight:
                            matc[1] += node.weight
                if not flag:
                    cursor.match.append([lib, node.weight, c])
                flag_not_deeper = True
                continue
        """
            One degree deeper!
            深入探测一层

                There's a situation that a package is a library and the child of a package is also a library.
                库是存在相互嵌套的。

                As we all know that Lcom/unity3d is definitely a Game Engine library. There could be some sub-package
                like Lcom/unity3d/player, Lcom/unity3d/plugin, Lcom/unity3d/sdk, etc. So we take Lcom/unity3d as the
                root package of this library.
                比如，Lcom/unity3d 显然是Unity3D这个游戏引擎，在游戏引擎下可能会有player, plugin, sdk等次级包（文件夹），所以我们很
                显然地把Lcom/unity3d作为游戏引擎的根包。

                However, Lcom/unity3d/ads is an Advertisement library.
                但是，Lcom/unity3d/ads是Unity3D公司推出的广告库

                If we do not search one degree deeper, we could only find the game engine other than the ads library.
                Likewise, we could not find Landroid/support/v4 anymore if we take Landroid/support as a library.
                如果我们不继续搜索的话，那么对于一个应用，我们只能检测到Unity3D这个引擎，无法检测到Unity3D Ads这个广告库。

            Implementation:
            实现：
                if lib[0] == a, we continue search his children.
                if lib[0] == a 这个后面从return变成了continue，我们会继续搜索它的子节点

                if we already found his child, we will not search deeper.
                在后面的代码中，如果已经知道的就是子节点，那么就不会继续深层的搜了。

                In my original code, I found a bug that the match degree is larger than the total amount of weight.
                This is impossible. After debugging, I found that if I add the match value multiple times, the match
                weight could overflow.
                在我原来有bug的代码中，我发现匹配的similarity有大于1的情况，即com/facebook这个库的similarity大于了1。这是因为match
                被我加总了数次

                For example:
                    There's a library Lcom/google/android/gson, weight is 189
                    we found Lcom/google/android/gson, so add the weight 189
                    we found Lcom/google/android/gson/internal, so add the weight 24
                    we found Lcom/google/android/gson/stream, so add the weight 43
                    In this case, the weight of package gson overflows.
                举例来看：
                    对于Lcom/google/android/gson这个包来说，它的API数量是189
                    搜索中找到 Lcom/google/android/gson， weight加上189
                    搜索中找到 Lcom/google/android/gson/internal， weight加上24
                    搜索中找到 Lcom/google/android/gson/stream, weight加上 43
                    这样显然就溢出了。

                Because we only search 1 degree deeper, the match situation of Lcom/google/android/gson is only true or
                false. In this case, we just need to check if the weight has overflowed before add weight. as the code:
                    if matc[1] != cursor.weight:
                        matc[1] += node.weight
                因为我们可以多搜一层，所以判断是否溢出很简单。因为对于上层的库来说，也就只有两种情况，那就是匹配到和没匹配到。所以只需要
                检测一下是否已经超出就行了。
        """
        if flag_not_deeper:
            return -1
        # Never find a good match, search its children.
        return 5

    def match(self):
        self.pre_order(visit=self._match)

    def _find_untagged(self, node, res):
        # If there's already some matches here, do not search its children. non-sense.
        a, c, u = None, None, None
        if len(node.match) != 0:
            return -1
        pipe = self.db.pipeline()
        pipe.hget(name=DB_UN_OB_PN, key=node.sha256)
        pipe.hget(name=DB_FEATURE_CNT, key=node.sha256)
        pipe.hget(name=DB_UN_OB_CNT, key=node.sha256)
        pipe_res = pipe.execute()
        a, c, u = pipe_res


        if a is None:
            return 1
        # If the package name is already in no_lib list, ignore it and search its children.
        for non_lib in no_lib:
            if non_lib[0] == a:
                return 1
        # Potential Name is not convincing enough. search its children
        if float(u) / float(c) < 0.5 or node.weight < 50 or int(c) < 20:
            return 2

        # JSON support
        utg_lib_obj = dict()            # untagged library object
        utg_lib_obj["Package"] = node.pn
        utg_lib_obj["Standard Package"] = a
        utg_lib_obj["Library"] = "Unknown"
        utg_lib_obj["Popularity"] = int(c)
        utg_lib_obj["Weight"] = node.weight

        res.append(utg_lib_obj)

        # OLD Print
        # print("----")
        # print("Package: %s" % node.pn)
        # print("Match Package: %s" % u)
        # print("Library: Unknown.")
        # print("Popularity: %s" % c)
        # print("API count: %s" % node.weight)

    def find_untagged(self, res):
        self.pre_order_res(visit=self._find_untagged, res=res)

    @staticmethod
    def _get_lib(node, res):
        for matc in node.match:
            if float(matc[1]) / float(node.weight) < 0.1 and matc[0][0] != node.pn:
                continue
            # JSON
            lib_obj = dict()
            lib_obj["Package"] = node.pn  # cpn
            lib_obj["Library"] = matc[0][1] # lib
            lib_obj["Standard Package"] = matc[0][0] # pn
            lib_obj["Type"] = matc[0][2] # tp
            lib_obj["Website"] = matc[0][3] # ch
            lib_obj["Match Ratio"] = "%d/%d" % (matc[1], node.weight) # no similarity in V1
            lib_obj["Popularity"] = matc[2] # dn
            lib_obj["Permission"] = sorted(list(node.permissions))
            res.append(lib_obj)
            # Old Print
            # print("----")
            # print("Package: %s" % node.pn)
            # print("Library: %s" % matc[0][1])
            # print("Standard Package: %s" % matc[0][0])
            # print("Type: %s" % matc[0][2])
            # print("Website: %s" % matc[0][3])
            # print("Similarity: %d/%d" % (matc[1], node.weight))
            # print("Popularity: %d" % matc[2])
            # permission_out = ""
            # for permission in sorted(list(node.permissions)):
            #     permission_out += (permission + ",")
            # if len(permission_out) > 0:
            #     permission_out = permission_out[:-1]
            # print("Permissions:" + permission_out)
        return 0

    def get_lib(self, res):
        self.pre_order_res(visit=self._get_lib, res=res)

    @staticmethod
    def _get_repackage_main(node, res, ret):
        if node.pn in res:
            return -1
        if len(node.children) == 0:
            ret.extend(node.api_id_list)
            ret += node.api_id_list
        return 0

    def get_repackage_main(self, res, hex_sha256):
        # res is a list of libraries. Result.
        pn_list = list()
        for item in res:
            pn_list.append(item["Package"])
        ret = list()
        self.pre_order_res_ret(visit=self._get_repackage_main, res=pn_list, ret=ret)
        ret_length = len(ret)
        kvd = dict(Counter(ret))
        str = rputil.Util.dict2str(kvd)
        zstr = zlib.compress(str,1)
        self.db_rep.hset(name="apk_feature", key=hex_sha256, value=zstr)
        self.db_rep.zadd("apk_weight", ret_length, hex_sha256 )
