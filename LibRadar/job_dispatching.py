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


#   dispatcher
#       Android Package Extractor Dispatcher
#   This script is a dispatcher for scheduling.


# Step 1 jar 反编译，得到api dict [tech: jad]
# Step 2 hash feature Tree [tech: sha256]
# Step 3 [tech: Redis]
# Step 3.1 [tech: 众数机制]
# Step 3.2 [tech: 分布式、并行]
# Step 3.3 Redis 导出
# Step 4 Detector
# Step 5 online [tech: node.js]

from multiprocessing import Pool
import multiprocessing
import glob
from _settings import *
import hashlib
import zipfile
import dex_extracting
import redis


class DexExtractorWrapper:
    """
        Dex Extractor Wrapper

        Dex Extractor is a class for extracting features from dex file.
        DexExtractorWrapper is a container for the extractor.
        DexExtractorWrapper occupies a process and got a queue from arguments.
        In the main loop, it get an item from the queue and then create a new instance of DexExtractor and run it.
    """
    def __init__(self, p_name, queue):
        """
        Init the instance with process name and queue(full of app path)
        :param p_name: basestring
        :param queue: multiprocessing.Manager().Queue
        """
        self.p_name = p_name
        self.queue = queue
        # MD5 for current app, for the current instance of Dex Extractor
        self.sha256 = ""
        # Path for current app.
        self.app_path = ""

    def execute(self):
        logger.info("Process %s is running" % self.p_name)
        while True:
            try:
                self.app_path = self.queue.get(block=True, timeout=QUEUE_TIME_OUT)
            except: # multiprocessing.Manager().Queue.Empty:
                break
            logger.debug("Process %s is extracting %s" % (self.p_name, self.app_path))
            try:
                self.get_sha256()
            except:
                # Yeah, Too broad exception it is. But I don't care.
                # There could be many types of exception but what I want to do is ignore the wrong apk and focus on
                # the next app.
                logger.error("Process %s get Md5 error!" % self.p_name)
                continue
            # logger.info("Process %s got sha256 %s" % (self.p_name, self.sha256))
            # If the apk file is broken, it can not be unzipped.
            try:
                zf = zipfile.ZipFile(self.app_path, mode="r")
                dex_file_extracted = zf.extract("classes.dex", SCRIPT_PATH + "/Data/Decompiled/%s" % self.sha256)
            except:
                logger.error("Process %s, not a valid Zip file." % self.p_name)
                continue
            try:
                de = dex_extracting.DexExtractor(dex_file_extracted)
                de.extract_dex()
            except:
                logger.critical("Process %s, extracting error!!" % self.p_name)
                continue
            try:
                cmd = 'rm -rf ' + SCRIPT_PATH + "/Data/Decompiled/%s" % self.sha256
                os.system(cmd)
            except:
                logger.error("Process %s, rm error" % self.p_name)
        logger.info("Process %s returns" % self.p_name)

    def get_sha256(self):
        if not os.path.isfile(self.app_path):
            logger.critical("file path %s is not a file" % self.app_path)
            raise AssertionError
        file_sha256 = hashlib.sha256()
        f = file(self.app_path, 'rb')
        while True:
            block = f.read(4096)
            if not block:
                break
            file_sha256.update(block)
        f.close()
        file_sha256_value = file_sha256.hexdigest()
        logger.debug("APK %s's MD5 is %s" % (self.app_path, file_sha256_value))
        self.sha256 = file_sha256_value
        return file_sha256_value


def run_dex_extractor_wrapper(process_name, q):
    dew = DexExtractorWrapper(process_name, q)
    dew.execute()


class DexExtractorDispatcher:
    """
        Dex Extractor Dispatcher
    """
    def __init__(self, folder_full_of_apps):
        self.folder = folder_full_of_apps

    @staticmethod
    def clear_decompiled():
        cmd = 'rm -rf ' + SCRIPT_PATH + '/Data/Decompiled'
        os.system(cmd)

    def execute(self):
        q = multiprocessing.Manager().Queue()
        p = Pool()
        logger.info("Pool created")
        app_list = glob.glob("%s/*" % self.folder)
        for apk in app_list:
            if len(apk) < 4 or apk[-4:] != ".apk":
                continue
            q.put(apk)
        for i in range(RUNNING_PROCESS_NUMBER):
            process_name = str(i).zfill(2)
            p.apply_async(run_dex_extractor_wrapper, args=(process_name, q))
        logger.info("Waiting for all sub-processes done.")
        p.close()
        p.join()
        logger.critical("All sub-processes done.")

if __name__ == "__main__":
    ded = DexExtractorDispatcher("/home/zachary/Projects/apks")
    ded.clear_decompiled()
    ded.execute()
    # q:-)
    # "eject" is just a trick as a reminder. Do not work on Mac obviously. Remove it when necessary.
    # d:-)
    os.system("eject cdrom")
