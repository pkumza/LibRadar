# -*- coding: utf-8 -*-
"""
    DEX Extractor

    This script is used to extract features and other information from DEX files.
    :copyright: (c) 2016 by Zachary Ma
    : Project: LibRadar
"""

import threading
import os.path
from _settings import *


class DexExtractor(threading.Thread):
    """
    DEX Extractor

    """
    def __init__(self, thread_name, dex):
        """
            Init the Feature Extractor

        """
        threading.Thread.__init__(self, name=thread_name)
        self.dex_name = dex
        # Info
        self.string_list = []

    def _flush(self):
        pass

    def run(self):
        logger.debug("Extracting %s" % self.dex_name)
        if not os.path.isfile(self.dex_name):
            print "%s not file" % self.dex_name
            return



if __name__ == "__main__":
    de = DexExtractor("threadname1", "./Data/IntermediateData/air/classes.dex")
    de.start()
    de.join()
