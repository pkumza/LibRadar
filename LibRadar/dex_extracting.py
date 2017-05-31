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


#   DEX Extractor
#
#   This script is used to extract features and other information from DEX files.
#   :copyright: (c) 2016 by Zachary Ma
#   : Project: LibRadar
#
#   Target:
#       Get a dex file
#       Generate features from the dex file.
#       Get the features of classes and packages.
#
#   Implementation:
#       Firstly, get class defines from dex file.
#       For each class, we could generate it's APIs and so as the sha256 feature.
#       As the class definition contains the path, so we could construct a tree for the classes.
#
#       e.g.
#
#                     root
#                     /   \
#               android   com
#                 /       /  \
#             support  google facebook
#               /       /   \      \
#              v4     gson  ads    c.class
#              |       |      \
#            media   e.class  purchase
#            /    \              |
#        a.class  b.class       d.class
#
#       For every package, we generate features based on it's child.
#       for example, the feature of /android/support/v4/media is based on a.class and b.class.
#       If we need to generate features of all packages, we could construct a tree for them.
#       To minimize the complexity, and avoid constructing the tree, I sorted the class defines first.
#
#       android/support/v4/media/a
#       android/support/v4/media/b
#       com/facebook/c
#       com/google/ads/purchase/d
#       com/google/gson/e
#
#       It's like an in-order traversal for this tree:
#
#       Create a stack for this. (Type: PackageNode)
#       Scan android/support/v4/media/a and put 'android', 'support', 'v4', 'media' into the stack.
#       Get the feature of a.class
#       Update media's feature
#       Get the feature of b.class
#       Update media's feature
#       Get the feature of c.class
#       Pop media and put the feature into db
#       Update and pop v4      and put the feature into db
#       Update and pop support and put the feature into db
#       Update and pop android and put the feature into db
#       Push com
#       Push facebook
#       Update facebook with c.class
#       Pop facebook
#       Push google
#       Push ads
#       Push purchase
#       Update Purchase's feature with d
#       Pop Purchase
#       Pop ads
#       Push gson
#       Update gson with e
#       Pop gson
#       Update and pop google
#       Update and pop com


import os.path
import hashlib
import redis
import dex_parser
import time
from _settings import *
import sys


class PackageNode:
    """
        PackageNode
            Every Node of PackageNodeList is an instance of PackageNode.

        contains:
            sha256_list: children's sha256
                the sha256 feature of current node is based on sha256 from children.
                sort children's sha256 and then generate its own sha256 feature.

            path: the path is current packages' folder's name.
                e.g. Lcom/google/ads 's path is "ads"

            full_path: It is easy to imaging that full path of Lcom/google/ads is Lcom/google/ads

            weight: How many APIs are used in this package.
    """
    def __init__(self, path, full_path):
        """
            Init PackageNode with path
            Weight and sha256 list are initiated as empty.
        :param path: basestring
        :param full_path: basestring
        """
        self.sha256_list = list()
        self.path = path
        self.full_path = full_path
        self.weight = 0

    def generate_sha256(self):
        """
            Generate sha256 of current node based on children's sha256.
        :return: current Node's raw_sha256 and weight.
        """
        curr_sha256 = hashlib.sha256()
        self.sha256_list.sort()
        for sha256_item in self.sha256_list:
            curr_sha256.update(sha256_item)
        # if not IGNORE_ZERO_API_FILES or len(self.sha256_list) != 0:
        #    logger.debug("sha256: %s Weight: %-6d PackageName: %s" %
        #                 (curr_sha256.hexdigest(), self.weight, '/'.join(self.full_path)))
        return curr_sha256.hexdigest(), self.weight


class PackageNodeList:
    """
        A list (could be token as a stack) of PackageNodes.
        Used to implement the algorithm in introduction.

        One instance for one DexExtractor
    """
    def __init__(self):
        self.pn_list = list()
        self.db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID, password=DB_PSWD)

    def flush_db(self):
        """
        Flush databases
        :return: None
        """
        certain_flush = raw_input("You really want to flush database?(Y/N)")
        if certain_flush != "Y":
            logger.info("Do not flush.")
            return
        logger.warning("Flush Database")
        self.db.flushdb()

    def catch_a_class_def(self, package_name, class_sha256, class_weight):
        """
        catch a class definition

        Class definitions are sorted.
        Every time this function catch a new class definition.
        It got the class's package name, sha256 and class weight(API count)

        :param package_name: basestring
        :param class_sha256: basestring
        :param class_weight: int
        :return: None
        """
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
            child_sha256, curr_weight = stage_to_be_pop.generate_sha256()
            if len(self.pn_list) > 1:
                stage_to_be_update = self.pn_list[-2]
                stage_to_be_update.sha256_list.append(child_sha256)
                stage_to_be_update.weight += curr_weight
            package_exist = self.db.hget(DB_FEATURE_CNT, child_sha256)
            """
                If there's no instance in database.
                    incr count
                    set weight
                    set un ob pn
                    un ob pn count incr
                Else
                    incr count
                    If un ob pn == current pn
                        un ob pn count incr
                    Else
                        un ob pn count decr
                        if un ob pn count <= 0
                            un ob pn = current pn
            """
            while True:
                pipe = self.db.pipeline(transaction=False)
                if package_exist is None:
                    pipe.hincrby(name=DB_FEATURE_CNT, key=child_sha256, amount=1)
                    pipe.hset(name=DB_FEATURE_WEIGHT, key=child_sha256, value=curr_weight)
                    pipe.hset(name=DB_UN_OB_PN, key=child_sha256, value='/'.join(stage_to_be_pop.full_path))
                    pipe.hset(name=DB_UN_OB_CNT, key=child_sha256, value=1)
                else:
                    pipe.hincrby(name=DB_FEATURE_CNT, key=child_sha256, amount=1)
                    db_un_ob_pn = self.db.hget(name=DB_UN_OB_PN, key=child_sha256)
                    if db_un_ob_pn is None:
                        logger.error("db_un_ob_pn should not be None here.")
                    if '/'.join(stage_to_be_pop.full_path) == db_un_ob_pn:
                        pipe.hincrby(name=DB_UN_OB_CNT, key=child_sha256, amount=1)
                    else:
                        pipe.hincrby(name=DB_UN_OB_CNT, key=child_sha256, amount=-1)
                        db_un_ob_pn_count = self.db.hget(name=DB_UN_OB_CNT, key=child_sha256)
                        if db_un_ob_pn_count is None:
                            logger.error("db_un_ob_pn_count should not be None here.")
                        if int(db_un_ob_pn_count) <= 0:
                            pipe.hset(name=DB_UN_OB_PN, key=child_sha256, value='/'.join(stage_to_be_pop.full_path))
                            # forget to reset the count, which caused some count appears to be negative number.
                            pipe.hset(name=DB_UN_OB_CNT, key=child_sha256, value=0)
                pipe.execute()
                break
            self.pn_list.pop()
        # Operation 2
        for d in range(common_depth, len(package_path_parts_list)):
            self.pn_list.append(PackageNode(package_path_parts_list[d], package_path_parts_list[:d + 1]))

        # add sha256
        if len(self.pn_list) != 0:
            self.pn_list[-1].sha256_list.append(class_sha256)
            self.pn_list[-1].weight += class_weight


class DexExtractor:
    """
    DEX Extractor

    """
    def __init__(self, dex_name):
        """
         Init the Feature Extractor
        :param dex_name: basestring
        """
        self.dex_name = dex_name
        # self.dex is an instance of dex_parser.DexFile()
        # clear it here
        self.dex = None
        # use as a stack
        self.package_node_list = list()
        """
            Use redis database to exam whether a call is an Android API consumes 27% running time.
            I think it should be replaced by a hash table as the API list could not be modified during the progress.
        """
        invoke_file = open(SCRIPT_PATH + "/Data/IntermediateData/invokeFormat.txt", 'r')
        self.invokes = set()
        for line in invoke_file:
            self.invokes.add(line[:-1])

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
                logger.warning("smali code is None.")
                if decoded_instruction == 0:
                    break
                else:
                    offset += decoded_instruction.length
                    continue
            # Next Instruction.
            offset += decoded_instruction.length
            if smali_code == 'nop':
                break
            # 4 invokes from 0x6e to 0x72
            if 0x6e <= op_code <= 0x72:
                if decoded_instruction.getApi in self.invokes:
                    api_list.append(decoded_instruction.getApi)
        return

    def extract_class(self, dex_class_def_obj):
        class_sha256 = hashlib.sha256()
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
            class_sha256.update(api)
        if not IGNORE_ZERO_API_FILES or len(api_list) != 0:
            pass
        return len(api_list), class_sha256.hexdigest(), class_sha256.hexdigest()

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
        # Generate sha256 from Dex

        class_info_list = list()
        for dex_class_def_obj in self.dex.dexClassDefList:
            weight, raw_sha256, hex_sha256 = self.extract_class(dex_class_def_obj=dex_class_def_obj)
            class_name = self.dex.getDexTypeId(dex_class_def_obj.classIdx)
            """
            I got many \x01 here before the class name.
                such as '\x01Lcom/vungle/publisher/inject'
            don't know exactly but could use code below to deal with it.
            """
            if class_name[0] is not 'L':
                l_index = class_name.find('L')
                if l_index == '-1':
                    continue
                class_name = class_name[l_index:]
            if IGNORE_ZERO_API_FILES and weight == 0:
                continue
            class_info_list.append((class_name, weight, raw_sha256))
        """
            Sort the info list with the package name.
        """
        class_info_list.sort(cmp=lambda x, y: cmp(x[0], y[0]))
        for class_info in class_info_list:
            # logger.debug("class_name %s" % class_name)
            class_name = class_info[0]
            raw_sha256 = class_info[2]
            weight = class_info[1]
            last_slash = class_name.rfind('/')
            # If a class belongs to root, just ignore it because it hardly be a library.
            if last_slash == -1:
                continue
            # get the package name
            # for class name Lcom/company/air/R; It's package name is Lcom/company/air
            package_name = class_name[:last_slash]
            pnl.catch_a_class_def(package_name, raw_sha256, weight)
        # Let PackageNodeList pop all the nodes.
        pnl.catch_a_class_def("", "", 0)
        return 0


if __name__ == "__main__":
    # A test for dex extractor here.
    assert len(sys.argv) == 2
    logger.critical(" ------------------------- START ------------------------- ")
    de = DexExtractor(sys.argv[1])
    if de.extract_dex() < 0:
        logger.error("Wrong!")
    logger.critical(" -------------------------- END -------------------------- ")
    # os.system("eject cdrom")
