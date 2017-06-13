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

# Utility for repackage detection use

from _settings import *

class Util(object):
    """
    Format of String Storage:

    {1:2}
    |--------|--------|--------|---------|
    |00000000|00000001|00000000|000000010|
    |--------|--------|--------|---------|


    {2:3,4:128}
    |--------|--------|--------|---------|--------|--------|--------|---------|
    |00000000|00000010|00000000|000000011|00000000|00000100|00000000|100000000|
    |--------|--------|--------|---------|--------|--------|--------|---------|

    """
    @staticmethod
    def dict2str(kvd):
        """
        Convert Key-Value Dict to String
        :param kvd: Key-Value Dict
        :return: feature_str String
        """
        feature_str = ""
        assert type(kvd) == dict, 'kvd is a dictionary'
        items = kvd.items()
        items.sort()
        for item in items:
            if type(item[0]) is not int:
                logger.error("Key not int")
            if item[0] >= 256 * 256:
                logger.error("Key too Large")
            s1 = chr(item[0] / 256)
            s2 = chr(item[0] % 256)
            if type(item[1]) is not int:
                logger.error("Value not int.")
            if item[1] >= 256 * 256:
                logger.warning("Value too Large.")
                s3 = chr(255)
                s4 = chr(255)
            else:
                s3 = chr(item[1] / 256)
                s4 = chr(item[1] % 256)
            feature_str += s1 + s2 + s3 + s4
        return feature_str

    @staticmethod
    def str2dict(feature_str):
        """
        Convert String to Key-Value Dict
        :param feature_str:
        :return: kvd
        """
        kvd = dict()
        feature_mod = len(feature_str) % 4
        if feature_mod != 0:
            logger.error("feature_str length is not 4X")
        feature_length = len(feature_str)
        for i in range(0, feature_length, 4):
            i1 = ord(feature_str[i])
            i2 = ord(feature_str[i + 1])
            i3 = ord(feature_str[i + 2])
            i4 = ord(feature_str[i + 3])
            key_int = i1 * 256 + i2
            value_int = i3 * 256 + i4
            kvd[key_int] = value_int
        return kvd

    @staticmethod
    def get_key(feature_str, offset):
        """

        :param feature_str:
        :param offset:
        :return:
        """
        return ord(feature_str[offset]) * 256 + ord(feature_str[offset + 1])

    @staticmethod
    def get_value(feature_str, offset):
        return ord(feature_str[offset + 2]) * 256 + ord(feature_str[offset + 3])

    @staticmethod
    def comp_str(str1, str2):
        assert len(str1) % 4 == 0 and len(str2) % 4 == 0, "Feature_str length is not 4X"
        feature_length1, feature_length2 = len(str1), len(str2)
        cur1, cur2 = 0, 0
        diff = 0
        sum1, sum2 = 0, 0
        while cur1 < feature_length1 or cur2 < feature_length2:
            if cur1 == feature_length1 or Util.get_key(str2, cur2) < Util.get_key(str1, cur1):
                v2 = Util.get_value(str2, cur2)
                sum2 += v2
                diff += v2
                cur2 += 4
                continue
            if cur2 == feature_length2 or Util.get_key(str2, cur2) > Util.get_key(str1, cur1):
                v1 = Util.get_value(str1, cur1)
                sum1 += v1
                diff += v1
                cur1 += 4
                continue
            if Util.get_key(str2, cur2) == Util.get_key(str1, cur1):
                v1 = Util.get_value(str1, cur1)
                v2 = Util.get_value(str2, cur2)
                diff += abs(v1 - v2)
                sum1 += v1
                sum2 += v2
                cur1 += 4
                cur2 += 4
                continue
            assert False, "Not reachable."
        return float(diff) / (sum1 + sum2)
