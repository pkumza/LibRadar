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

#   API_Dict.py
#
#   WARNING!!! Could be run under Mac OS only.
#
#   You don't need to run this again!!! Just use Data/IntermediateData/invokeFormat.txt
#
#   This is the first step for data collection. However, jad is out of data and it could only been easily used on Mac.
#   What's more, running this script need to download all the versions of Android SDK.
#   So, if you do not want to learn about the principle, just ignore this script.
#
#   Firstly, get android.jar in Android SDK folder.
#   Rename them and place them into Data/RawData folder.
#   Glob module will automatically detect them and decompile them.
#   In this case, we could extract all the APIs.
#   Finally, some non-sense API should be removed.
#
#   Non-sense API:
#       As an example, a package named Lcom/degoo/android/fbmassage is not a library, which belongs to an app named
#       "Princess Full Body Massage APK". This package contains no API other than 15 "Ljava/lang/Object;-><init>()"
#       It is very likely that another packages share the same feature.
#
#       In my database of 4600 apps, There're already 140 packages shares the same feature. That's definitely wrong!
#       (MD5: 5019771e5f8ce4bc333b504a3a6bc4a6)
#
#   Implementation:
#       ApiDictionaryGenerator.ignore_list
#
#   Warning: Working Directory should be LibRadar other than LibRadar/LibRadar

#   Take API Level 16,18,19,21,22,23,24,25 in account, We could found 34299 APIs without overloading
#   Ignore 1761 APIs
#   2016/12/30

#   Take API Level 7,8,9,...,25 in account, we could found 34683 APIs without overloading.
#   (From Android 2.1 to newest Android 7.1.1)
#   Ignore 1775 APIs
#   2017/01/10

import os.path
import commands
# ## import redis
import glob
from _settings import *

"""
    Information about Database.
    Redis is used here and the default setting points to localhost:6379
    If your Redis IP and Port is different, you can change the value here.
    In my redis.conf, I set 32 for the maximum number of databases.
    What's the databases for?

        0 : Android.jar Classes
        1 : Android.jar APIs with return_type and arguments
        2 : Android.jar APIs with only full class name and method name
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
        # ## self.redis_class_name = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_CLASS_NAME)
        # ## logger.warning("Clean all the keys in databases")
        # ## self.redis_class_name.flushdb()
        # ## self.redis_android_api = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_ANDROID_API)
        # ## self.redis_android_api.flushdb()
        # ## self.redis_android_api_simplified = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_API_INVOKE)
        # ## self.redis_android_api_simplified.flushdb()
        # ## self.api_set = set()
        # ## self.txt_output_api = open("./Data/IntermediateData/api.txt", 'w')
        self.api_simplified_set = set()
        self.txt_invoke_format = open(SCRIPT_PATH + "/Data/IntermediateData/invokeFormat.txt", 'w')
        self.ignore_list = [
            "Ljava/lang",
            "Ljava/util/logging",
            "Landroid/util/Log",
            "Landroid/Manifest",
            "Landroid/R",
            "Landroid/test",
            "Ljunit",
            "Lorg/apache/commons/logging/Log"
        ]

    def __del__(self):
        """
            __del__
            StrictRedis doesn't implement close or quit methods.
            We don't need to close redis connection here.
        """
        self.txt_invoke_format.close()

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
            logger.critical("Jad is not runnable. please put `tool/jad` into your $PATH environment.")
            raise AssertionError
        if status == 256:
            pass
        else:
            logger.warning("Maybe there is something wrong with jad status.")

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
            logger.info("Decompiling %s" % jar)
            cmd = "./tool/jar_decompiler.sh " + jar
            os.popen(cmd)

    """
        Walk through the directories to find all the class names and methods (SDK API).


    """
    def walk_dir(self):
        for jar in self.jar_list:
            dir_to_be_walked = jar + ".dir"
            logger.info("Walk %s" % dir_to_be_walked)
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
                        self.read_java(full_path_name, class_name, jar)
                        # ## self.redis_class_name.incr(class_name)
            # clean the directory
            if CLEAN_WORKSPACE:
                logger.info("Cleaning the directory which is already walked.")
                os.system('rm -rf %s' % dir_to_be_walked)
        # ## logger.info("API Count is %d counting overloading." % len(self.api_set))
        logger.info("API Count is %d without overloading." % len(self.api_simplified_set))
        logger.info("Write the APIs into txt file as a backup.")
        # ## for api in self.api_set:
        # ##     self.txt_output_api.write(api + '\n')
        api_simplified_list = list()
        # Ignore those APIs that appears in ignore_list. Such as Landroid/util/Log
        ignore_cnt = 0
        for api_s in self.api_simplified_set:
            flag = True
            for ign_api in self.ignore_list:
                if ign_api in api_s:
                    flag = False
                    break
            if flag:
                api_simplified_list.append(api_s)
            else:
                ignore_cnt += 1
        logger.info("Ignore %d APIs" % ignore_cnt)
        for api_s in sorted(api_simplified_list):
            self.txt_invoke_format.write(api_s + '\n')

    def read_java(self, full_path_name, class_name, jar):
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
            if ('public' in line or 'protected' in line) and 'class' in line and brackets_count == 0:
                continue
            # inner class
            if ('public' in line or 'protected' in line) and 'class' in line and brackets_count == 1:
                current_inner_class = line.split('class')[1].strip()
                # if there's 'extends' here in this string
                if " " in current_inner_class:
                    current_inner_class = current_inner_class.split(' ')[0]
                continue
            if ('public' in line or 'protected' in line) and 'interface' in line and brackets_count == 1:
                current_inner_class = line.split('interface')[1].strip()
                if " " in current_inner_class:
                    current_inner_class = current_inner_class.split(' ')[0]
                continue
            # method (API)
            if ('public' in line or 'protected' in line) and '(' in line and ')' in line:
                left_part = line.split('(')[0]
                method_name = left_part.split(' ')[-1]
                return_type = left_part.split(' ')[-2]
                if "extends" in method_name:
                    pass
                if "extends" in return_type:
                    pass
                '''
                    if the value is public, that means the function is a constructive method.
                    I use '#' here to tag that the method does not have a return type.

                    If the value is not '#', the value is put into database 0 for a count.
                '''
                # ## if return_type == 'public' or return_type == 'protected':
                # ##     return_type = '#'
                # ## else:
                # ##     self.redis_class_name.incr(return_type)
                right_part = line.split('(')[1]
                # parameters of the method
                paras = []
                paras_number = len(right_part.split(' '))
                for i in range(paras_number):
                    if i % 2 == 0:
                        para_type = right_part.split(' ')[i]
                        # ## self.redis_class_name.incr(para_type)
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
                # ## method_declare = "%s %s->%s(%s)" % (return_type, full_class_name, method_name, parameters_string)
                point_to_slash = full_class_name.replace('.', '/')
                if method_name == class_name.split('.')[-1]:
                    method_name = "<init>"
                method_invoke = "L%s;->%s" % (point_to_slash, method_name)

                # ## self.redis_android_api_simplified.incr(method_invoke)
                # ## self.api_set.add(method_declare)
                # ## self.redis_android_api.incr(method_declare)
                self.api_simplified_set.add(method_invoke)

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
        logger.info("Creating an instance of ApiDictionaryGenerator")
        adg = ApiDictionaryGenerator()
        # add the jar into list.
        logger.info("Adding jar path into jar list")
        adg.add_jars(jar_list)
        # decompiling the jar file. decompiling is only needed once.
        logger.info("Decompiling jar")
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
    jar_file_list = glob.glob(SCRIPT_PATH + "/Data/RawData/*.jar")
    api_dict_generator_wrapper = ApiDictionaryGeneratorWrapper(jar_file_list)
