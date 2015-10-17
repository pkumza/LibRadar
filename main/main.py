# -*- coding:utf-8 -*-
# Created at 2015/7/20
# Recently Modified at 2015/10/17
# Current Version 1.2.1

__author__ = 'Zachary Marv - 马子昂'

import sys
import os
from detect import Detector


def main_func(path):
    """
    Detect 3rd-party libraries in app.
    The detection result is printed.
    :param path: The path of target app.
    :return: None.
    """
    print "--Decoding--"
    detector = Detector()
    decoded_path = detector.get_smali(path)
    clean_app_path = detector.get_hash(decoded_path)
    print "--Splitter--"
    print('clean app path : %s' % clean_app_path)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "No apk file name in parameters.\nTry detecting 'Yo.apk' for test."
        main_func("~/Downloads/Yo.apk")
    else:
        print os.path.basename(sys.argv[1])
        main_func(sys.argv[1])
