# -*- coding: utf-8 -*-
"""
    dispatcher
        Android Package Extractor Dispatcher
    This script is a dispatcher for scheduling.
"""

import threading
import glob
from Queue import Queue
from _settings import *
import app_extracting


class AEDispatcher:
    """
    AED
    """
    def __init__(self, folder_full_of_apps):
        self.folder = folder_full_of_apps
        self.app_list = glob.glob("%s/*" % folder_full_of_apps)

    def run(self):
        queue = Queue()
        for app in self.app_list:
            queue.put(app)
        thread_list = list()
        for i in range(running_threads_number):
            thread_name = str(i).zfill(4)
            ae_thread = app_extracting.APKExtractor(thread_name, queue)
            thread_list.append(ae_thread)
        for one_thread in thread_list:
            one_thread.start()
            logger.info("Ignite thread %s" % one_thread.thread_name)
        for one_thread in thread_list:
            one_thread.join()
            logger.info("Reap thread %s" % one_thread.thread_name)

if __name__ == "__main__":
    aed = AEDispatcher("")
    aed.run()

