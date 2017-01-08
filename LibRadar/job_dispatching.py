# -*- coding: utf-8 -*-
"""
    dispatcher
        Android Package Extractor Dispatcher
    This script is a dispatcher for scheduling.
"""

import threading
import glob
import Queue
from _settings import *
import hashlib
import zipfile
import dex_extracting
import redis


class DexExtractorWrapper(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.t_name = t_name
        self.queue = queue
        self.md5 = ""
        self.app_path = ""

    def get_md5(self):
        if not os.path.isfile(self.app_path):
            logger.critical("file path %s is not a file" % self.app_path)
            raise AssertionError
        file_md5 = hashlib.md5()
        f = file(self.app_path, 'rb')
        while True:
            block = f.read(4096)
            if not block:
                break
            file_md5.update(block)
        f.close()
        file_md5_value = file_md5.hexdigest()
        logger.debug("APK %s's MD5 is %s" % (self.app_path, file_md5_value))
        self.md5 = file_md5_value
        return file_md5_value

    def run(self):
        logger.info("Thread %s is running" % self.t_name)
        while True:
            try:
                self.app_path = self.queue.get(block=True, timeout=QUEUE_TIME_OUT)
            except Queue.Empty:
                break
            logger.info("Thread %s is extracting %s" % (self.t_name, self.app_path))
            self.get_md5()
            logger.info("Thread %s got md5 %s" % (self.t_name, self.md5))
            # TODO: Every corner could went wrong. I must wrap everything with 'try'.
            # If the apk file is broken, it can not be unzipped.
            zf = zipfile.ZipFile(self.app_path, mode="r")
            dex_file_extracted = zf.extract("classes.dex", "/dev/shm/Data/Decompiled/%s" % self.md5)
            de = dex_extracting.DexExtractor(dex_file_extracted)
            de.extract_dex()
            cmd = 'rm -rf ' +  "/dev/shm/Data/Decompiled/%s" % self.md5
            os.system(cmd)

        # de = dex_extracting.DexExtractor(dex_name=)


class DexExtractorDispatcher:
    """
        Dex Extractor Dispatcher
    """
    def __init__(self, folder_full_of_apps):
        self.folder = folder_full_of_apps
        self.app_list = glob.glob("%s/*" % folder_full_of_apps)
        self.redis_db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_COUNT)

    def flush_all(self):
        self.redis_db.flushall()

    def clear_decompiled(self):
        cmd = 'rm -rf Data/Decompiled'
        os.system(cmd)

    def execute(self):
        queue = Queue.Queue()
        for apk in self.app_list:
            if len(apk) < 4 or apk[-4:] != ".apk":
                continue
            queue.put(apk)
        for i in range(29):
            queue.get()
        thread_list = list()
        for i in range(RUNNING_THREAD_NUMBER):
            thread_name = str(i).zfill(4)
            de_thread = DexExtractorWrapper(thread_name, queue)
            thread_list.append(de_thread)
        for one_thread in thread_list:
            one_thread.start()
        for one_thread in thread_list:
            one_thread.join()

"""
class AEDispatcher:
    '''
    AED
    '''
    def __init__(self, folder_full_of_apps):
        self.folder = folder_full_of_apps
        self.app_list = glob.glob("%s/*" % folder_full_of_apps)

    def run(self):
        queue = Queue()
        for app in self.app_list:
            queue.put(app)
        thread_list = list()
        for i in range(RUNNING_THREAD_NUMBER):
            thread_name = str(i).zfill(4)
            ae_thread = app_extracting.APKExtractor(thread_name, queue)
            thread_list.append(ae_thread)
        for one_thread in thread_list:
            one_thread.start()
            logger.info("Ignite thread %s" % one_thread.thread_name)
        for one_thread in thread_list:
            one_thread.join()
            logger.info("Reap thread %s" % one_thread.thread_name)
"""


if __name__ == "__main__":
    ded = DexExtractorDispatcher("/home/zachary/Projects/apks")
    ded.flush_all()
    ded.clear_decompiled()
    ded.execute()
    os.system("eject cdrom")

