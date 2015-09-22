# -*- coding:utf-8 -*-
# Created at 2015/9/15
# Recently Modified at 2015/09/15


__author__ = 'Zachary Marv - 马子昂'

"""
    LibRadar is a tool for detecting third-party libraries in Android apps accurately and instantly.
    Tag_Dict.py is a python script for tagging permissions on new_dict.dat
"""

import json

origin_dict = open('../data/new_dict.dat', 'r')
target_dict = open('tagged_dict.txt', 'w')

api_dict = {}
# -- Loading API Dict
for line in origin_dict:
    # print line
    u = json.loads(line)
    api_dict[u['key']] = {'v': u['value'], 'p': []}

p_scout = open('pscout_all_api_4.1.1.txt', 'r')
cur_p = ""
for line in p_scout:
    if len(line) > 10 and line[:11] == "Permission:":
        cur_p = line[11:]
    if len(line) > 1 and line[0] == '<':
        parts = line[1:line.index('(')].split(' ')
        api = 'L'+parts[0][:-1].replace('.', '/') + ';->' + parts[2] + '('
        if api in api_dict:
            api_dict[api]['p'].append(cur_p[19:-1])

for k in api_dict:
    if len(api_dict[k]['p']) == 0:
        item = {'k': k, 'v': api_dict[k]['v']}
    else:
        item = {'k': k, 'v': api_dict[k]['v'], 'p': api_dict[k]['p']}
    target_dict.write(json.dumps(item)+'\n')

origin_dict.close()
target_dict.close()
p_scout.close()