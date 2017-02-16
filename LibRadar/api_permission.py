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

# API Permission

# Get permission from PScout

# Input LibRadar/Data/RawData/mapping_x.x.x.csv
# Input invokeFormat.txt

# Output api_permission.csv

import glob

def generate_permission():
    # invokes
    invokes = dict()
    with open("Data/IntermediateData/invokeFormat.txt") as invoke_format:
        for line in invoke_format:
            invokes[line.strip()] = set()
    # Now we got 4.1.1 4.2.2 4.4.4 5.0.2 5.1.1 as sample
    pscout_files = glob.glob("Data/RawData/mapping_*.csv")
    for pscout_file in pscout_files:
        with open(pscout_file, 'r') as pscout:
            for line in pscout:
                line_split = line.split(',')
                caller_class = line_split[0]
                caller_method = line_split[1]
                caller_method_desc = line_split[2]
                permission = line_split[3]
                version = line_split[4]
                if caller_class == "CallerClass":
                    continue
                if permission == "Unknown" or permission == "Parent":
                    continue
                invoke = "L" + caller_class + ";->" + caller_method
                if invoke in invokes:
                    invokes[invoke].add(permission)
                else:
                    invokes[invoke] = set()
                    invokes[invoke].add(permission)
    invoke_list = list()
    for invoke in invokes:
        invoke_list.append([invoke, list(invokes[invoke])])
    invoke_list.sort()
    with open("Data/IntermediateData/api.csv", "w") as api_file:
        for invoke in invoke_list:
            api_file.write(invoke[0] + ",")
            for permi in invoke[1]:
                api_file.write(permi)
                api_file.write(":")
            api_file.write("\n")



if __name__ == '__main__':
    generate_permission()