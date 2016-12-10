# -*- coding: utf-8 -*-
"""
    API_Dict.py

    This is the first step for data collection.

    Firstly, get android.jar in Android SDK folder.

"""

import os
import commands
import redis

#TODO: Databases were made for? To be completed.
"""
    Information about Database.
    Redis is used here and the default setting points to localhost:6379
    If your Redis IP and Port is different, you can change the value here.
    In my redis.conf, I set 32 for the maximum number of databases.
    What's the databases for?

        0 : Android.jar Classes

"""
db_host = 'localhost'
db_port = 6379
db_id = 0

"""
    Implementation for Singleton
"""
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


"""
    A class used for collecting API data
"""
class API_Dictionary_Generator(Singleton):

    def __init__(self):
        self.jar_list = []
        self.redis_database = redis.StrictRedis(host=db_host, port=db_port, db=db_id)

    """
        Test if jad command exists.
        Run `jad` command as a test. If the status is 32512, it means that system cannot
            find the `jad` command. If the response is 256, `jad` can be run but `jad`
            cannot runs stably without arguments. If the status is neither 32512 nor 256,
            I don't know what happened.
    """
    def if_jad_exists(self):
        # run `jad` command as a test.
        # if
        status, out = commands.getstatusoutput('jad')
        if status == 32512:
            print("jad is not runnable. please put `tool/jad` into your $PATH environment.")
            raise AssertionError
        if status == 256:
            pass
        else:
            print("something wrong with jad status. if you don't think this is wrong, " \
                  "just remove the raise after.")
            raise AssertionError

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
        print(self.jar_list)

    def add_jars(self, jar_files):
        self.jar_list.extend(jar_files)
        print(self.jar_list)

    """
        Use jad to decompile jar file into android.jar.dir

        Step:
            1 - Unzip .jar file
            2 - use jad to decompile .class file into .java file.
    """
    def decompile_jar(self):
        self.if_jad_exists()
        for jar in self.jar_list:
            cmd = "../tool/jardecompiler.sh ../Data/RawData/" + jar
            print(cmd)
            os.system(cmd)

    """
        Walk through the directories to find all the class names and methods (SDK API).


    """
    def walk_dir(self):
        for jar in self.jar_list:
            dir_2B_walked = "../Data/RawData/" + jar + ".dir"
            print("Walk:")
            # TODO: turn java source into tree.
            # That's simple, try to identify public type method(type),
            # 找到 函数的特点 类的特点 内部类的特点 以及构造函数的特点即可

            # TODO: Redis 的 INCR 是线程安全的，所以可以尝试多线程来完成这一步的操作。
            for dirName, subdirList, fileList in os.walk(dir_2B_walked):
                print("Directory %s" % dirName)
                for filename in fileList:
                    if len(filename) > 4 and filename[-5:] == ".java":
                        full_path_name = '/'.join(dirName.split('/')[4:]) + '/' + filename
                        print("\t%s" % full_path_name)
                        class_name = full_path_name[:-5].replace('/','.')
                        self.redis_database.incr(class_name)


adg = API_Dictionary_Generator()
adg.add_jar('android24.jar')
'''decompiling is only needed once.'''
# adg.decompile_jar()
adg.walk_dir()
