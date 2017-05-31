from _settings import *
import redis
import math
import csv

db = redis.StrictRedis(db=2) #, password=DB_PSWD)

result = list()

THRESHOLD = 50

dict_tag_rules = dict()
new_prefix_list = list()
if os.path.exists(FILE_RULE):
    file_rules = open(FILE_RULE, 'r')
    csv_rules_reader = csv.reader(file_rules, delimiter=',', quotechar='|')
    for row in csv_rules_reader:
        dict_tag_rules[row[0]] = row[1]
    file_rules.close()


cursor = 0
for i in range(7255):#255):
    if i % 10 == 0:
        print ("Progress:%d" % i)
    res = db.hscan(name="feature_cnt", cursor=cursor, count=1000)
    cursor = res[0]
    for i in res[1]:
        if int(res[1][i]) > THRESHOLD:
            un_ob_pn = db.hget(name="un_ob_pn", key=i)
            flag = True
            for lib in dict_tag_rules:
                if lib == un_ob_pn:
                    if dict_tag_rules[lib] == "no":
                        flag = False
                        break
                    else:
                        result.append(un_ob_pn)
                    break
                elif len(lib) > len(un_ob_pn) :
                    continue
                elif lib[:len(un_ob_pn)] == un_ob_pn and dict_tag_rules[lib] != "no":
                    flag = False
                    break
            if flag == False:
                continue
            if 1 < len(un_ob_pn.split('/')) <= 3:
                result.append(un_ob_pn)


for r in result:
    print r
print len(result)
