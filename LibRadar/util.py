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
