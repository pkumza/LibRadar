# -*- coding: utf-8 -*-
"""
    LibRadar

    main function for instant detecting use.

"""

import sys
from _settings import *
import dex_tree
import hashlib
import zipfile

class LibRadar(object):
    """
    LibRadar
    """
    def __init__(self, apk_path):
        self.apk_path = apk_path

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
        dex_file_extracted = zf.extract("classes.dex", "Data/Decompiled/%s" % self.hex_md5)
        return dex_file_extracted

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



if __name__ == '__main__':
    apk_path = sys.argv[1]
    libradar = LibRadar(apk_path)
    print "unzip: " + libradar.unzip()

