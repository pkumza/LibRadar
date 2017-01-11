#coding:utf-8

from multiprocessing import Process, Queue, Pool
import multiprocessing
import os, time, random

# 写数据进程执行的代码:
def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    while True:
        if not q.empty():
            value = q.get(True)
            print 'Get %s from queue.' % value
            time.sleep(random.random())
        else:
            break


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    # 父进程创建Queue，并传给各个子进程：
    q = manager.Queue()
    p = Pool()
    pw = p.apply_async(write, args=(q,))
    time.sleep(0.5)
    pr = p.apply_async(read, args=(q,))
    p.close()
    p.join()

    print
    print '所有数据都写入并且读完'