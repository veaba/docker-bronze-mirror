from utils import setTimeInteval,setTimeOut
from docker import docker_get_all_containers_list,docker_get_live_containers_list,docker_image_list
# 青铜镜类
class DockerBronzeMirror():
    # todo 
    def __init__(self):
        self.container=[]           # todo 全部参数
        self.all_containers=[]      # 全部的容器列表
        self.live_containers=[]     # 存储的容器列表
        self.dead_contianers=[]     # 僵死的容器列表
        self.images=[]              # 镜像列表

    @staticmethod
    def run(self):
        print('run~~~~~')
        self._docker_check_dead()
        pass
    
    # ------------------------- 青铜镜-内置方法 ---------------------------#
    # todo 检查到容器死掉，则发送警告
    @staticmethod
    def _docker_check_dead(self):
        pass

    # ------------------------- 青铜镜-公开方法 ---------------------------#
    # todo 需要每 x秒 就存储 活着 容器的id列表
    @staticmethod
    def get__docker_live_containers():
        pass

    # todo 需要每 x秒 就存储 全部 容器的id列表，
    @staticmethod
    def get_docker_all_containers(self):
        self.all_containers=docker_get_all_containers_list()
    
    # todo 需要每 x秒 就存储 退出的容器id列表
    @staticmethod
    def get_docker_exit_containers():
        pass

    # todo 需要每 x秒 就存储 镜像id 列表
# 实例化青铜镜

docker_bronze_mirror= DockerBronzeMirror()
setTimeInteval(docker_bronze_mirror.run,2) # 每x秒执行一次


