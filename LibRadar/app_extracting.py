# -*- coding: utf-8 -*-
"""
    APK Extractor

    This script is used to extract features and other information from APK files.
"""

import redis
import hashlib
import threading
from _settings import *
import feature_extracting
# import Queue # ???


class APKExtractor(threading.Thread):
    """
    APK Extractor

    """
    def __init__(self, thread_name, app_queue):
        """
            Init the Feature Extractor with ID and smali folder's path.
        :type thread_name: basestring
        """
        threading.Thread.__init__(self, name=thread_name)
        self.thread_name = thread_name
        self.app_queue = app_queue
        self.APKPath = ""
        self.md5 = ""
        self.package_name = ""
        self.DB_MD5_TO_APK_PN = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_MD5_TO_APK_PN)
        self.decompiled_path = ""

    def get_md5(self):
        if not os.path.isfile(self.APKPath):
            logger.critical("file path %s is not a file" % self.APKPath)
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
        logger.debug("APK %s's MD5 is %s" % (self.APKPath, file_md5_value))
        self.md5 = file_md5_value
        return file_md5_value

    def decompile(self):
        # get md5 for this file.
        self.get_md5()
        package_name_in_db = self.DB_MD5_TO_APK_PN.get(self.md5)
        if package_name_in_db is not None:
            # There's already the same file extracted in database.
            logger.warning("File already in database")
            if False:  # repeated file rerun.
                pass
            else:
                return -1
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
        #
        apktool_cmd = "./tool/apktool d -q -b -o %s %s" % (self.decompiled_path, self.APKPath)
        logger.debug("APKTOOL CMD LINE : %s" % apktool_cmd)
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
            logger.warning("No package name information in manifest file. Use file name instead.")
            self.package_name = apk_file_name
        logger.debug("Package Name of %s is %s" % (self.APKPath, self.package_name))
        # DB 8
        self.DB_MD5_TO_APK_PN.set(self.md5, self.package_name)
        return 0

    def feature_extract(self):
        feature_extractor = feature_extracting.FeatureExtractor("FE_%s" % self.thread_name,
                                                                self.decompiled_path + "/smali",
                                                                self.md5)
        # feature_extractor.flush_feature_db()
        feature_extractor.start()
        feature_extractor.join()
        logger.info("Feature Extractor finished.")

    def clean(self):
        if CLEAN_WORKSPACE == 0:
            return
        if CLEAN_WORKSPACE == 1:
            cmd_rm_assets = "rm -rf %s/assets" % self.decompiled_path
            os.system(cmd_rm_assets)
            cmd_rm_res = "rm -rf %s/res" % self.decompiled_path
            os.system(cmd_rm_res)
            return
        if CLEAN_WORKSPACE == 2:
            cmd_rm_assets = "rm -rf %s/assets" % self.decompiled_path
            os.system(cmd_rm_assets)
            cmd_rm_res = "rm -rf %s/res" % self.decompiled_path
            os.system(cmd_rm_res)
            cmd_rm_smali = "rm -rf %s/smali" % self.decompiled_path
            os.system(cmd_rm_smali)
            return
        if CLEAN_WORKSPACE == 3:
            cmd_rm = "rm -rf %s" % self.decompiled_path
            os.system(cmd_rm)
            return
        logger.critical("Should not arrive here!!! Something wrong with CLEAN_WORKSPACE in _settings.py!!")

    def run(self):
        while True:
            try:
                self.APKPath = self.app_queue.get(block=True, timeout=QUEUE_TIME_OUT)
                logger.info("Thread %s is dealing with %s" % (self.thread_name, self.APKPath))
                if self.decompile() >= 0:
                    # if no error in decompiling
                    self.feature_extract()
                    self.clean()
                else:
                    # if the ret is -1, that means the same file is already extracted.
                    pass
            except:
                # More than QUEUE_TIME_OUT(30) seconds.
                logger.info("No more app needs to be extracted. By thread %s" % self.thread_name)
                break
            finally:
                # Trivial but debug-able: Set APKPath to empty.
                self.APKPath = ""

if __name__ == "__main__":
    ae = APKExtractor("001", "/Volumes/UltraPassport/apks/advanced.speed.booster.apk")
    ae.start()
    ae.join()
