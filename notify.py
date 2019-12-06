"""
@desc 推送消息的类型
@todo 将推送的日志都异步写到notify.log 日志文件里面去

"""

import requests
import re
import json
from config import post_url

# 动作
ACTIONS = {

}
NOTIFY = {
    "SOME_ONE_LOGIN": 1,  # 有人在登录
    "DOCKER_IS_CLOSE": 2,  # docker 在关闭
}

# 警告类型1
NOTIFY_TYPE = {
    "SOME_ONE_CLOSE_DOCKER": 1,  # 有人关闭docler
    "DOCKER_IS_DOWN_FOR_THREE_MINUTES": 2,  # docker 宕机 x 分钟
}

""""
@desc d->sss  low->high
"""
LEVEL = {
    "SSS": "获得举世震惊（SSSensational）成就！！！",
    "SS": "获得超级虐待狂（SSadistic）",
    "S": "获得灭绝人性（Savage）记录",
    "A": "获得无法无天（Anarchic）记录",
    "B": "获得残暴（Burtal）记录",
    "C": "烦死了心情！",
    "D": "日常搞事",
}
"""
@desc 谁关闭了docker 触发
@who  {ip:xxx,name:xxx,time:xxx}
@docker {name:xx,ip:xx,level:xxx}

"""


def notify_who_shut_down_the_docker(who, docker):
    pass


"""
@desc 僵死推送 docker

"""


def notify_docker_is_dead(obj=None):
    if obj is None:
        obj = {}
    body = {
        'msgtype': 'markdown',
        'markdown': {
            'content': '<font color="warning">【' + obj['level'] + '级】</font>：检测到容器僵死！ \n'
                       + '> **节点：** <font color="comment">' + obj['ip'] + '</font>\n'
                       + '> **容器ID：** <font color="comment">' + obj['id'] + '</font>\n'
                       + '> **服务名称：** <font color="comment">' + obj['names'] + '</font>\n'
                       + '> **状态：** <font color="comment">' + obj['status'] + '</font>\n'
                       + '> **威胁级别：** <font color="comment">' +
                       LEVEL[obj['level']] + '</font>\n'
                       + '请相关人员处理!\n'
        }
    }
    res = requests.post(post_url, data=json.dumps(body), headers={
        'content-type': 'application/json'})
    print(res.text)


"""
@desc 退出（exit）推送 docker 
"""


def notify_docker_is_exit(obj):
    body = {
        'msgtype': 'markdown',
        'markdown': {
            'content': '<font color="warning">【' + obj['level'] + '级】</font>：检测到容器退出！ \n'
                       + '> **节点：** <font color="comment">' + obj['ip'] + '</font>\n'
                       + '> **容器ID：** <font color="comment">' + obj['id'] + '</font>\n'
                       + '> **服务名称：** <font color="comment">' + obj['names'] + '</font>\n'
                       + '> **状态：** <font color="comment">' + obj['status'] + '</font>\n'
                       + '> **威胁级别：** <font color="comment">' +
                       LEVEL[obj['level']] + '</font>\n'
                       + '请相关人员处理!\n'
        }
    }
    res = requests.post(post_url, data=json.dumps(body), headers={
        'content-type': 'application/json'})
    print(res.text)


"""
@desc 容器丢失（lost）推送 docker
"""


def notify_docker_is_lost(obj):
    body = {
        'msgtype': 'markdown',
        'markdown': {
            'content': '<font color="warning">【' + obj['level'] + '级】</font>：检测到服务丢失，可能有人在重启容器！ \n'
                       + '> **节点：** <font color="comment">' + obj['ip'] + '</font>\n'
                       + '> **服务名称：** <font color="comment">' + obj['names'] + '</font>\n'
                       + '> **状态：** <font color="comment">可能在重启</font>\n'
                       + '> **威胁级别：** <font color="comment">' +
                       LEVEL[obj['level']] + '</font>\n'
                       + '请咨询相关人员处理!\n'
        }
    }
    res = requests.post(post_url, data=json.dumps(body), headers={
        'content-type': 'application/json'})
    print(res.text)


if __name__ == "__main__":
    notify_docker_is_dead('111')
