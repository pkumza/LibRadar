# -*- coding:utf-8 -*-
# Created at 2015/10/17
# Recently Modified at 2015/10/17
# Current Version 1.2.0

__author__ = 'Zachary Marv - 马子昂'

import time

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
