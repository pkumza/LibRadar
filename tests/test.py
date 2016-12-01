# -*- coding: utf-8 -*-

import os
import commands


cmd = "jadc"
status, out = commands.getstatusoutput('jasdcs')
print "OUTPUT is "
print out
print status
