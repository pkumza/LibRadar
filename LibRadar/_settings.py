# -*- coding: utf-8 -*-
"""
    LibRadar settings.py

    Settings about python scripts in LibRadar folder.
    All the scripts in LibRadar need import this file.

"""

import os
import logging.config

"""
    whether clean the workspace after work
        0 : Clean nothing
        1 : Clean res files
        2 : Clean smali files
        3 : Clean everything, including AndroidManifest.xml & apktool.yml
"""
CLEAN_WORKSPACE = 0

"""
    Config about databases

        @deprecated 0 : Android.jar Classes
            Key: Classes (Not used)
            Value: Count (Not used)
        @deprecated 1 : Android.jar APIs with return_type and argument_type
            Key: API with return_type and argument_type (Not used)
            Value: Count (Not used)
        @deprecated 2 : Android.jar APIs with only full class name and method name
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
        9 : Tag
            Key: Hash (MD5) of a package
            Value: Tag
        10: Rule
            Key: prefix of library package name
            Value: Library Name; Library Type; Official Website
"""
DB_HOST = 'localhost'
DB_PORT = 6379
DB_CLASS_NAME = 0
DB_ANDROID_API = 1
DB_API_INVOKE = 2
DB_FEATURE_COUNT = 3
DB_FEATURE_WEIGHT = 4
DB_UN_OB_PN = 5
DB_UN_OB_PN_COUNT = 6
DB_APK_MD5_LIST = 7
DB_MD5_TO_APK_PN = 8
DB_TAG = 9
DB_RULE = 10

"""
    running_processes

    Use multi-processing could fully use the cores of cpu.
    Once I set QUEUE_TIME_OUT 5. After about two hours, three processes returns. So it should be little longer.
    I set it 30 yesterday and in two hours' processing, every process runs well.
"""
RUNNING_PROCESS_NUMBER = 8
QUEUE_TIME_OUT = 30


"""
IGNORE ZERO API FILES

    If there's no API in a class file, just ignore it.
    If there's no API in a package, just ignore it.
"""
IGNORE_ZERO_API_FILES = True

"""
Config Files
"""
FILE_LOGGING = 'LibRadar/logging.conf'
FILE_RULE = 'Data/IntermediateData/tag_rules.csv'

"""
    Logs
"""

if not os.path.exists("./Data"):
    os.mkdir("./Data")
logging.config.fileConfig(FILE_LOGGING)
# create logger
logger = logging.getLogger('radar')
