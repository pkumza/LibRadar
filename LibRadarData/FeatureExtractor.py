# -*- coding: utf-8 -*-
"""
    Feature Extractor

    This script is used to extract features from smali files.
"""

import redis
from LRD_Settings import *
import hashlib
import threading
import os


class FeatureExtractor(threading.Thread):
    """
    Feature Extractor

    """
    def __init__(self, thread_id, smali_dir_path):
        """
            Init the Feature Extractor with ID and smali folder's path.
        :type thread_id: basestring
        :type smali_dir_path: basestring
        """
        self.thread_id = thread_id
        self.smali_dir_path = smali_dir_path
        threading.Thread.__init__(self, name=thread_id)
        self.db_invoke = redis.StrictRedis(host=db_host, port=db_port, db=db_api_invoke)
        self.db_feature_count = redis.StrictRedis(host=db_host, port=db_port, db=db_feature_count)
        self.db_feature_weight = redis.StrictRedis(host=db_host, port=db_port, db=db_feature_weight)

    def flush_feature_db(self):
        """
            Delete feature databases.
            Warning! Just for Test!!!
        :return: None
        """
        log_w("Delete database feature count!  [DB3]")
        self.db_feature_count.flushdb()
        log_w("Delete database feature weight! [DB4]")
        self.db_feature_weight.flushdb()

    def smali_extractor(self, smali_file_name):
        """
        This function is used to extract API information from a smali file.
        :param smali_file_name:
        :return: (a list of APIs that this file used, how many APIs here)
        """
        smali_file = open(smali_file_name, 'r')
        api_list = list()
        md5 = hashlib.md5()
        for line in smali_file:
            if line[:11] == "    invoke-":
                # left point of the API section.
                # the API string starts with },
                #
                # For Example:
                # invoke-static {v0, p0}, Ljava/lang/Enum;->valueOf(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;
                #
                # this string starts with invoke
                # for the arguments v0 and p0, there's always '}, ' after them.
                # As it is a function, a bracket is needed after the API name.
                # We could use the two clue to catch the potential API
                left_point = line.find('}, ') + 3
                # right point of the API section.
                right_point = line.find('(')
                # if the code cannot find '}, ' or '(' here, the return value will be -1.
                # That's definitely not an API here. So, just continue.
                if left_point < 0 or right_point < 0:
                    continue
                # cut this line to extract the potential API
                potential = line[left_point:right_point]
                # find the potential API in database to exam whether it is an API.
                version_count = self.db_invoke.get(potential)
                if version_count is not None:
                    api_list.append(potential)
        # it must be sorted to ensure that the result is not associated with the order.
        for api in sorted(api_list):
            md5.update(api)
        # return a tuple: (Hash, Weight)
        return md5.hexdigest(), len(api_list)

    @staticmethod
    def _check_directory_name(directory_name):
        """
            Check if there's something wrong with directory setting.
        """
        if not isinstance(directory_name, basestring):
            log_e("Directory name is not a string.")
            raise AssertionError
        if len(directory_name) < 7:
            log_e("Directory name is too short.")
            raise AssertionError
        if directory_name[-6:] != "/smali":
            if directory_name[-1] == '/':
                log_e("There should be no '/' in the end of directory name.")
                raise AssertionError
            else:
                log_e("The Directory name should ends with smali. You should adjoin decoded path with '/smali'.")

    def dir_extractor(self, directory_name):
        """
            Extract all the features from an APK.
            the directory name is the smali folder of a decompiled APK.
        :param directory_name:
        :return:
        """
        self._check_directory_name(directory_name)
        # hash_storage is used to store all the hash value of packages in this APK file temporarily.
        #   Key: Dir_Path
        #   Value: MD5-128bit Hex Format
        hash_storage = dict()
        for dir_path, sub_dirs, file_list in os.walk(directory_name, topdown=False):
            hash_list = list()
            api_count = 0
            for smali_file in file_list:
                smali_hash, smali_api_count = self.smali_extractor(dir_path + '/' + smali_file)
                api_count += smali_api_count
                hash_list.append(smali_hash)
                smali_weight_in_db = self.db_feature_weight.get(smali_hash)
                if smali_weight_in_db is None:
                    if smali_api_count > 0:
                        self.db_feature_weight.set(smali_hash, smali_api_count)
                elif smali_weight_in_db != str(smali_api_count):
                    # Strong checking mode for examining MD5-128bit is really powerful for this work.
                    # It can be closed after this examination to save calculation resource.
                    log_d("SmaliPath: %s" % dir_path + '/' + smali_file)
                    log_d("SmaliHash: %s" % smali_hash)
                    log_d("Weight   : %s" % smali_weight_in_db)
                    log_d("Count    : %d" % smali_api_count)
                    log_e("Something wrong with the code or MD5-128bit is not enough. [Smali Level]")
                else:
                    pass
                if smali_api_count > 0:
                    self.db_feature_count.incr(smali_hash)
            for sub_dir in sub_dirs:
                sub_dir_full_path = dir_path + '/' + sub_dir
                if sub_dir_full_path not in hash_storage:
                    log_e("sub-directory %s should exists in hash_list." % sub_dir_full_path)
                    raise AssertionError
                hash_list.append(hash_storage[sub_dir_full_path])
            md5 = hashlib.md5()
            for hash_value in sorted(hash_list):
                md5.update(hash_value)
            dir_hash = md5.hexdigest()
            hash_storage[dir_path] = dir_hash
            weight_in_db = self.db_feature_weight.get(dir_hash)
            if weight_in_db is None:
                # If It's the first time we met this hash.
                if api_count > 0:
                    self.db_feature_weight.set(dir_hash, api_count)
            elif weight_in_db != str(api_count):
                # Strong checking mode for examining MD5-128bit is really powerful for this work.
                # It can be closed after this examination to save calculation resource.
                log_d("DirPath: %s" % dir_path)
                log_d("DirHash: %s" % dir_hash)
                log_d("Weight : %s" % weight_in_db)
                log_d("Count  : %d" % api_count)
                log_e("Something wrong with the code or MD5-128bit is not enough. [Package Level]")
                raise AssertionError
            else:
                # Everything is OK.
                pass
            # Feature Count++
            if api_count > 0:
                self.db_feature_count.incr(dir_hash)
        return hash_storage

    def run(self):
        log_i("Feature Extractor %s is extracting %s" % (self.thread_id, self.smali_dir_path))
        hash_storage = self.dir_extractor(self.smali_dir_path)
        for key, vl in hash_storage.items():
            log_v("%s - %s" % (vl, key))
        log_i("Feature Extractor %s has extracted %s" % (self.thread_id, self.smali_dir_path))


if __name__ == "__main__":
    """
        Usage Sample
    """
    fe = FeatureExtractor("001", "./Data/RawData/com.FunLiveWallpaper/smali")
    fe.flush_feature_db()
    fe.start()
    fe.join()
    log_i("All Threads Finished")
