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

import logging
import os
import shutil

rules = []

copy_num = 1
while True:
    if os.path.exists("tag_rules.csv.backup.%d" % copy_num):
        copy_num += 1
        continue
    shutil.copyfile("tag_rules.csv", "tag_rules.csv.backup.%d" % copy_num)
    break

with open("tag_rules.csv") as rules_file:
    for line in rules_file:
        if line.startswith("Package Name,Library Name,Type,Official Website"):
            continue
        if len(line.split(',')) != 4:
            logging.error("Num of Commas Wrong!\n%s" % line)
            break
        rules.append(line)

rules.sort()
with open("tag_rules.csv", "w") as rules_file:
    rules_file.write("Package Name,Library Name,Type,Official Website\n")
    for line in rules:
        rules_file.write(line)
