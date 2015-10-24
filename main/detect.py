# -*- coding:utf-8 -*-
# Created at 2015/7/20
# Recently Modified at 2015/10/17
# Current Version 1.2.0

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
import zipfile
from time_recorder import TimeRecord

"""
RM_STATUS : {
    0 Remove Nothing
    1 Remove all
    2 Remove Lib Code
}
"""
RM_STATUS = 0
DEBUG_ON = False
DEBUG_PATH = False


class Detector:
    """
     Detector
    """
    library_type = {
        "da": "Development Aid",
        "sn": "Social Network",
        "ad": "Advertisement",
        "am": "App Market",
        "ma": "Mobile Analytics",
        "pa": "Payment",
        "ui": "UI Component",
        "ge": "Game Engine",
        "ut": "Utility",
        "mp": "Map"
    }

    def __init__(self):
        # Init Two Time Recorder.
        self.time_decode = TimeRecord('Target App Decoding')
        self.time_load = TimeRecord('Lib Data Loading')
        self.time_extract = TimeRecord('Feature Extracting')
        self.time_compare = TimeRecord('Library Searching')

        # For decoding bug.
        reload(sys)
        sys.setdefaultencoding("utf-8")

        # Init API dict and data.
        self.api_dict = {}
        self.packages_feature = []
        self.libs_feature = []
        self.project_path = os.path.dirname(sys.argv[0])

        self.load_data()


    @staticmethod
    def rm_lib_files(lib_list):
        for lib_dir_name in lib_list:
            cmd = 'rm -rf %s' % lib_dir_name
            subprocess.call(cmd, shell=True)

    @staticmethod
    def zip_apk(source, target):
        if not os.path.exists(os.path.dirname(target)):
            os.mkdir(os.path.dirname(target))
        file_list = []
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for name in files:
                    file_list.append(os.path.join(root, name))
        else:
            # print '%s is not a directory.' % source
            file_list.append(source)
        zf = zipfile.ZipFile(target, 'w', zipfile.zlib.DEFLATED)
        for tar in file_list:
            arcname = tar[len(source):]
            zf.write(tar, arcname)
        zf.close()

    def get_number(self, string):
        """
        Get API ID From API Dictionary.
        获得API的编号
        :param string: API Name+
        :return: API ID
        """
        if string not in self.api_dict:
            return -1
        return str(self.api_dict[string]['v'])

    def get_permission(self, string):
        """
        Get Permission From API Dictionary.
        获得API的权限
        :param string: API Name
        :return: Permission List
        """
        if string not in self.api_dict:
            return -1
        return self.api_dict[string]['p']

    def all_over(self, apk_path, path):
        """
        Recursive body of package for getting the features
        :param apk_path: APK Path
        :param path: Packages Path
        :return: API Dict of this package, Directory Number in this Package, File Number, Total API Call.
        """
        if DEBUG_PATH:
            print ('PATH : ' + path)
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
                if DEBUG_PATH:
                    print ('Path and Current Work Directory.')
                    print thing
                    print os.getcwd()
                os.chdir(thing + '/')
                # Merge Dictionary
                # 合并字典
                child = self.all_over(apk_path, path + thing + '/')
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
                os.chdir('..')
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
                            call_num = self.get_number(system_call)
                            permissions = self.get_permission(system_call)
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
        if DEBUG_PATH:
            print ('APK_PATH' + apk_path)
        bh = 0
        for a in this_dict:
            bh = (bh + int(a) * this_dict[a]) % 999983          # 99983 is A Big Prime
        self.packages_feature.append((bh, len(this_dict), this_call_num, path, this_permission))
        return this_dict, this_dir_num, this_file_num, this_call_num, this_permission


    def get_smali(self, path):
        """
        Convert APK into Smali file.
        :param path:
        :return: decoded files' path
        """
        self.time_decode.start()
        cmd = self.project_path + "/" + "../tool/apktool decode %s -o " % path + self.project_path + "/" + \
            "../decoded/%s" % os.path.basename(path)
        subprocess.call(cmd, shell=True)
        self.time_decode.end()
        return self.project_path + '/../decoded/%s' % os.path.basename(path)

    def load_data(self):
        # - Loading Data

        self.time_load.start()
        dep_address = self.project_path + "/" + "../data/tgst5.dat"
        dict_address = self.project_path + "/" + "../permission/tagged_dict.txt"
        dep_file = open(dep_address, 'r')
        dict_file = open(dict_address, 'r')

        # -- Loading API Dict
        for line in dict_file:
            # print line
            u = json.loads(line)
            if 'p' in u:
                self.api_dict[u['k']] = {'v': u['v'], 'p': u['p']}
            else:
                self.api_dict[u['k']] = {'v': u['v'], 'p': []}

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
                components = u['lib'].split(';')
                assert len(components) == 3
                lib_type = components[0]
                if lib_type in self.library_type:
                    lib_type = self.library_type[lib_type]
                eng_lib = components[1]        # English Library
                ch_des = components[2]         # Web Link
                self.libs_feature.append(
                    (u['bh'], u['btn'], u['btc'], u['sp'], eng_lib, u['pn'], u['dn'], ch_des, lib_type)
                )
            else:
                self.libs_feature.append((u['bh'],  u['btn'], u['btc'], u['sp'], u['lib'], "", u['dn'], "", ""))

        self.time_load.end()

    def get_hash(self, apk_path):
        """
        Convert APK into Smali file.
        :param path:
        :return: The path of apk with libs removed.
        """

        self.time_extract.start()

        # - All Over
        # print apk_path+'/smali'
        if os.path.exists(apk_path+'/smali'):
            os.chdir(apk_path+'/smali')
            self.all_over(apk_path, '')
            # os.chdir(apk_path)

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

        number_of_tagged_libs = len(self.libs_feature)
        self.time_extract.end()
        self.time_compare.start()

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
            if compare_d(package, self.libs_feature[mid]) == 0:
                if self.libs_feature[mid][4] != "" and self.libs_feature[mid][4] != "Nope":
                    cur_app_libs.append({
                        "bh": self.libs_feature[mid][0],
                        "btn": self.libs_feature[mid][1],
                        "btc": self.libs_feature[mid][2],
                        "sp": self.libs_feature[mid][3],
                        "lib": self.libs_feature[mid][4],
                        "pn": self.libs_feature[mid][5],
                        "dn": self.libs_feature[mid][6],
                        "ch": self.libs_feature[mid][7],         # Web Link
                        "tp": self.libs_feature[mid][8],
                        "csp": package[3],                  # Current S_path
                    })
                elif self.libs_feature[mid][4] == "":
                    cur_app_routes[self.libs_feature[mid][3]] = {
                        "pn": self.libs_feature[mid][3],
                        "cpn": package[3],
                        "p": package[4],
                        "dn": self.libs_feature[mid][6]
                    }
            elif compare_d(package, self.libs_feature[mid]) < 0:
                return find_feature(package, mid + 1, end)
            else:
                return find_feature(package, start, mid)

        if DEBUG_ON:
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

        for pack in self.packages_feature:
            if DEBUG_PATH:
                print ('PACK' + str(pack))
            find_features(pack)
        if DEBUG_ON:
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
                # 找到同样package name的小包中，重复次数最多的，作为总的重复次数
                # 本来想找到大包的重复次数作为重复次数，但是大包的重复次数甚至很容易直接是0
                # 并不适合。
                if final_libs_dict[i['pn']]['dn'] < i['dn']:
                    final_libs_dict[i['pn']]['dn'] = i['dn']
            pn_number = len(i['pn'].split('/'))
            cpn = '/'.join(i['csp'].split('/')[0:pn_number])
            if cpn[-1:] != '/':
                cpn += '/'
            i['cpn'] = cpn
            i['p'] = path_and_permission[cpn]
            final_libs_dict[i['pn']] = i
            #print str(i) + ','
        final_libs_list = []
        for i in final_libs_dict:
            final_libs_dict[i]['pn'] += '/'
            final_libs_list.append(final_libs_dict[i])
        # print json.dumps(final_libs_list)
        final_routes_list = []
        for i in cur_app_routes:
            cur_app_routes[i]['pn'] += '/'
            final_libs_list.append(cur_app_routes[i])
        sorted_libs = sorted(final_libs_list, key=lambda lib: lib['dn'], reverse=True)
        print json.dumps(sorted_libs)
        print "--Splitter--"
        print "--Splitter--"
        self.time_compare.end()

        # To String
        # print "--Time-Consuming--"
        self.time_decode.tostring()
        self.time_load.tostring()
        self.time_extract.tostring()
        self.time_compare.tostring()

        # Remove Lib Files.
        lib_dir_list = []
        for i in final_libs_dict:
            if 'cpn' in final_libs_dict[i]:
                lib_dir_list.append(apk_path + '/smali/' + final_libs_dict[i]['cpn'])
        if RM_STATUS > 0:
            self.rm_lib_files(lib_dir_list)

        zip_file_name = self.project_path + '/../clean_app/' + os.path.basename(apk_path)[:-3] + 'zip'
        smali_path = apk_path + '/smali'
        self.zip_apk(smali_path, zip_file_name)

        if RM_STATUS == 1:
            cmd = 'rm -rf %s' % apk_path
            subprocess.call(cmd, shell=True)
        elif RM_STATUS == 2:
            zip_file_name = self.project_path + '/../clean_app/' + os.path.basename(apk_path)[:-3] + 'zip'
            smali_path = apk_path + '/smali'
            self.zip_apk(smali_path, zip_file_name)
            return zip_file_name
        return "No Zip File Here."
