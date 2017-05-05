import redis
from _settings import *
import logging

db = redis.StrictRedis(host="redis.pkuos.org", port=DB_PORT, db=0, password=DB_PSWD)



for i in range(1164):
    a = db.lrange(name="apk_queue", start=-1000-i*1000, end=-1-i*1000)
    multi = db.pipeline(transaction=False)
    for j in a:
        if j.startswith("New "):
            multi.rpush("apk_new_2", j)
    multi.execute()
    logging.info("%d", i)