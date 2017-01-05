# -*- coding: utf-8 -*-
"""
    DEX Extractor

    This script is used to extract features and other information from DEX files.
    :copyright: (c) 2016 by Zachary Ma
    : Project: LibRadar

    Target:
        Get a dex file
        Generate features from the dex file.
        Get the features of classes and packages.

    Implementation:
        Firstly, get class defines from dex file.
        For each class, we could generate it's APIs and so as the MD5 feature.
        As the class definition contains the path, so we could construct a tree for the classes.

        e.g.

                        root
                        /   \
                  android   com
                    /       /  \
                support  google facebook
                  /       /   \      \
                 v4     gson  ads    c.class
                 |       |      \
               media   e.class  purchase
               /    \              |
           a.class  b.class       d.class

        For every package, we generate features based on it's child.
        for example, the feature of /android/support/v4/media is based on a.class and b.class.
        If we need to generate features of all packages, we could construct a tree for them.
        To minimize the complexity, and avoid constructing the tree, I sorted the class defines first.

        android/support/v4/media/a
        android/support/v4/media/b
        com/facebook/c
        com/google/ads/purchase/d
        com/google/gson/e

        It's like an in-order traversal for this tree:

        Create a stack for this. (Type: PackageNode)
        Scan android/support/v4/media/a and put 'android', 'support', 'v4', 'media' into the stack.
        Get the feature of a.class
        Update media's feature
        Get the feature of b.class
        Update media's feature
        Get the feature of c.class
        Pop media and put the feature into db
        Update and pop v4      and put the feature into db
        Update and pop support and put the feature into db
        Update and pop android and put the feature into db
        Push com
        Push facebook
        Update facebook with c.class
        Pop facebook
        Push google
        Push ads
        Push purchase
        Update Purchase's feature with d
        Pop Purchase
        Pop ads
        Push gson
        Update gson with e
        Pop gson
        Update and pop google
        Update and pop com

"""

import os.path
import hashlib
import dex_parser
import redis
from _settings import *


class PackageNode:
    def __init__(self, path, full_path):
        self.md5_list = list()
        self.path = path
        self.full_path = full_path
        self.weight = 0

    def generate_md5(self):
        curr_md5 = hashlib.md5()
        self.md5_list.sort()
        for md5_item in self.md5_list:
            curr_md5.update(md5_item)
        # TODO: put it into database
        if not IGNORE_ZERO_API_FILES or len(self.md5_list) != 0:
            logger.debug("MD5: %s Weight: %-6d PackageName: %s" %
                         (curr_md5.hexdigest(), self.weight, '/'.join(self.full_path)))
        return curr_md5.digest(), self.weight


class PackageNodeList:
    def __init__(self):
        self.pn_list = list()

    def catch_a_class_def(self, package_name, class_md5, class_weight):
        package_path_parts_list = package_name.split('/')
        common_depth = 0
        """
            len(self.pn_list)               The Length of the Stack
            len(package_path_parts_list)    The Length of current Class's package
            common_depth                           The Common parts' Length

            Operation 1:
                pop accomplished packages in pn_list

            Operation 2:
                append new parts from package_p... into pn_list

            e.g.
                self.pn_list     Lair/br/com/bitlabs/SWFPlayer/Player    len: 6
                package_p...     Lair/br/com/bitlabs/Software            len: 5
                --------
                common_depth: 4

                Operation 1:
                    Generate feature of Lair/br/com/bitlabs/SWFPlayer/Player
                    Pop Player
                    Update feature of Lair/br/com/bitlabs/SWFPlayer
                    Generate feature of Lair/br/com/bitlabs/SWFPlayer
                    Pop SWFPlayer
                    Update feature of Lair/br/com/bitlabs

                Operation 2:
                    Create new Node Software
        """
        # Get Common Depth ---- Test how many stages are the same.
        while common_depth < len(self.pn_list) and common_depth < len(package_path_parts_list):
            if package_path_parts_list[common_depth] != self.pn_list[common_depth].path:
                break
            common_depth += 1
        # Operation 1
        pn_list_size = len(self.pn_list)
        for d in range(pn_list_size - 1, common_depth - 1, -1):
            stage_to_be_pop = self.pn_list[-1]
            child_md5, curr_weight = stage_to_be_pop.generate_md5()
            if len(self.pn_list) > 1:
                stage_to_be_update = self.pn_list[-2]
                stage_to_be_update.md5_list.append(child_md5)
                stage_to_be_update.weight += curr_weight
            self.pn_list.pop()
        # Operation 2
        for d in range(common_depth, len(package_path_parts_list)):
            self.pn_list.append(PackageNode(package_path_parts_list[d], package_path_parts_list[:d + 1]))

        # add md5
        if len(self.pn_list) != 0:
            self.pn_list[-1].md5_list.append(class_md5)
            self.pn_list[-1].weight += class_weight


class DexExtractor:
    """
    DEX Extractor

    """
    def __init__(self, dex_name):
        """
            Init the Feature Extractor

        """
        self.dex_name = dex_name
        # self.dex is an instance of dex_parser.DexFile()
        self.dex = None
        # use as a stack
        self.package_node_list = list()
        # database
        self.db_invoke = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_API_INVOKE)

    def _flush(self):
        self.dex = None

    def get_api_list(self, dex_method, api_list):
        if dex_method.dexCode is None:
            return
        offset = 0
        insns_size = dex_method.dexCode.insnsSize * 4
        while offset < insns_size:
            op_code = int(dex_method.dexCode.insns[offset:offset + 2], 16)
            decoded_instruction = dex_parser.dexDecodeInstruction(self.dex, dex_method.dexCode, offset)
            smali_code = decoded_instruction.smaliCode
            if smali_code is None:
                continue
            offset += decoded_instruction.length

            if smali_code == 'nop':
                break

            if 0x6e <= op_code <= 0x72:
                version_count = self.db_invoke.get(decoded_instruction.getApi)
                if version_count is not None:
                    api_list.append(decoded_instruction.getApi)
        return

    def extract_class(self, dex_class_def_obj):
        class_md5 = hashlib.md5()
        # API List
        #   a list for basestring
        api_list = list()
        # direct methods
        last_method_index = 0
        for k in range(len(dex_class_def_obj.directMethods)):
            current_method_index = last_method_index + dex_class_def_obj.directMethods[k].methodIdx
            last_method_index = current_method_index
            self.get_api_list(dex_class_def_obj.directMethods[k], api_list=api_list)
        # virtual methods
        last_method_index = 0
        for k in range(len(dex_class_def_obj.virtualMethods)):
            current_method_index = last_method_index + dex_class_def_obj.virtualMethods[k].methodIdx
            last_method_index = current_method_index
            self.get_api_list(dex_class_def_obj.virtualMethods[k], api_list=api_list)
        # Use sort to pass the tree construction stage.
        # In this case, we could only use a stack to create the package features.
        api_list.sort()
        for api in api_list:
            class_md5.update(api)
        if not IGNORE_ZERO_API_FILES or len(api_list) != 0:
            # TODO: use database to output this.
            logger.debug("MD5: %s Weight: %-6d ClassName: %s" %
                         (class_md5.hexdigest(), len(api_list), self.dex.getDexTypeId(dex_class_def_obj.classIdx)))
        return len(api_list), class_md5.digest(), class_md5.hexdigest()

    def extract_dex(self):
        # Log Start
        logger.debug("Extracting %s" % self.dex_name)
        # Validate existing
        if not os.path.isfile(self.dex_name):
            logger.error("%s not file" % self.dex_name)
            return -1
        # Create a Dex object
        self.dex = dex_parser.DexFile(self.dex_name)
        pnl = PackageNodeList()
        # Generate Md5 from Dex

        class_info_list = list()
        for dex_class_def_obj in self.dex.dexClassDefList:
            weight, raw_md5, hex_md5 = self.extract_class(dex_class_def_obj=dex_class_def_obj)
            class_name = self.dex.getDexTypeId(dex_class_def_obj.classIdx)
            if IGNORE_ZERO_API_FILES and weight == 0:
                continue
            class_info_list.append((class_name, weight, raw_md5))
        """
            Sort the info list with the package name.
        """
        class_info_list.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        for class_info in class_info_list:
            # logger.debug("class_name %s" % class_name)
            class_name = class_info[0]
            raw_md5 = class_info[2]
            weight = class_info[1]
            last_slash = class_name.rfind('/')
            # If a class belongs to root, just ignore it because it hardly be a library.
            if last_slash == -1:
                continue
            # get the package name
            # for class name Lcom/company/air/R; It's package name is Lcom/company/air
            package_name = class_name[:last_slash]
            pnl.catch_a_class_def(package_name, raw_md5, weight)
            # logger.debug("Class: %s    Hex Md5: %s    Weight: %d" % (class_name, hex_md5, weight))
        # Let PackageNodeList pop all the nodes.
        pnl.catch_a_class_def("", "", 0)
        return 0


if __name__ == "__main__":
    de = DexExtractor("./Data/IntermediateData/air/classes.dex")
    if de.extract_dex() < 0:
        logger.error("Wrong!")
