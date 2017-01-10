# -*- coding: utf-8 -*-
"""
    Dumping features in database into file for LibRadar Lite (Instant Detection.)

    created at 2017/01/09
"""

import binascii
import redis
from _settings import *


def dump_database():
    db_feature_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_COUNT)
    db_feature_weight = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_WEIGHT)
    db_un_ob_pn = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN)
    dump_file = open("Data/IntermediateData/db_dump.csv", "w")
    # Run once, so do not care the complexity.
    for key in db_feature_count.keys():
        count = db_feature_count.get(key)
        if int(count) <= 4:
            continue
        weight = db_feature_weight.get(key)
        package_name = db_un_ob_pn.get(key)
        dump_file.write("%s;%s;%s;%s\n" %(binascii.hexlify(key), count, weight, package_name))


if __name__ == "__main__":
    dump_database()
