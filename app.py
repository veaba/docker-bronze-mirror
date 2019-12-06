"""
@集群模块
    todo 分布式部署，集群监控（通过websocket 的方式实现，心跳为1s）
    todo 静默式执行脚本
    todo 跟随服务器自动启动
    todo 一键重连
    todo 增加master 和集群模式
    todo 一键加入集群，增加授权
    todo 监控加入到本集群的网络和从节点机器
    todo 从节点也可以查看父节点情况
    todo 主节点挂了怎么办？选举模式推选master 节点


"""
from utils import SetTimeInterval, SetTimeOut
from docker import docker_get_exit_containers_list, docker_get_all_containers_list, docker_get_live_containers_list, \
    docker_image_list, docker_check_is_dead, docker_check_is_exit, docker_get_dead_containers_list, \
    docker_get_all_containers_obj
from notify import notify_docker_is_dead, notify_docker_is_exit, notify_docker_is_lost
from datetime import datetime
import sys
import re


# 青铜镜类


class DockerBronzeMirror:
    def __init__(self, ip="61.174.254.105", ignore=None):
        # 默认填补忽略的容器名
        if ignore is None:
            ignore = ['report', 'order', 'bill', 'activity']
        self.ip = ip  # 服务器ip
        self.all_containers_obj = {}  # 所有容器的对象
        self.all_containers = []  # 全部的容器列表
        self.live_containers = []  # 存储的容器列表
        self.dead_containers = []  # 僵死的容器列表
        self.exit_containers = []  # 退出的容器列表
        self.images = []  # 镜像列表

        # ignore 暂时用不到的服务
        self.ignore_containers = ignore

        # 常用的容器，如果不见了则发出警报
        self.exist_containers = ['crm', 'integration', 'webchatslzt', 'activity', 'coupon', 'etl',
                                 'customer']  # 常用的容器列表

    def run(self):
        print('run~~~~~')
        self.docker_check_dead()
        pass

    # ------------------------- 青铜镜-内置方法 ---------------------------#
    def _is_ignore_container(self, container_name):
        container_name = re.sub(r'-server.*$', '', container_name)
        if container_name in self.ignore_containers:
            return True
        else:
            return False

    # ------------------------- 青铜镜-系统方法 ---------------------------#
    # docker 心跳，每1s执行一次

    def docker_heart_beat(self):

        # 所有容器的信息
        self.all_containers_obj = docker_get_all_containers_obj()

        # 所有容器
        self.all_containers = docker_get_all_containers_list()

        # 退出容器
        self.exit_containers = docker_get_exit_containers_list()

        # 活着容器
        self.live_containers = docker_get_live_containers_list()

        # todo 容器不见，通过kill、stop、rm的方式

        # 镜像列表
        self.images = docker_image_list()

        # 僵死容器
        self.dead_containers = docker_get_dead_containers_list()

        # 打印

        # print('===> 容器信息：', self.all_containers_obj)
        # print('===> 所有容器：', self.all_containers)
        # print('===> 退出容器：', self.exit_containers)
        # print('===> 活着容器：', self.live_containers)
        # print('===> 僵死容器：', self.dead_containers)
        # print('===> 镜像列表：', self.images)
        # print('*****************'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'*************************')

    # 检查到容器死掉，则发送警告
    def docker_check_dead(self):
        for container_id in self.dead_containers:
            if docker_check_is_dead(container_id):
                current_item = self.all_containers_obj[container_id]
                current_item['ip'] = self.ip
                current_item['level'] = 'C'
                notify_docker_is_dead(current_item)

    # 检查到容器不见，通过kill、stop、rm的方式
    def docker_check_lost(self):
        lost_labels_name = []
        for container_id in self.all_containers:
            obj = self.all_containers_obj[container_id] or {}
            the_name = obj['names'].strip()
            the_name = re.sub(r'-server.*$', '', the_name)
            lost_labels_name.append(the_name)

        # 存在现在的容器名列表
        # print('现在存在的容器名列表===>', lost_labels_name)
        # print('需要检测的容器名列表===>', self.exist_containers)
        for label_name in self.exist_containers:
            if label_name not in lost_labels_name:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '容器不见===>', label_name)
                notify_docker_is_lost({
                    'ip': self.ip,
                    'names': label_name + '-server',
                    'level': 'C'
                })

    # 检查到容器退出(exit)，则发送警告
    def docker_check_exit(self):
        for item in self.exit_containers:
            if docker_check_is_exit(item['container_id']):
                # 过滤无关容器名词
                if not (self._is_ignore_container(item['names'])):
                    current_item = item
                    current_item['ip'] = self.ip
                    current_item['level'] = 'B'
                    notify_docker_is_exit(current_item)
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '容器退出检测：===>', current_item)

    # ------------------------- 青铜镜-公开方法 ---------------------------#
    # todo 需要每 x秒 就存储 活着 容器的id列表
    def get__docker_live_containers(self):
        pass

    # 需要每 x秒 就存储 全部 容器的id列表，
    def _get_docker_all_containers(self):
        self.all_containers = docker_get_all_containers_list()

    # todo 需要每 x秒 就存储 退出的容器id列表
    def get_docker_exit_containers(self):
        pass


if __name__ == "__main__":
    # 实例化青铜镜

    print(sys.argv)

    ip = ""

    for arg in sys.argv:
        if 'ip=' in arg:
            ip = arg[3:]
            break

    docker_bronze_mirror = DockerBronzeMirror(ip=ip)

    # 容器心跳，获取所有容器，活着的容器、退出的容器、僵死容器
    heart_beat = SetTimeInterval(
        docker_bronze_mirror.docker_heart_beat, 1)  # 每x秒执行一次
    heart_beat.start()

    # 每30s 执行一次检查容器僵死
    dead_docker_containers = SetTimeInterval(
        docker_bronze_mirror.docker_check_dead, 30)
    dead_docker_containers.start()

    # 每10s 执行一次检查容器是否不见了
    lost_docker_containers = SetTimeInterval(
        docker_bronze_mirror.docker_check_lost, 10
    )
    lost_docker_containers.start()

    # 每5s 执行一次检查容器exit
    exit_docker_containers = SetTimeInterval(
        docker_bronze_mirror.docker_check_exit, 5)
    exit_docker_containers.start()
