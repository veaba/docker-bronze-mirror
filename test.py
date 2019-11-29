import time
# 测试父级执行1s，子级执行2s
import threading
from utils import SetTimeInteval,SetTimeOut

def parent():
    time.sleep(1)
    print('父级：',time.time())


def children():
    time.sleep(2)
    print('子级：',time.time())



if __name__ == "__main__":

    # todo 使用线程的情况下，可能存在一些误差，阻塞
    a1= SetTimeInteval(fn=parent,second=1)
    a1.start()

    a2= SetTimeOut(fn=children,second=1)
    a2.start()

    a3= SetTimeInteval(fn=children,second=1)
    a3.start()