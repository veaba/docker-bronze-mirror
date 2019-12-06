import re
import os
import time
from multiprocessing.pool import ThreadPool
import threading

IP_MAPS = {
    "127.0.0.1": "张三",
    "192.168.1.1": "李四"
}


# 根据ip获取用户名称
def get_name_by_ip(ip):
    return IP_MAPS[ip] or "未知"


def remove_newline(string=""):
    return string.replace('\n', '').strip()


# 返回{时间:ip}
def host_who():
    who = os.popen('who')
    std_lines = who.readlines()
    time_ip_map = {}
    for line in std_lines:
        time_and_ip = re.sub(r'^.*        ', '', line.strip())
        time_and_ip = time_and_ip.split(' (')
        ip = ""
        new_time = time_and_ip[0] + '00'
        if len(time_and_ip) == 2:
            ip = time_and_ip[1][0:-1]
        time_ip_map[new_time] = ip
    """
    {
        time:"ip",
        时间最近的在后面
    }ei
    """
    return time_ip_map


# 2019-11-28 22:11 转时间戳 => 1574950260
# 根据操作的时间和最近的登录日志获取到ip
# 返回登录时间：ip


def time_to_timestamp(time_str):
    # 转为时间数组
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timestamp = int(time.mktime(time_array))
    return timestamp


# 定时器 多线程执行函数
class SetTimeInterval(threading.Thread):
    def __init__(self, fn=None, second=1, clear=False):
        threading.Thread.__init__(self)
        self.fn = fn
        self.second = second
        self.clear = clear

    def run(self):
        while True:
            if self.clear:
                break
            time.sleep(self.second)
            self.fn()


# 延时器 多线程执行函数
class SetTimeOut(threading.Thread):
    def __init__(self, fn=None, second=1, clear=False):
        threading.Thread.__init__(self)
        self.fn = fn
        self.second = second
        self.clear = clear

    def run(self):
        time.sleep(self.second)
        self.fn()


# 定时器
# fn 执行函数，
# second 单位 秒，表示每x second 执行一次
# clear  入参，则打断
# def SetTimeInterval(fn, second, clear=False):
#     while True:
#         if clear:
#             break
#         time.sleep(second)
#         fn()


# 延时器
# def setTimeOut(fn, second):
#     time.sleep(second)
#     fn()


if __name__ == "__main__":
    # host_who()
    time_to_timestamp('2019-11-28 22:11:00')
