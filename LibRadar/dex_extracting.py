# -*- coding: utf-8 -*-
"""
    DEX Extractor

    This script is used to extract features and other information from DEX files.
    :copyright: (c) 2016 by Zachary Ma
    : Project: LibRadar
"""

import os.path
import hashlib
import dex_parser
import redis
from _settings import *


class PackageNode:
    def __init__(self, path):
        self.md5 = hashlib.md5()
        self.path = path
        self.weight = 0


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
        self.db_invoke = redis.StrictRedis(host=db_host, port=db_port, db=db_api_invoke)

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
            # insns = dex_method.dexCode.insns[decoded_instruction.offset:decoded_instruction.offset
            #                                                            + decoded_instruction.length]
            # print  '    \t%-16s|%04x: %s' % (insns, offset/4, smali_code)
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
        # print 'classIdx\t= %s\t#%s' % (hex(dex_class_def_obj.classIdx),
        #  self.dex.getDexTypeId(dex_class_def_obj.classIdx))
        last_method_index = 0
        # API List
        #   a list for basestring
        api_list = list()
        for k in range(len(dex_class_def_obj.directMethods)):
            current_method_index = last_method_index + dex_class_def_obj.directMethods[k].methodIdx
            # dex_methodIdObj = self.dex.dex_methodIdList[current_method_index]
            last_method_index = current_method_index
            """
            print '    # %s~%s' % (hex(dex_class_def_obj.directMethods[k].offset),
                                   hex(dex_class_def_obj.directMethods[k].offset +
                                    dex_class_def_obj.directMethods[k].length))
            print '    DexClassDef[]->DexClassData->directMethods[%d]\t= %s\t#%s' %
             ( k, dex_methodIdObj.toString(self.dex), dex_class_def_obj.directMethods[k])
            """
            self.get_api_list(dex_class_def_obj.directMethods[k], api_list=api_list)
            # print '    ------------------------------------------------------------------------'

        last_method_index = 0
        for k in range(len(dex_class_def_obj.virtualMethods)):
            current_method_index = last_method_index + dex_class_def_obj.virtualMethods[k].methodIdx
            # dex_methodIdObj = self.dex.dex_methodIdList[current_method_index]
            last_method_index = current_method_index
            """
            print '    # %s~%s' % (hex(dex_class_def_obj.virtualMethods[k].offset),
                                   hex(dex_class_def_obj.virtualMethods[k].offset +
                                    dex_class_def_obj.virtualMethods[k].length))
            print '    DexClassDef[]->DexClassData->virtualMethods[%d]\t= %s\t#%s' %
             ( k, dex_methodIdObj.toString(self.dex), dex_class_def_obj.virtualMethods[k])
            """
            self.get_api_list(dex_class_def_obj.virtualMethods[k], api_list=api_list)
            # print '    ------------------------------------------------------------------------'
        """
        print "LIST:"
        for api in  api_list:
            print api
        """
        api_list.sort()
        for api in api_list:
            class_md5.update(api)
        return class_md5.digest(), class_md5.hexdigest()

    def run(self):
        # Log Start
        logger.debug("Extracting %s" % self.dex_name)
        # Validate existing
        if not os.path.isfile(self.dex_name):
            print "%s not file" % self.dex_name
            return
        # Create a Dex object
        self.dex = dex_parser.DexFile(self.dex_name)
        # Generate Md5 from Dex
        for dex_class_def_obj in self.dex.dexClassDefList:
            print
            raw_md5, hex_md5 = self.extract_class(dex_class_def_obj=dex_class_def_obj)
            print raw_md5
            print hex_md5
            print len(raw_md5)


if __name__ == "__main__":
    de = DexExtractor("./Data/IntermediateData/air/classes.dex")
    de.run()
