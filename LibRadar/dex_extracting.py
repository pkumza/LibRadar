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
import redis
import dex_parser
from _settings import *


class PackageNode:
    """
        PackageNode
            Every Node of PackageNodeList is an instance of PackageNode.

        contains:
            md5_list: children's md5
                the md5 feature of current node is based on md5 from children.
                sort children's md5 and then generate its own md5 feature.

            path: the path is current packages' folder's name.
                e.g. Lcom/google/ads 's path is "ads"

            full_path: It is easy to imaging that full path of Lcom/google/ads is Lcom/google/ads

            weight: How many APIs are used in this package.
    """
    def __init__(self, path, full_path):
        """
            Init PackageNode with path
            Weight and md5 list are initiated as empty.
        :param path: basestring
        :param full_path: basestring
        """
        self.md5_list = list()
        self.path = path
        self.full_path = full_path
        self.weight = 0

    def generate_md5(self):
        """
            Generate Md5 of current node based on children's md5.
        :return: current Node's raw_md5 and weight.
        """
        curr_md5 = hashlib.md5()
        self.md5_list.sort()
        for md5_item in self.md5_list:
            curr_md5.update(md5_item)
        # TODO: Currently do not put class into database.
        # if not IGNORE_ZERO_API_FILES or len(self.md5_list) != 0:
        #    logger.debug("MD5: %s Weight: %-6d PackageName: %s" %
        #                 (curr_md5.hexdigest(), self.weight, '/'.join(self.full_path)))
        return curr_md5.digest(), self.weight


class PackageNodeList:
    """
        A list (could be token as a stack) of PackageNodes.
        Used to implement the algorithm in introduction.

        One instance for one DexExtractor
    """
    def __init__(self):
        self.pn_list = list()
        self.db_feature_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_COUNT)
        self.db_feature_weight = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_WEIGHT)
        self.db_un_ob_pn = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN)
        self.db_un_ob_pn_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN_COUNT)
        # TODO: apk md5 list didn't used.
        # If every package contains a list of apk, it consumes a lot.
        # It's only use for research but in fact it's no use for LibRadar the project itself.
        self.db_apk_md5_list = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_APK_MD5_LIST)

    def flush_db(self):
        """
        Flush databases
        :return: None
        """
        certain_flush = raw_input("You really want to flush database?(Y/N)")
        if certain_flush != "Y":
            logger.info("Do not flush.")
            return
        logger.warning("Flush 5 Databases")
        self.db_feature_count.flushdb()
        self.db_feature_weight.flushdb()
        self.db_un_ob_pn.flushdb()
        self.db_un_ob_pn_count.flushdb()
        self.db_apk_md5_list.flushdb()

    def flush_all(self):
        """
        Flush databases
        :return: None
        """
        certain_flush = raw_input("You really want to flush all databases?(Y/N)")
        if certain_flush != "Y":
            logger.info("Do not flush.")
            return
        logger.warning("Flush All Databases")
        self.db_apk_md5_list.flushall()

    def catch_a_class_def(self, package_name, class_md5, class_weight):
        """
        catch a class definition

        Class definitions are sorted.
        Every time this function catch a new class definition.
        It got the class's package name, md5 and class weight(API count)

        :param package_name: basestring
        :param class_md5: basestring
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
            child_md5, curr_weight = stage_to_be_pop.generate_md5()
            if len(self.pn_list) > 1:
                stage_to_be_update = self.pn_list[-2]
                stage_to_be_update.md5_list.append(child_md5)
                stage_to_be_update.weight += curr_weight
            package_exist = self.db_feature_count.get(name=child_md5)
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
            # TODO: Should use pipe and scan_iter to modify the efficiency.
            if package_exist is None:
                self.db_feature_count.incr(name=child_md5, amount=1)
                self.db_feature_weight.set(name=child_md5, value=curr_weight)
                self.db_un_ob_pn.set(name=child_md5, value='/'.join(stage_to_be_pop.full_path))
                self.db_un_ob_pn_count.incr(name=child_md5, amount=1)
            else:
                self.db_feature_count.incr(name=child_md5, amount=1)
                db_un_ob_pn = self.db_un_ob_pn.get(name=child_md5)
                if db_un_ob_pn is None:
                    logger.error("db_un_ob_pn should not be None here.")
                if '/'.join(stage_to_be_pop.full_path) == db_un_ob_pn:
                    self.db_un_ob_pn_count.incr(name=child_md5, amount=1)
                else:
                    self.db_un_ob_pn_count.decr(name=child_md5, amount=1)
                    db_un_ob_pn_count = self.db_un_ob_pn_count.get(name=child_md5)
                    if db_un_ob_pn_count is None:
                        logger.error("db_un_ob_pn_count should not be None here.")
                    if int(db_un_ob_pn_count) <= 0:
                        self.db_un_ob_pn.set(name=child_md5, value='/'.join(stage_to_be_pop.full_path))
                        # forget to reset the count, which caused some count appears to be negative number.
                        self.db_un_ob_pn_count.set(name=child_md5, value=0)
            # TODO: APK List
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
        invoke_file = open("./Data/IntermediateData/invokeFormat.txt", 'r')
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
            pass
            # TODO: use database to output this.
            # logger.debug("MD5: %s Weight: %-6d ClassName: %s" %
            #              (class_md5.hexdigest(), len(api_list), self.dex.getDexTypeId(dex_class_def_obj.classIdx)))
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
    # A test for dex extractor here.
    logger.critical(" ------------------------- START ------------------------- ")
    de = DexExtractor("./Data/IntermediateData/air/classes.dex")
    if de.extract_dex() < 0:
        logger.error("Wrong!")
    logger.critical(" -------------------------- END -------------------------- ")
    # os.system("eject cdrom")
