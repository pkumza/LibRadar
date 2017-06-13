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

#   LibRadar settings.py

#   Settings about python scripts in LibRadar folder.
#   All the scripts in LibRadar need import this file.



import os
import logging.config

"""
    whether clean the workspace after work
        0 : Clean nothing
        1 : Clean res files
        2 : Clean smali files
        3 : Clean everything
"""
CLEAN_WORKSPACE = 0

"""
    Database use db 0 as default
"""

DB_HOST = 'localhost'
DB_PORT = 6379
DB_ID = 2
DB_ID_REP = 1
# if you don't have Password, delete DB_PSWD
DB_PSWD = ''

DB_FEATURE_CNT = 'feature_cnt'
DB_FEATURE_WEIGHT = 'feature_weight'
DB_UN_OB_PN = 'un_ob_pn'
DB_UN_OB_CNT = 'un_ob_cnt'


"""
    running_processes

    Use multi-processing could fully use the cores of cpu.
    Once I set QUEUE_TIME_OUT 5. After about two hours, three processes returns. So it should be little longer.
    I set it 30 yesterday and in two hours' processing, every process runs well.
"""
# RUNNING_PROCESS_NUMBER = 8
RUNNING_PROCESS_NUMBER = 1
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

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
if not os.path.exists(SCRIPT_PATH + '/Data'):
    os.mkdir(SCRIPT_PATH + '/Data')
FILE_LOGGING = SCRIPT_PATH + '/Data/logging.conf'
FILE_RULE = SCRIPT_PATH + '/Data/IntermediateData/tag_rules.csv'
LITE_DATASET_10 = SCRIPT_PATH + '/Data/IntermediateData/lite_dataset_10.csv'

"""
    Logs
"""

logging.config.fileConfig(FILE_LOGGING)
# create logger
logger = logging.getLogger('radar')
