from utils import SetTimeInteval,SetTimeOut
from docker import docker_get_all_containers_list,docker_get_live_containers_list,docker_image_list,docker_check_is_dead,docker_check_is_exit
from notify import  notify_docker_is_dead,notify_docker_is_exit
# 青铜镜类
class DockerBronzeMirror():
    # todo 
    def __init__(self):
        self.container=[]           # todo 全部参数
        self.all_containers=[]      # 全部的容器列表
        self.live_containers=[]     # 存储的容器列表
        self.dead_containers=[]     # 僵死的容器列表
        self.exit_containers=[]     # 退出的容器列巴
        self.images=[]              # 镜像列表

    @staticmethod
    def run(self):
        print('run~~~~~')
        self.docker_check_dead()
        pass
    
    # ------------------------- 青铜镜-内置方法 ---------------------------#
    # todo 检查到容器死掉，则发送警告
    # @staticmethod
    def docker_check_dead(self):
        dead_ids=[]
        for id in self.all_containers:
            if docker_check_is_dead(id):
                notify_docker_is_dead(id)
                dead_ids.append(id)


    # todo 检查到容器退出，则发送警告
    # @staticmethod
    def docker_check_exit(self):
        exit_ids=[]
        for id in self.exit_containers:
            if docker_check_is_exit(id):
                notify_docker_is_exit(id)
                exit_ids.append(id)
                
    # ------------------------- 青铜镜-公开方法 ---------------------------#
    # todo 需要每 x秒 就存储 活着 容器的id列表
    # @staticmethod
    def get__docker_live_containers(self):
        pass

    # todo 需要每 x秒 就存储 全部 容器的id列表，
    def get_docker_all_containers(self):
        self.all_containers=docker_get_all_containers_list()
    
    # todo 需要每 x秒 就存储 退出的容器id列表
    # @staticmethod
    def get_docker_exit_containers(self):
        pass

    # todo 需要每 x秒 就存储 镜像id 列表

if __name__ == "__main__":
    # 实例化青铜镜

    docker_bronze_mirror= DockerBronzeMirror()

    # 每1s 获取一次全部容器ids
    all_docker_containers=SetTimeInteval(docker_bronze_mirror.get_docker_all_containers,1) # 每x秒执行一次
    all_docker_containers.start()

    # # 每3s 执行一次检查容器僵死
    dead_docker_containers=SetTimeInteval(docker_bronze_mirror.docker_check_dead,3)
    dead_docker_containers.start()

    # 每5s 执行一次检查容器exit
    exit_docker_containers=SetTimeInteval(docker_bronze_mirror.docker_check_exit,10)
    exit_docker_containers.start()




