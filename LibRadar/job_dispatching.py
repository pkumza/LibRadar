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

from _settings import *
import redis
import zipfile
import os
import oss2
import dex_extracting

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'LTAI19YfqOSkHpRW')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'pmxBQkjnHYmnTmoExeG5w7Vdk4laMK')
bucket_name = os.getenv('OSS_TEST_BUCKET', 'lxapk')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'vpc100-oss-cn-beijing.aliyuncs.com') # vpc internal!!
# endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-beijing.aliyuncs.com')
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
try:
    db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=0, password=DB_PSWD)
except:
    logging.error("Redis DB connection error!")

while True:
    try:
        item = db.blpop("apk_new_3")[1].split(" ")
        assert(len(item) == 5)
    except:
        logging.error("item get error!")
        continue
    key = '/'.join(item[1:-1]) + '-' + item[-1] + ".apk"
    try:
        if db.sismember("processed_2", key):
            continue
    except:
        logging.error("check is member error")
        continue
    filename = "Data/APK/" + item[-2] + '-' + item[-1] + ".apk"
    try:
        result = bucket.get_object_to_file(key, filename)
    except:
        logging.error("FILE RETRIVE ERROR")
        continue
    try:
        zf = zipfile.ZipFile(filename, mode="r")
        dex_file_extracted = zf.extract("classes.dex", "./Data/Decompiled/%s" % filename)
        cmd = 'rm -rf ' + filename
        os.system(cmd)
    except:
        logging.error("Unzip ERROR")
        continue
    try:
        de = dex_extracting.DexExtractor(dex_file_extracted)
        de.extract_dex()
    except:
        logging.error("DEX EXTRACTING ERROR")
        continue
    try:
        cmd = 'rm -rf ' + 'Data/Decompiled/%s' % filename
        os.system(cmd)
    except:
        logging.error("DEX remove error!")
    db.sadd("processed_2", key)

