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

#   Library tagger
#
#   This script should be an interact-able script.



import redis
import csv
import os.path
from _settings import *


class Tagger:
    """
    Database tagger.

        My algorithm could only tell you that which package is library.
        I could tell you the package name but I don't have specific information like it's real library name, official
        website

    Rule
        A rule is established for tagging libraries.
        As there's many libraries, it could be many Lcom/google/android/gms, it is very hard to tag them one by one.
        So we need a rule file and tag all the libraries with package name started with 'Lcom/google/android/gms' as
        the library GMS.

        Rule information could be taken as a hash table.
        Key:
            package name
        Value:
            Library Name , Library Type, Official Website,
    """
    def __init__(self, base_count=20, base_weight=100):
        self.db = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ID, password=DB_PSWD)
        """
        Rules:
            There would be hundreds of lines of rules. Quite small the file should be.
            Thus I use a **file** rather that put them into database because that will be visible for developers.
            Every time we should import the file into main memory and use a dict for quick access, but it won't take a
              large portion of main memory.
            tag_rules.csv should be less than 100KB.
        """
        self.dict_tag_rules = dict()
        self.new_prefix_list = list()
        if os.path.exists(FILE_RULE):
            file_rules = open(FILE_RULE, 'r')
            csv_rules_reader = csv.reader(file_rules, delimiter=',', quotechar='|')
            for row in csv_rules_reader:
                self.dict_tag_rules[row[0]] = (row[1], row[2], row[3])
            file_rules.close()
        file_rules_w = open(FILE_RULE, 'a')
        self.csv_rule_writer = csv.writer(file_rules_w, delimiter=',', quotechar='|')
        self.base_count = base_count
        self.base_weight = base_weight
        logger.debug("LibRadar Tagger Initiated.")
        self.features = list()

    def get_potential_list(self):
        logger.debug("Searching in database. Need a few seconds.")
        # Yeah, use 'keys' function may block a while, but lib_tagging.py is designed for professional use only.
        # Up to now, do not like to support multi-threading.

        f_cnt = self.db.hgetall(name=DB_FEATURE_CNT)
        f_weight = self.db.hgetall(name=DB_FEATURE_WEIGHT)
        f_un_ob_pn = self.db.hgetall(name=DB_UN_OB_PN)
        for key in f_cnt:
            curr_count = int(f_cnt[key])
            if curr_count < self.base_count:
                continue
            curr_weight = int(f_weight[key])
            if curr_weight < self.base_weight:
                continue
            # sha256, count, weight, pn
            self.features.append((key, curr_count, curr_weight, f_un_ob_pn[key]))
        # sort with count and weight
        # count is more important so I gave it 3 times weight.
        self.features.sort(cmp=lambda x, y: cmp(y[1]*3 + y[2], x[1] * 3 + x[2]))
        return self.features

    def set_rule(self, ipt_pn, ipt_real_name, ipt_type, ipt_website):
        self.csv_rule_writer.writerow([ipt_pn, ipt_real_name, ipt_type, ipt_website])
        # use for ignore libs that already tagged.
        self.dict_tag_rules[ipt_pn] = (ipt_real_name, ipt_type, ipt_website)

    def exist(self, full_package_name):
        flag = False
        for key_pn in self.dict_tag_rules:
            if key_pn == full_package_name[:len(key_pn)]:
                flag = True
                break
        return flag


class TaggerCli:
    def __init__(self):
        self._print_title()
        self._set_base()
        self._tag()

    @staticmethod
    def _print_title():
        print("|---- LibRadar Tagging System -----|")
        print("|      Version: 2.0.1.dev1         |")
        print("|      Author:  Zachary Ma         |")
        print("|----------------------------------|")

    def _set_base(self):
        """
        Option settings.
        """
        """
            ignore 'only tag new' option

        only_tag_new = True
        while True:
            try:
                only_tag_new_option = raw_input("Only tag libraries that have not been tagged (Y/N): ")
                if only_tag_new_option == "N" or only_tag_new_option == "n":
                    only_tag_new = False
                    break
                if only_tag_new_option == "Y" or only_tag_new_option == "y":
                    only_tag_new = True
                    break
                print("Sorry, I'm not sure what you mean.")
            except:
                continue
        """
        base_count = -1
        base_weight = -1
        try:
            base_count = input("Set the minimum number of repetitions (Default 20): ")
        except NameError:
            base_count = 20
        except SyntaxError:
            base_count = 20
        finally:
            print("The minimum number of repetitions is set as %d." % base_count)
        try:
            base_weight = input("Set the minimum API count of libraries (Default 100): ")
        except NameError:
            base_weight = 100
        except SyntaxError:
            base_weight = 100
        finally:
            print("The minimum API count of library is set as %d" % base_weight)
        self.tagger = Tagger(base_count, base_weight)

    def _tag(self):
        self.features = self.tagger.get_potential_list()
        # Print length of features
        feature_num = len(self.features)
        feature_iterator = 0
        print("There're %d features need to be tagged" % feature_num)
        while True:
            if feature_iterator >= feature_num:
                break
            # If already tagged:
            if self.tagger.exist(self.features[feature_iterator][3]):
                print("  Ignore %d %s" % (feature_iterator + 1, self.features[feature_iterator][3]))
                feature_iterator += 1
                continue
            # If not tagged.
            print("-" * 60)
            print("# Tagging %d/%d." % (feature_iterator + 1, feature_num))
            print("  Potential Package Name: %s" % self.features[feature_iterator][3])
            print("  Number of repetitions: %s" % self.features[feature_iterator][1])
            print("  API contains: %s" % self.features[feature_iterator][2])
            print("-" * 60)
            ipt_know = raw_input("Do you know this library? (Y:Yes/ N:No/ W: It's not a library!)")
            if ipt_know == 'N' or ipt_know == 'n':
                print("OK, next one.")
                feature_iterator += 1
                continue
            if ipt_know == 'W' or ipt_know == 'w':
                print("OK, next one.")
                feature_iterator += 1
            if ipt_know != 'Y' and ipt_know != 'y':
                print("Sorry? I don't know what you mean.")
                continue
            ipt_pn = raw_input("Please input its true package name: ")
            # input longer warning!
            if len(ipt_pn) > len(self.features[feature_iterator][3]):
                logger.warning("Input longer that the original potential package name???")
                ipt_re = raw_input("Insist(Y/N).")
                if ipt_re == 'N' or ipt_re == 'n':
                    continue
            # prefix not the same warning!
            if self.features[feature_iterator][3][:len(ipt_pn)] != ipt_pn:
                logger.warning("Prefix not the same??? %s,%s" % (self.features[feature_iterator][3], ipt_pn))
                ipt_re = raw_input("Insist(Y/N).")
                if ipt_re == 'N' or ipt_re == 'n':
                    continue
            # Real Name
            ipt_real_name = raw_input("Input Library's real name: ")
            # type
            ipt_lib_type = raw_input("Input Library Type: ")
            # Official website
            ipt_website = raw_input("Input Official Website: ")
            self.tagger.set_rule(ipt_pn, ipt_real_name, ipt_lib_type, ipt_website)

            # Next
            feature_iterator += 1
