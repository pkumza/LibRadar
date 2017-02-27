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


#   LibRadar brand_lib.py
#
#   When you find an APK file has a lib, but you could not find it in my database, you could just use this script to
#   insert it into database with force.

import sys
from _settings import *
import dex_tree
import dex_parser
import hashlib
import zipfile
import json
import libradar


class BrandLib(libradar.LibRadar):
    """
    BrandLib
    """
    def __init__(self, apk_path, lib_package):
        """
        Init LibRadar instance with apk_path as a basestring.
        Create a Tree for every LibRadar instance. The tree describe the architecture of the apk. Every package is a
        node.
        :param apk_path: basestring
        """
        libradar.LibRadar.__init__(self, apk_path)
        self.lib_package = lib_package

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
    if len(sys.argv) != 3:
        print("Brand_lib takes 2 parameters!")
        exit(1)
    apk_path = sys.argv[1]
    lib_package = sys.argv[2]
    brand_lib = BrandLib(apk_path, lib_package)
    res = brand_lib.analyse()
    print(json.dumps(res, indent=4, sort_keys=True))
