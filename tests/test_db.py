# -*- coding: utf-8 -*-
"""
    Test Database

    I have analysed 3048 APKs in 2017-1-7.
    Some features are already put into database.

    This script is used to exam the information in database.
"""

"""
Test db case 1
"""

def case1():
    import redis

    db3 = redis.StrictRedis(db=3)
    db4 = redis.StrictRedis(db=4)
    db5 = redis.StrictRedis(db=5)

    for key in db3.keys():
        if int(db3.get(key)) > 100:
            if int(db4.get(key)) > 10:
                print "PackageName :", db5.get(key)
                print "Count       :", db3.get(key)
                print "Weight      :", db4.get(key)
                print "-------"

def case2():
    import redis

    db3 = redis.StrictRedis(db=3)
    db4 = redis.StrictRedis(db=4)
    db5 = redis.StrictRedis(db=5)

    for key in db3.keys():
        if int(db3.get(key)) > 10:
            if int(db4.get(key)) > 100:
                print "PackageName :", db5.get(key)
                print "Count       :", db3.get(key)
                print "Weight      :", db4.get(key)
                print "-------"

if __name__ == "__main__":
    case2()