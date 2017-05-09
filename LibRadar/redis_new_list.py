import redis
from _settings import *
import logging

db = redis.StrictRedis(host="redis.pkuos.org", port=DB_PORT, db=0, password=DB_PSWD)

for i in range(2167):
    a = db.lrange(name="apk_queue", start=-1000-i*1000, end=-1-i*1000)
    multi = db.pipeline(transaction=False)
    for j in a:
        if j.startswith("New ") or j.startswith("UpdateVersion "):
            multi.rpush("apk_new_3", j)
    multi.execute()
    logging.info("%d", i)