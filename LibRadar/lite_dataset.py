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

from _settings import *
import redis

THRESHOLD = 10

db = redis.StrictRedis(host=DB_HOST,port=DB_PORT, db=2, password=DB_PSWD)

no_lib_packages = set()

with open("Data/IntermediateData/tag_rules.csv", "r") as rules:
    for line in rules:
        if line.startswith("Package"):
            continue
        pn, lib = line.split(',')[0],line.split(',')[1]
        if lib == "no":
            no_lib_packages.add(pn)

cursor = 0
dataset = open("Data/IntermediateData/lite_dataset_%d.csv" % THRESHOLD, "w")
for i in range(11123):
    if i % 10 == 0:
        print ("Progress:%d" % i)
    res = db.hscan(name="feature_cnt", cursor=cursor, count=1000)
    cursor = res[0]
    for k in res[1]:
        if int(res[1][k]) > THRESHOLD:
            weight = db.hget(name="feature_weight", key=k)
            un_ob_cnt = db.hget(name="un_ob_cnt", key=k)
            if float(un_ob_cnt) / float(res[1][k]) < 0.2:
                continue
            un_ob_pn = db.hget(name="un_ob_pn", key=k)
            if un_ob_pn in no_lib_packages:
                continue
            dataset.write("%s,%s,%s,%s,%s\n" %(k, res[1][k], weight, un_ob_cnt, un_ob_pn))
dataset.close()