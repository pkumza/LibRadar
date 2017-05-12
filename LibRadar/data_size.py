from _settings import *
import redis
import math

db = redis.StrictRedis(host=DB_HOST,port=DB_PORT, db=2, password=DB_PSWD)

counter = dict()
for i in range(100):
    counter[i] = 0



cursor = 0
for i in range(7255):
    if i % 10 == 0:
        print ("Progress:%d" % i)
    res = db.hscan(name="feature_weight", cursor=cursor, count=1000)
    cursor = res[0]
    for k in res[1]:
        counter[int(math.log(float(res[1][k]),2))] += 1

print counter