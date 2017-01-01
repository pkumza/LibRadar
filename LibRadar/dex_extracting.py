# -*- coding: utf-8 -*-
"""
    DEX Extractor

    This script is used to extract features and other information from DEX files.
"""

import threading
import dex_parser
from _settings import *


class DexExtractor(threading.Thread):
    def __init__(self, thread_name, dex):
        """
            Init the Feature Extractor with ID and smali folder's path.
        """
        threading.Thread.__init__(self, name=thread_name)
        self.thread_name = thread_name
        self.dex = dex

    def run(self):
        dex = dex_parser.DexFile(self.dex)
        dex.print_header()
        dex.print_DexStringId()


if __name__ == "__main__":
    de = DexExtractor("T1", "./Data/IntermediateData/air/classes.dex")
    de.run()
