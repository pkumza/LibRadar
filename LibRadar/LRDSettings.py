# -*- coding: utf-8 -*-
"""
    LibRadar settings.py

    Settings about python scripts in LibRadar folder.
    All the scripts in LibRadar need import this file.

"""

import time
import os

"""
    whether clean the workspace after work
        0 : Clean nothing
        1 : Clean res files
        2 : Clean smali files
        3 : Clean everything, including AndroidManifest.xml & apktool.yml
"""
clean_workspace = 0

"""
    Config about databases
        0 : Android.jar Classes
            Key: Classes (Not used)
            Value: Count (Not used)
        1 : Android.jar APIs with return_type and argument_type
            Key: API with return_type and argument_type (Not used)
            Value: Count (Not used)
        2 : Android.jar APIs with only full class name and method name
            Key: API with only class name and method name (Important!!!)
            Value: Count (Not used)
        3 : Feature Count
            Key: Hash (MD5) of a package or smali file
            Value: Count
        4 : Feature Weight
            Key: Hash (MD5) of a package or smali file
            Value: Weigh. Which means how many APIs used in this package or smali file.
        5 : potential un-obfuscated package name
            Key: Hash (MD5) of a package or smali file
            Value: potential package name
        6 : potential un-obfuscated package name count. dynamically calculated.
            If we found a new package with this Hash result and the package name is equal to that one in DB5
                INCR this value
            else
                DECR this value
                if this value < 0
                    Change the package name in DB5 into current package name.
            Key: Hash (MD5) of a package or smali file
            Value: count of potential package name
        7 : A list of APK files that contains this package or smali.
            Key: Hash (MD5) of a package or smali file
            Value: a list of APK file MD5 for this APP
                e.g. "5cbcb2c2248ccdf30aca87612bc7b0de"
        8 : File MD5 to APP Package Name
            Key: APK file MD5
            Value: App's package name
                e.g. 6cc6e58b9229a05f35ae34d05da9f688 -> com.Viserl.FunLiveWallpaper
"""
db_host = 'localhost'
db_port = 6379
db_class_name = 0
db_android_api = 1
db_api_invoke = 2
db_feature_count = 3
db_feature_weight = 4
db_un_ob_pn = 5
db_un_ob_pn_count = 6
db_apk_md5_list = 7
db_md5_to_apk_pn = 8

"""
running_threads
"""
running_threads_number = 4
queue_time_out = 30

"""
    Logs
"""

# log level from 0 to 5
_log_level = 5
if not os.path.exists("./Data"):
    os.mkdir("./Data")
_log_file_name = "./Data/log.txt"
_log_file = open(_log_file_name, 'a')

# This var defines whether we need to re-run the extracting stage when we find the same file MD5 in DB.
repeat_file_rerun = True

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
