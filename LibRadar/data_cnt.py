from _settings import *
import redis
import math

db = redis.StrictRedis(host=DB_HOST,port=DB_PORT, db=2, password=DB_PSWD)

counter = dict()
for i in range(100):
    counter[i] = 0

po_list = []

cursor = 0
for i in range(7255):
    if i % 10 == 0:
        print ("Progress:%d" % i)
    ct = 1000
    if i == 7254:
        ct = 946
    res = db.hscan(name="feature_cnt", cursor=cursor, count=ct)
    cursor = res[0]
    for k in res[1]:
        counter[int(math.log(float(res[1][k]),2))] += 1
        if int(res[1][k]) > 2000 :
            anwser = db.hget(name="feature_weight", key=k)
            po_list.append((int(anwser),db.hget(name="un_ob_pn", key=k)))

print counter
po_list.sort(key=lambda x:(-x[0]))
for item in po_list:
    print item