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

import libradar
import sys


class BrandLib(libradar.LibRadar):
    """
    BrandLib
    """
    def __init__(self, apk_path, lib_package, standard_package):
        """
        Init LibRadar instance with apk_path as a basestring.
        Create a Tree for every LibRadar instance. The tree describe the architecture of the apk. Every package is a
        node.
        :param apk_path: basestring
        """
        libradar.LibRadar.__init__(self, apk_path)
        self.lib_package = lib_package
        self.standard_package = standard_package

    def brand(self):
        # use analyse in libradar.
        # Do not place the same logic in two place!
        self.analyse()
        # brand lib
        return self.tree.brand(self.lib_package, self.standard_package)


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("== Brand_lib takes 2 or 3 parameters! ==")
        print("  Usage 1: not obfuscated package name.")
        print("    python brand_lib.py sample.apk Lcom/google/zxing")
        print("  Usage 2: obfuscated package name.")
        print("    python brand_lib.py sample.apk Lcom/a/a Lcom/tencent/tauth")
        exit(1)
    apk_path = sys.argv[1]
    lib_package = sys.argv[2]
    standard_package = lib_package
    if (len(sys.argv) == 4):
        standard_package = sys.argv[3]
    brand_lib = BrandLib(apk_path, lib_package, standard_package)
    res = brand_lib.brand()
    print(res)
