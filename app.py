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
from utils import SetTimeInteval, SetTimeOut
from docker import docker_get_exit_containers_list, docker_get_all_containers_list, docker_get_live_containers_list, docker_image_list, docker_check_is_dead, docker_check_is_exit, docker_get_dead_containers_list,docker_get_all_containers_obj
from notify import notify_docker_is_dead, notify_docker_is_exit
from datetime import datetime
import sys
# 青铜镜类


class DockerBronzeMirror():
    # todo
    def __init__(self, ip=""):
        self.ip = ip                        # 服务器ip
        self.all_containers_obj={}         # 所有容器的对象 
        self.container = []                 # todo 全部参数
        self.all_containers = []            # 全部的容器列表
        self.live_containers = []           # 存储的容器列表
        self.dead_containers = []           # 僵死的容器列表
        self.exit_containers = []           # 退出的容器列巴
        self.images = []                    # 镜像列表

    @staticmethod
    def run(self):
        print('run~~~~~')
        self.docker_check_dead()
        pass

    # ------------------------- 青铜镜-内置方法 ---------------------------#
    # docker 心跳，每1s执行一次

    def docker_heart_beat(self):

        # 所有容器的信息
        self.all_containers_obj=docker_get_all_containers_obj()
    
        # 所有容器
        self.all_containers = docker_get_all_containers_list()

        # 退出容器
        self.exit_containers = docker_get_exit_containers_list()

        # 活着容器
        self.live_containers = docker_get_live_containers_list()

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
        print('*****************'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'*************************')

    # todo 检查到容器死掉，则发送警告
    # @staticmethod

    def docker_check_dead(self):
        for id in self.dead_containers:
            if docker_check_is_dead(id):
                notify_docker_is_dead(id)

    # todo 检查到容器退出，则发送警告
    # @staticmethod
    def docker_check_exit(self):
        for id in self.exit_containers:
            # todo 过滤
            if docker_check_is_exit(id) and not('order' in self.all_containers_obj[id]['name'] or 'coupon' in self.all_containers_obj[id]['name']):
                current_item=self.all_containers_obj[id]
                current_item['ip']=self.ip
                current_item['level']='B'
                notify_docker_is_exit(current_item)

    # ------------------------- 青铜镜-公开方法 ---------------------------#
    # todo 需要每 x秒 就存储 活着 容器的id列表
    # @staticmethod
    def get__docker_live_containers(self):
        pass

    # todo 需要每 x秒 就存储 全部 容器的id列表，
    def _get_docker_all_containers(self):
        self.all_containers = docker_get_all_containers_list()

    # todo 需要每 x秒 就存储 退出的容器id列表
    # @staticmethod
    def get_docker_exit_containers(self):
        pass

    # todo 需要每 x秒 就存储 镜像id 列表


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
    heart_beat = SetTimeInteval(
        docker_bronze_mirror.docker_heart_beat, 1)  # 每x秒执行一次
    heart_beat.start()

    # # 每3s 执行一次检查容器僵死
    # dead_docker_containers = SetTimeInteval(
    #     docker_bronze_mirror.docker_check_dead, 3)
    # dead_docker_containers.start()

    # 每5s 执行一次检查容器exit
    exit_docker_containers = SetTimeInteval(
        docker_bronze_mirror.docker_check_exit, 5)
    exit_docker_containers.start()
