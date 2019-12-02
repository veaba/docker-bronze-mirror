# 执行python docker.py 在windows 下无法打印出来
import os

# 检查docker 僵死


def docker_check_is_dead(containerId):
    docker_dead_status = os.popen(
        'docker inspect --format="{{.State.Dead}}" '+containerId)
    dead_status_list = [status.replace('\n', '')
                        for status in list(docker_dead_status)]
    if 'true' in dead_status_list:
        return True
    else:
        return False

# 检查docker exit


def docker_check_is_exit(containerId):
    docker_exit_status = os.popen(
        'docker inspect --format="{{.State.Status}}" '+containerId)
    exit_status_list = [status.replace('\n', '')
                        for status in list(docker_exit_status)]
    if 'exited' in exit_status_list:
        return True
    else:
        return False

# 获取所有容器的信息组


def docker_get_all_containers_obj():
    containers_list = os.popen('docker ps -a')
    obj = {}
    the_list= list(containers_list)[1:]
    for line in the_list:
        info = [item for item in line.split('  ') if len(item)]
        id=info[0] or ''
        obj[id] = {
            'id': id,
            'container_id': id,
            'image': info[1] or '',
            'command': info[2] or '',
            'created': info[3] or '',
            'status': info[4] or '',
            'name': info[5] or ''
        }

    return obj

# 所有列表-所有容器


def docker_get_all_containers_list():
    containers_list = os.popen('docker ps -a -q')
    std_lines = containers_list.readlines()
    return [id.replace('\n', '') for id in std_lines]


# 活着列表-列出活着容器
def docker_get_live_containers_list():
    container_live_list = os.popen('docker ps -q')
    std_lines = container_live_list.readlines()
    return [id.replace('\n', '') for id in std_lines]

# 退出列表-列出退出容器的列表


def docker_get_exit_containers_list():
    container_exit_list = os.popen('docker ps -f STATUS=exited -q')
    std_lines = container_exit_list.readlines()
    return [id.replace('\n', '') for id in std_lines]

# 僵死列表-列出僵死容器的列表


def docker_get_dead_containers_list():
    all_containers = docker_get_all_containers_list()
    dead_ids = []
    for id in all_containers:
        if docker_check_is_dead(id):
            dead_ids.append(id)
    return dead_ids


# 列出镜像列表
def docker_image_list():
    container_live_list = os.popen('docker images -q')
    std_lines = container_live_list.readlines()
    return [id.replace('\n', '') for id in std_lines]


# todo 获取通过id 获取name
def docker_get_name_by_container_id():
    pass

# todo 判断容器列表中，谁被关闭了


# if __name__ == "__main__":
#     docker_get_all_containers_list()
