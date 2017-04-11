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

#   Dumping features in database into file for LibRadar Lite (Instant Detection.)
#
#   created at 2017/01/09

import binascii
import redis
from _settings import *


# deprecated 2017-04-09
def dump_database():
    pass
    """
    db_feature_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_COUNT)
    db_feature_weight = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_FEATURE_WEIGHT)
    db_un_ob_pn = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_UN_OB_PN)
    dump_file = open(SCRIPT_PATH + "/Data/IntermediateData/db_dump.csv", "w")
    # Run once, so do not care the complexity.
    for key in db_feature_count.keys():
        count = db_feature_count.get(key)
        if int(count) <= 4:
            continue
        weight = db_feature_weight.get(key)
        package_name = db_un_ob_pn.get(key)
        dump_file.write("%s;%s;%s;%s\n" % (binascii.hexlify(key), count, weight, package_name))
    """

if __name__ == "__main__":
    dump_database()
