# -*- coding: utf-8 -*-
"""
    APK Extractor

    This script is used to extract features and other information from APK files.
"""

import os
import redis
import hashlib
import threading
from LRDSettings import *
import FeatureExtractor


class APKExtractor(threading.Thread):
    """
    APK Extractor

    """
    def __init__(self, thread_name, apk_path):
        """
            Init the Feature Extractor with ID and smali folder's path.
        :type thread_name: basestring
        :type apk_path: basestring
        """
        threading.Thread.__init__(self, name=thread_name)
        self.thread_name = thread_name
        self.APKPath = apk_path
        self.md5 = ""
        self.package_name = ""
        self.db_un_ob_pn = redis.StrictRedis(host=db_host, port=db_port, db=db_un_ob_pn)
        self.db_un_ob_pn_count = redis.StrictRedis(host=db_host, port=db_port, db=db_un_ob_pn_count)
        self.db_apk_list = redis.StrictRedis(host=db_host, port=db_port, db=db_apk_list)
        self.decompiled_path = ""

    def get_md5(self):
        if not os.path.isfile(self.APKPath):
            log_e("file path %s is not a file" % self.APKPath)
            raise AssertionError
        file_md5 = hashlib.md5()
        f = file(self.APKPath, 'rb')
        while True:
            block = f.read(4096)
            if not block:
                break
            file_md5.update(block)
        f.close()
        file_md5_value = file_md5.hexdigest()
        log_v("APK %s's MD5 is %s" % (self.APKPath, file_md5_value))
        self.md5 = file_md5_value
        return file_md5_value

    def decompile(self):
        # get md5 for this file.
        self.get_md5()
        # get the basename for the location of decompiling
        apk_file_name = os.path.basename(self.APKPath)
        if os.path.exists("./Data/Decompiled/%s" % apk_file_name):
            repeat_id = 1
            while os.path.exists("./Data/Decompiled/%s-%d" % (apk_file_name, repeat_id)):
                repeat_id += 1
            self.decompiled_path = "./Data/Decompiled/%s-%d" % (apk_file_name, repeat_id)
        else:
            self.decompiled_path = "./Data/Decompiled/%s" % apk_file_name
        # command line for terminal
        apktool_cmd = "./tool/apktool d -q -b -o %s %s" % (self.decompiled_path, self.APKPath)
        log_v("APKTOOL CMD LINE : %s" % apktool_cmd)
        # run cmd
        os.system(apktool_cmd)
        # extract features from AndroidManifest.xml
        manifest_file = open("%s/AndroidManifest.xml" % self.decompiled_path, 'r')
        self.package_name = ""
        for line in manifest_file:
            if "manifest" in line and "package=" in line:
                left_point = line.find("package=") + 9
                right_point = line[left_point:].find('"')
                self.package_name = line[left_point:left_point + right_point]
                break
        if self.package_name == "":
            log_w("No package name information in manifest file. Use file name instead.")
            self.package_name = apk_file_name
        log_v("Package Name of %s is %s" % (self.APKPath, self.package_name))

    def feature_extract(self):
        feature_extractor = FeatureExtractor.FeatureExtractor(self.thread_name + "_FE", self.decompiled_path + "/smali")
        feature_extractor.start()
        feature_extractor.join()
        log_i("Feature Extractor finished.")

    def run(self):
        log_i("Thread %s is dealing with %s" % (self.thread_name, self.APKPath))
        self.decompile()
        self.feature_extract()

ae = APKExtractor("001", "/Users/marchon/Downloads/air.com.dpflashes.clearvision3.apk")
ae.start()
ae.join()
