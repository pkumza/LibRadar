# -*- coding: utf-8 -*-
"""
    API_Dict.py

    This is the first step for data collection.

    Firstly, get android.jar in Android SDK folder.
    Rename them and place them into Data/RawData folder.
    Glob module will automatically detect them and decompile them.
    Finally, we could extract all the APIs.

    Warning: Working Directory should be LibRadar other than LibRadar/LibRadarData

    Warning: Working Directory should be LibRadar other than LibRadar/LibRadarData

"""

import os
import commands
import redis
import glob
from settings import *

"""
    Information about Database.
    Redis is used here and the default setting points to localhost:6379
    If your Redis IP and Port is different, you can change the value here.
    In my redis.conf, I set 32 for the maximum number of databases.
    What's the databases for?

        0 : Android.jar Classes
        1 : Android.jar APIs
"""


class Singleton(object):
    """
        Implementation for Singleton
    """
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls)
        return cls._inst


class ApiDictionaryGenerator(Singleton):
    """
        A class used for collecting API data
    """

    def __init__(self):
        """
            __init__
            Create connection to redis database.
            open a file for api output.
        """
        self.jar_list = []
        self.redis_class_name = redis.StrictRedis(host=db_host, port=db_port, db=db_class_name_id)
        log_w("Clean all the keys in class database")
        self.redis_class_name.flushdb()
        self.redis_android_api = redis.StrictRedis(host=db_host, port=db_port, db=db_android_api_id)
        log_w("Clean all the keys in API database")
        self.redis_android_api.flushdb()
        self.api_set = set()
        self.txt_output_api = open("./Data/IntermediateData/api.txt", 'w')

    def __del__(self):
        """
            __del__
            StrictRedis doesn't implement close or quit methods.
            We don't need to close redis connection here.
        """
        self.txt_output_api.close()

    @staticmethod
    def if_jad_exists():
        """
            Test if jad command exists.
            Run `jad` command as a test. If the status is 32512, it means that system cannot
                find the `jad` command. If the response is 256, `jad` can be run but `jad`
                cannot runs stably without arguments. If the status is neither 32512 nor 256,
                I don't know what happened.
        """
        # run `jad` command as a test here to exam if jad is installed.
        status, out = commands.getstatusoutput('jad')
        if status == 32512:
            log_e("Jad is not runnable. please put `tool/jad` into your $PATH environment.")
            raise AssertionError
        if status == 256:
            pass
        else:
            log_w("Maybe there is something wrong with jad status.")

    """
        Take jar file into account. It is ok to have only one version of android.jar
        android.jar could be found in $YOUR_ANDROID_SDK_ROOT/platforms/android-$VERSION

        For Example:
            /Library/Android_SDK/platforms/android-11/android.jar

        Use add_jar to add a file.
        Use add_jar several times or add_jars to add a list of files.
    """
    def add_jar(self, jar_file):
        self.jar_list.append(jar_file)

    def add_jars(self, jar_files):
        self.jar_list.extend(jar_files)

    """
        Use jad to decompile jar file into android.jar.dir

        Step:
            1 - Unzip .jar file
            2 - use jad to decompile .class file into .java file.
    """
    def decompile_jar(self):
        self.if_jad_exists()
        for jar in self.jar_list:
            log_i("Decompiling %s" % jar)
            cmd = "./tool/jar_decompiler.sh " + jar
            os.popen(cmd)

    """
        Walk through the directories to find all the class names and methods (SDK API).


    """
    def walk_dir(self):
        for jar in self.jar_list:
            dir_to_be_walked = jar + ".dir"
            log_i("Walk %s" % dir_to_be_walked)
            for dirName, subdirList, fileList in os.walk(dir_to_be_walked):
                for filename in fileList:
                    if len(filename) > 4 and filename[-5:] == ".java":
                        full_path_name = '/'.join(dirName.split('/')[4:]) + '/' + filename
                        class_name = full_path_name[:-5].replace('/', '.')
                        '''
                            Contents in inner class file like 'R$style.java' are already included in
                                the parent class file. So we need to ignore the java file with symbol
                                '$' in it.
                        '''
                        if '$' in full_path_name:
                            continue
                        self.read_java(full_path_name, class_name, jar, self.api_set)
                        self.redis_class_name.incr(class_name)
            # clean the directory
            if clean_workspace:
                log_i("Cleaning the directory which is already walked.")
                os.system('rm -rf %s' % dir_to_be_walked)
        log_i("API Count is %d" % len(self.api_set))
        log_i("Write the APIs into txt file as a backup.")
        for api in self.api_set:
            self.txt_output_api.write(api + '\n')

    def read_java(self, full_path_name, class_name, jar, api_set):
        """
            Read APIs from java file.
        """
        open_java_file = open(jar + '.dir/' + full_path_name, 'r')
        brackets_count = 0
        current_inner_class = ""
        for line in open_java_file:
            # if the line is a comment.
            if len(line.strip()) > 2 and line.strip()[:2] == "//":
                continue
            if '{' in line:
                brackets_count += 1
            if '}' in line:
                brackets_count -= 1
            # outer class
            if 'public' in line and 'class' in line and brackets_count == 0:
                continue
            # inner class
            if 'public' in line and 'class' in line and brackets_count == 1:
                current_inner_class = line.split('class')[1].strip()
                continue
            # method (API)
            if 'public' in line and '(' in line and ')' in line:
                left_part = line.split('(')[0]
                method_name = left_part.split(' ')[-1]
                return_type = left_part.split(' ')[-2]
                '''
                    if the value is public, that means the function is a constructive method.
                    I use '#' here to tag that the method does not have a return type.

                    If the value is not '#', the value is put into database 0 for a count.
                '''
                if return_type == 'public':
                    return_type = '#'
                else:
                    self.redis_class_name.incr(return_type)
                right_part = line.split('(')[1]
                # parameters of the method
                paras = []
                paras_number = len(right_part.split(' '))
                for i in range(paras_number):
                    if i % 2 == 0:
                        para_type = right_part.split(' ')[i]
                        self.redis_class_name.incr(para_type)
                        paras.append(para_type)
                # reconstruct the method
                full_class_name = class_name
                if brackets_count == 2:
                    full_class_name += '$'
                    full_class_name += current_inner_class
                parameters_string = ""
                for i in range(paras_number / 2):
                    if i != 0:
                        parameters_string += ','
                    parameters_string += paras[i]
                method_declare = "%s %s;->%s(%s)" % (return_type, full_class_name, method_name, parameters_string)
                api_set.add(method_declare)
                self.redis_android_api.incr(method_declare)

        open_java_file.close()


class ApiDictionaryGeneratorWrapper:
    """
        ADG Wrapper
        If you are not interested in the details, just use this class.
        Input a list of file names which you have already placed into Data/RawData folder.
        There're no more thing you need to do here.
        information about classes and APIs are automatically stalled into txt file and database.
    """
    def __init__(self, jar_list):
        # create an instance.
        log_i("Creating an instance of ApiDictionaryGenerator")
        adg = ApiDictionaryGenerator()
        # add the jar into list.
        log_i("Adding jar path into jar list")
        adg.add_jars(jar_list)
        # decompiling the jar file. decompiling is only needed once.
        log_i("Decompiling jar")
        adg.decompile_jar()
        # walk through the directory to find APIs.clean
        adg.walk_dir()


if __name__ == "__main__":
    """
        In my test case, I use android.jar of version21 and android.jar of version24 here.

        How to use this line of code?
            1. firstly, change android.jar's name and put them into ./Data/RawData
            2. write the names here as a list
            3. run this python file.
        What happened when this file is running?
            1. files are extracted into ./Data/RawData/$directory_name$.dir
            2. the program will automatically read the class file with jad and convert them into java
            3. this script read the java files and search for the classes and APIs
            4. classes and native types are stalled into database 0 in redis
            5. APIs are written into api.txt
            6. APIs are also placed into database 1 in redis

        PS:
            There are commonly 30 thousands of APIs in one version of android.jar
    """
    jar_file_list = glob.glob("./Data/RawData/*.jar")
    api_dict_generator_wrapper = ApiDictionaryGeneratorWrapper(jar_file_list)
