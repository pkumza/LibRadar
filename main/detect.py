# -*- coding:utf-8 -*-
# Created at 2015/7/20
# Recently Modified at 2015/09/02
# Current Version 1.1.0

__author__ = 'Zachary Marv - 马子昂'

"""
    LibRadar is a tool for detecting third-party libraries in Android apps accurately and instantly.
"""

import os
import json
import glob
import re
import subprocess
import sys
import time

DEBUG_ON = False


class TimeRecord:
    """
    @ class TimeRecord
    Made for Time Recording.
    用来计时。
    """
    def __init__(self, task_tag=""):
        self.init_time = time.time()
        self.if_start = False
        self.start_time = 0
        self.tag = task_tag

    def start(self):
        self.start_time = time.time()
        self.if_start = True

    def end(self):
        end_time = time.time()
        if self.if_start:
            task_interval = end_time - self.start_time
            s = task_interval
            if s <= 1:
                se = 'second'
            else:
                se = 'seconds'
            self.to_string = self.tag + '\tConsumed ' + str(s)[:7]+' '+se+'.'
        self.if_start = False

    def tostring(self):
        print self.to_string

# Init Two Time Recorder.
time_decode     = TimeRecord('Target App Decoding')
time_load       = TimeRecord('Lib Data Loading')
time_extract    = TimeRecord('Feature Extracting')
time_compare    = TimeRecord('Library Searching')


# For decoding Bug.
reload(sys)
sys.setdefaultencoding("utf-8")


api_dict = {}
packages_feature = []
libs_feature = []
project_path = os.path.dirname(sys.argv[0])


def get_smali(path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    time_decode.start()
    cmd = project_path + "/" + "../tool/apktool decode %s -o " % path + project_path + "/" + "../decoded/%s" % os.path.basename(path)
    subprocess.call(cmd, shell=True)
    time_decode.end()
    return project_path + '/../decoded/%s' % os.path.basename(path)


def get_hash(apk_path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    # - Loading Data

    time_load.start()
    dep_address = project_path + "/" + "../data/tgst5.dat"
    dict_address = project_path + "/" + "../permission/tagged_dict.txt"
    dep_file = open(dep_address, 'r')
    dict_file = open(dict_address, 'r')

    # -- Loading API Dict
    for line in dict_file:
        # print line
        u = json.loads(line)
        if 'p' in u:
            api_dict[u['k']] = {'v': u['v'], 'p': u['p']}
        else:
            api_dict[u['k']] = {'v': u['v'], 'p': []}

    # -- Loading Hashed Libs

    for line in dep_file:
        # print line
        u = json.loads(line)
        """
        {"dn": 311,                         Repetitions
         "lib": "pollfish",                 Library
          "sp": "com/pollfish/f/a",         Simplified Path
           "bh": 32370,                     B_Hash
            "btc": 40,                      B_Total_Call
             "btn": 12,                     B_Total_Number
              "pn": "com/pollfish"}         Package Name
        """
        if "pn" in u:
            if ';' in u['lib']:
                english_lib = u['lib'].split(';')[0]
                ch_des = u['lib'].split(';')[1]         # Chinese Description
                libs_feature.append((u['bh'],  u['btn'], u['btc'], u['sp'], english_lib, u['pn'], u['dn'], ch_des))
            else:
                libs_feature.append((u['bh'],  u['btn'], u['btc'], u['sp'], u['lib'], u['pn'], u['dn'], ""))
        else:
            libs_feature.append((u['bh'],  u['btn'], u['btc'], u['sp'], u['lib'], "", u['dn'], ""))

    time_load.end()
    time_extract.start()

    # - All Over
    # print apk_path+'/smali'
    if os.path.exists(apk_path+'/smali'):
        os.chdir(apk_path+'/smali')
        all_over(apk_path, apk_path+'/smali')
        os.chdir(apk_path)

    # Print Res
    # print packages_feature
    '''
    if DEBUG:
        for p in packages_feature:
            print p
    '''
    cur_app_libs = []
    cur_app_routes = {}
    path_and_permission = {}

    number_of_tagged_libs = len(libs_feature)
    time_extract.end()
    time_compare.start()

    def compare_d(a, b):
        if a[1] < b[1]:
            return -1
        elif a[1] > b[1]:
            return 1
        else:
            if a[2] < b[2]:
                return -2
            elif a[2] > b[2]:
                return 2
            else:
                if a[0] < b[0]:
                    return -3
                elif a[0] > b[0]:
                    return 3
                else:
                    return 0

    def find_feature(package, start, end):
        if start >= end:
            return None
        mid = (start + end) / 2
        """
            packages_feature.append((bh, len(this_dict), this_call_num, '/'.join(parts), this_permission))
        """
        if compare_d(package, libs_feature[mid]) == 0:
            if libs_feature[mid][4] != "" and libs_feature[mid][4] != "Nope":
                cur_app_libs.append({
                    "bh": libs_feature[mid][0],
                    "btn": libs_feature[mid][1],
                    "btc": libs_feature[mid][2],
                    "sp": libs_feature[mid][3],
                    "lib": libs_feature[mid][4],
                    "pn": libs_feature[mid][5],
                    "dn": libs_feature[mid][6],
                    "ch": libs_feature[mid][7],         # Chinese Description
                    "csp": package[3],                  # Current S_path
                })
            elif libs_feature[mid][4] == "":
                cur_app_routes[libs_feature[mid][3]] = {
                    "sp": libs_feature[mid][3],
                    "csp": package[3],
                    "cp": package[4],
                    "dn": libs_feature[mid][6]
                }
        elif compare_d(package, libs_feature[mid]) < 0:
            return find_feature(package, mid + 1, end)
        else:
            return find_feature(package, start, mid)

    print "--Packages--"

    def find_features(package):
        if package[3] != "":
            if len(package[4]) == 0:
                if DEBUG_ON:
                    print package[3]
                path_and_permission[package[3]] = []
            else:
                if DEBUG_ON:
                    print package[3]+' -- Permission: '+str(package[4])
                path_and_permission[package[3]] = package[4]
        find_feature(package, 0, number_of_tagged_libs)

    for pack in packages_feature:
        find_features(pack)
    print "PATH and Permission:"
    for k in path_and_permission:
        print k + str(path_and_permission[k])
    print "--Splitter--"
    final_libs_dict = {}
    for i in cur_app_libs:
        # 先找PN
        # 然后切分sp。找到对应的path
        # 然后把对应的Permission找出来加进来
        if i['pn'] in final_libs_dict:
            continue
        pn_number = len(i['pn'].split('/'))
        cpn = '/'.join(i['csp'].split('/')[0:pn_number])
        i['cpn'] = cpn
        i['p'] = path_and_permission[cpn]
        final_libs_dict[i['pn']] = i
        #print str(i) + ','
    final_libs_list = []
    for i in final_libs_dict:
        final_libs_list.append(final_libs_dict[i])
    print json.dumps(final_libs_list)
    print "--Splitter--"
    final_routes_list = []
    for i in cur_app_routes:
        final_routes_list.append(cur_app_routes[i])
    print json.dumps(final_routes_list)
    print "--Splitter--"
    time_compare.end()

    # To String
    print "--Time-Consuming--"
    time_decode.tostring()
    time_load.tostring()
    time_extract.tostring()
    time_compare.tostring()
    cmd = 'rm -rf %s' % apk_path
    subprocess.call(cmd, shell=True)
    return "Get Function Ends."


def get_number(string):
    """
    Get API ID From API Dictionary.
    获得API的编号
    :param string: API Name
    :return: API ID
    """
    if string not in api_dict:
        return -1
    return str(api_dict[string]['v'])


def get_permission(string):
    """
    Get Permission From API Dictionary.
    获得API的权限
    :param string: API Name
    :return: Permission List
    """
    if string not in api_dict:
        return -1
    return api_dict[string]['p']


def all_over(apk_path, path):
    """
    Recursive body of package for getting the features
    :param apk_path: APK Path
    :param path: Packages Path
    :return: API Dict of this package, Directory Number in this Package, File Number, Total API Call.
    """

    find_file = re.compile(r'.smali$')
    p = re.compile(r'Landroid/.*?;?\-?>*?\(|Ljava/.*?;?\-?>*?\(|Ljavax/.*?;?\-?>*?\(|Lunit/runner/.*?;?\-?>*?\('
                   r'|Lunit/framework/.*?;?\-?>*?\('
                   r'|Lorg/apache/commons/logging/.*?;?\-?>*?\(|Lorg/apache/http/.*?;?\-?>*?\(|Lorg/json/.*?;'
                   r'?\-?>*?\(|Lorg/w3c/.*?;?\-?>*?\(|Lorg/xml/.*?;?\-?>*?\(|Lorg/xmlpull/.*?;?\-?>*?\(|'
                   r'Lcom/android/internal/util.*?;?\-?>*?\(')
    all_thing = glob.glob('*')
    this_permission = []
    this_call_num = 0
    this_dir_num = 0
    this_file_num = 0
    direct_dir_num = 0
    direct_file_num = 0
    this_dict = {}
    for thing in all_thing:
        # If the thing is a directory.
        if os.path.isdir(thing):
            os.chdir(path+'/'+thing)
            # Merge Dictionary
            # 合并字典
            child = all_over(apk_path, path+'/'+thing)
            if child is not None:
                this_dict.update(child[0])
                this_dir_num += child[1] + 1
                direct_dir_num += 1
                this_file_num += child[2]
                this_call_num += child[3]
                if child[4] != []:
                    for per in child[4]:
                        if per not in this_permission:
                            this_permission.append(per)
            os.chdir(path)
        # If the 'thing' is a file
        # 如果 thing 是一个文件
        else:
            try:
                # Is this file a smali file?
                # 如果这个文件是一个SMALI文件
                if not find_file.search(thing):
                    continue
                f = open(thing, 'r')
                for u in f:
                    # For every line in this file.
                    # 搜索每一行。
                    match = p.findall(u)
                    for system_call in match:
                        if '"' in system_call:
                            continue
                        this_call_num += 1
                        call_num = get_number(system_call)
                        permissions = get_permission(system_call)
                        if permissions == -1:
                            continue
                        # print permissions
                        if len(permissions) != 0:
                            for per in permissions:
                                if per not in this_permission:
                                    this_permission.append(per)
                        
                        if call_num == -1:
                            continue
                        if call_num in this_dict:
                            this_dict[call_num] += 1
                        else:
                            this_dict[call_num] = 1
                f.close()
                this_file_num += 1
                direct_file_num += 1
            except Exception as ex:
                if DEBUG_ON:
                    print('Can not Open ' + thing + ' Wrong with:' + str(ex))
    # If there is no API call in this package, just ignore it.
    if len(this_dict) == 0:
        return
    parts = path[len(apk_path)+7:].split("/")
    bh = 0
    for a in this_dict:
        bh = (bh + int(a) * this_dict[a]) % 999983          # 99983 is A Big Prime
    packages_feature.append((bh, len(this_dict), this_call_num, '/'.join(parts), this_permission))
    return this_dict, this_dir_num, this_file_num, this_call_num, this_permission


def main_func(path):
    """
    Detect 3rd-party libraries in app.
    The detection result is printed.
    :param path: The path of target app.
    :return: None.
    """
    print "--Decoding--"
    decoded_path = get_smali(path)
    get_hash(decoded_path)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "No Apk File Name.\nTry to detect 'Yo.apk' for test."
        main_func("~/Downloads/org.itishka.pointim_23.apk")
    else:
        print os.path.basename(sys.argv[1])
        main_func(sys.argv[1])
