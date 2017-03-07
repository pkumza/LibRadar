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


#   LibRadar
#
#   main function for instant detection.


import sys
from _settings import *
import dex_tree
import dex_parser
import hashlib
import zipfile
import json

class LibRadar(object):
    """
    LibRadar
    """
    def __init__(self, apk_path):
        """
        Init LibRadar instance with apk_path as a basestring.
        Create a Tree for every LibRadar instance. The tree describe the architecture of the apk. Every package is a
        node.
        :param apk_path: basestring
        """
        self.apk_path = apk_path
        self.tree = dex_tree.Tree()
        self.dex_name = ""
        # Instance of Dex Object in dex_parser.
        self.dex = None
        """
            Use redis database to exam whether a call is an Android API consumes 27% running time.
            I think it should be replaced by a hash table as the API list could not be modified during the progress.
        """
        self.k_api_v_permission = dict()
        with open(SCRIPT_PATH + "/Data/IntermediateData/strict_api.csv", 'r') as api_and_permission:
            for line in api_and_permission:
                api, permission_with_colon = line.split(",")
                permissions = permission_with_colon[:-2].split(":")
                # delete the last empty one
                permission_list = list()
                for permission in permissions:
                    if permission != "":
                        permission_list.append(permission)
                self.k_api_v_permission[api] = permission_list
        """
        invoke_file = open(SCRIPT_PATH +"/Data/IntermediateData/invokeFormat.txt", 'r')
        self.invokes = set()
        for line in invoke_file:
            self.invokes.add(line[:-1])
        """

    def __del__(self):
        # Delete dex file
        if CLEAN_WORKSPACE >= 3:
            os.remove(self.dex_name)
            os.removedirs(self.dex_name[:-12])

    def unzip(self):
        # If it is a valid file
        if not os.path.isfile(self.apk_path):
            logger.error("%s is not a valid file." % self.apk_path)
            raise AssertionError
        # If it is a apk file
        if len(self.apk_path) <= 4 or self.apk_path[-4:] != ".apk":
            logger.error("%s is not a apk file.")
            raise AssertionError
        # Get Md5
        self.hex_md5 = self.get_md5()
        # Unzip
        zf = zipfile.ZipFile(self.apk_path, mode='r')
        # Transfer the unzipped dex file name to self.dex_name
        self.dex_name = zf.extract("classes.dex", SCRIPT_PATH + "/Data/Decompiled/%s" % self.hex_md5)
        return self.dex_name

    def get_md5(self):
        if not os.path.isfile(self.apk_path):
            logger.critical("file path %s is not a file" % self.apk_path)
            raise AssertionError
        file_md5 = hashlib.md5()
        f = file(self.apk_path, 'rb')
        while True:
            block = f.read(4096)
            if not block:
                break
            file_md5.update(block)
        f.close()
        file_md5_value = file_md5.hexdigest()
        logger.debug("APK %s's MD5 is %s" % (self.apk_path, file_md5_value))
        return file_md5_value

    def get_api_list(self, dex_method, api_list, permission_list):
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
                if decoded_instruction.getApi in self.k_api_v_permission:
                    api_list.append(decoded_instruction.getApi)
                    for permission in self.k_api_v_permission[decoded_instruction.getApi]:
                        permission_list.add(permission)
        return

    def extract_class(self, dex_class_def_obj):
        class_md5 = hashlib.md5()
        # API List
        #   a list for basestring
        api_list = list()
        permission_list = set()
        # direct methods
        last_method_index = 0
        for k in range(len(dex_class_def_obj.directMethods)):
            current_method_index = last_method_index + dex_class_def_obj.directMethods[k].methodIdx
            last_method_index = current_method_index
            self.get_api_list(dex_class_def_obj.directMethods[k], api_list=api_list, permission_list=permission_list)
        # virtual methods
        last_method_index = 0
        for k in range(len(dex_class_def_obj.virtualMethods)):
            current_method_index = last_method_index + dex_class_def_obj.virtualMethods[k].methodIdx
            last_method_index = current_method_index
            self.get_api_list(dex_class_def_obj.virtualMethods[k], api_list=api_list, permission_list=permission_list)
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
        return len(api_list), class_md5.digest(), class_md5.hexdigest(), sorted(list(permission_list))

    def extract_dex(self):
        # Log Start
        logger.debug("Extracting %s" % self.dex_name)
        # Validate existing
        if not os.path.isfile(self.dex_name):
            logger.error("%s is not a file" % self.dex_name)
            return -1
        # Create a Dex object
        self.dex = dex_parser.DexFile(self.dex_name)
        for dex_class_def_obj in self.dex.dexClassDefList:
            weight, raw_md5, hex_md5, permission_list = self.extract_class(dex_class_def_obj=dex_class_def_obj)
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
            self.tree.insert(package_name=class_name, weight=weight, md5=raw_md5, permission_list=permission_list)
        return 0

    def analyse(self):
        """
        Main function for LibRadar Object.
        :return: None
        """
        # Step 1: Unzip APK file, only extract the dex file.
        self.unzip()
        # Step 2: Extract Dex and insert package-level info into Tree
        self.extract_dex()
        # Step 3: post-order traverse the tree, calculate every package's md5 value.
        self.tree.cal_md5()


    def compare(self):
        self.analyse()
        # Step 4: pre-order traverse the tree, calculate every node's match degree (similarity).
        self.tree.match()
        # Init res for step 5 & 6
        res = list()
        # Step 5: traverse the tree, find out all the libraries.
        self.tree.get_lib(res)
        # Step 6: traverse the tree, find potential libraries that has not been tagged.
        self.tree.find_untagged(res)
        return res



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("LibRadar only takes 1 arguments.")
        print("Usage:")
        print("    $ python libradar.py example.apk")
        exit(1)
    apk_path = sys.argv[1]
    lrd = LibRadar(apk_path)
    res = lrd.compare()
    print(json.dumps(res, indent=4, sort_keys=True))