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
from _settings import *


class PackageNode:
    def __init__(self, path):
        self.md5 = hashlib.md5()
        self.path = path
        self.weight = 0


class DexExtractor():
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

    def _flush(self):
        self.dex = None

    def dumpDexCode(self, dexMethod, api_list):
        if dexMethod.dexCode == None:
            return
        offset = 0
        insnsSize = dexMethod.dexCode.insnsSize * 4
        weight = 0

        while offset < insnsSize:
            op_code = int(dexMethod.dexCode.insns[offset:offset + 2], 16)
            formatIns, _ = dex_parser.getOpCode(op_code)

            decodedInstruction = dex_parser.dexDecodeInstruction(self.dex, dexMethod.dexCode, offset)

            smaliCode = decodedInstruction.smaliCode
            if smaliCode == None:
                continue
            insns = dexMethod.dexCode.insns[decodedInstruction.offset:decodedInstruction.offset + decodedInstruction.length]
            #print  '    \t%-16s|%04x: %s' % (insns, offset/4, smaliCode)
            offset += decodedInstruction.length

            if smaliCode == 'nop':
                break

            if op_code >= 0x6e and op_code <= 0x72:
                api_list.append(decodedInstruction.getApi)
                weight += 1
        return weight

    def extract_class(self, dex_class_def_obj):
        # print 'classIdx\t= %s\t#%s' % (hex(dex_class_def_obj.classIdx), self.dex.getDexTypeId(dex_class_def_obj.classIdx))
        lastMethodIdx = 0
        # API List
        #   a list for basestring
        api_list = list()
        weight = 0
        for k in range(len(dex_class_def_obj.directMethods)):
            currMethodIdx = lastMethodIdx + dex_class_def_obj.directMethods[k].methodIdx
            dexMethodIdObj = self.dex.DexMethodIdList[currMethodIdx]
            lastMethodIdx = currMethodIdx
            """
            print '    # %s~%s' % (hex(dex_class_def_obj.directMethods[k].offset),
                                   hex(dex_class_def_obj.directMethods[k].offset + dex_class_def_obj.directMethods[k].length))
            print '    DexClassDef[]->DexClassData->directMethods[%d]\t= %s\t#%s' % ( k, dexMethodIdObj.toString(self.dex), dex_class_def_obj.directMethods[k])
            """
            self.dumpDexCode(dex_class_def_obj.directMethods[k], api_list=api_list)
            # print '    ------------------------------------------------------------------------'

        lastMethodIdx = 0
        for k in range(len(dex_class_def_obj.virtualMethods)):
            currMethodIdx = lastMethodIdx + dex_class_def_obj.virtualMethods[k].methodIdx
            dexMethodIdObj = self.dex.DexMethodIdList[currMethodIdx]
            lastMethodIdx = currMethodIdx
            """
            print '    # %s~%s' % (hex(dex_class_def_obj.virtualMethods[k].offset),
                                   hex(dex_class_def_obj.virtualMethods[k].offset + dex_class_def_obj.virtualMethods[k].length))
            print '    DexClassDef[]->DexClassData->virtualMethods[%d]\t= %s\t#%s' % ( k, dexMethodIdObj.toString(self.dex), dex_class_def_obj.virtualMethods[k])
            """
            self.dumpDexCode(dex_class_def_obj.virtualMethods[k], api_list=api_list)
            #print '    ------------------------------------------------------------------------'
        print "LIST:"
        for api in  api_list:
            print api

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
            self.extract_class(dex_class_def_obj=dex_class_def_obj)


if __name__ == "__main__":
    de = DexExtractor("./Data/IntermediateData/air/classes.dex")
    de.run()
