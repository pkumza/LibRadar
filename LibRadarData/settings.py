# -*- coding: utf-8 -*-
"""
    settings.py

    Settings about python scripts in LibRadarData folder.
    All the scripts in LibRadarData need import this file.

"""

import time

# whether clean the workspace after work
clean_workspace = False

# Config about database
db_host = 'localhost'
db_port = 6379
db_class_name = 0
db_android_api = 1
db_android_api_simplified = 2

"""
    Logs
"""

# log level from 0 to 5
_log_level = 5
_log_file_name = "./Data/log.txt"
_log_file = open(_log_file_name, 'a')


def _log(log_l, message):
    """
    inner log function
    """
    if isinstance(message, basestring):
        log_line = "%s %s %s" % (log_l, time.strftime('%m/%d %H:%M:%S', time.localtime(time.time())), message)
        print(log_line)
        _log_file.write(log_line + '\n')
        _log_file.flush()
    if isinstance(message, int):
        log_line = "%s %s %d" % (log_l, time.strftime('%m/%d %H:%M:%S', time.localtime(time.time())), message)
        print(log_line)
        _log_file.write(log_line + '\n')
        _log_file.flush()
    if isinstance(message, float):
        log_line = "%s %s %f" % (log_l, time.strftime('%m/%d %H:%M:%S', time.localtime(time.time())), message)
        print(log_line)
        _log_file.write(log_line + '\n')
        _log_file.flush()
    '''
    if isinstance(message, tuple):
        print("%s %s" % (log_l, time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))))
        for m in message:
            print(m)
    '''


def log_v(message):
    if _log_level >= 5:
        _log("V", message)


def log_d(message):
    if _log_level >= 4:
        _log("D", message)


def log_i(message):
    if _log_level >= 3:
        _log("I", message)


def log_w(message):
    if _log_level >= 2:
        _log("W", message)


def log_e(message):
    if _log_level >= 1:
        _log("E", message)
