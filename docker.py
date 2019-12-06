# 执行python docker.py 在windows 下无法打印出来
import os
from utils import remove_newline


# 检查docker 僵死
def docker_check_is_dead(container_id):
    docker_dead_status = os.popen(
        'docker inspect --format="{{.State.Dead}}" ' + container_id)
    dead_status_list = [status.replace('\n', '')
                        for status in list(docker_dead_status)]
    if 'true' in dead_status_list:
        return True
    else:
        return False


# 检查docker 退出
def docker_check_is_exit(container_id):
    docker_exit_status = os.popen(
        'docker inspect --format="{{.State.Status}}" ' + container_id)
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
    the_list = list(containers_list)[1:]
    for line in the_list:
        info = [item for item in line.split('  ') if len(item)]
        # 补全没有ports的情况
        if len(info) < 7:
            info.insert(5, '')
        container_id = remove_newline(info[0] or '')
        obj[container_id] = {
            'id': container_id,
            'container_id': container_id,
            'image': remove_newline(info[1] or ''),
            'command': remove_newline(info[2] or ''),
            'created': remove_newline(info[3] or ''),
            'status': remove_newline(info[4] or ''),
            'ports': remove_newline(info[5] or ''),
            'names': remove_newline(info[6] or '')
        }
    return obj


# 所有列表-所有容器
def docker_get_all_containers_list():
    containers_list = os.popen('docker ps -a -q')
    std_lines = containers_list.readlines()
    return [all_id.replace('\n', '') for all_id in std_lines]


# 活着列表-列出活着容器
def docker_get_live_containers_list():
    container_live_list = os.popen('docker ps -q')
    std_lines = container_live_list.readlines()
    return [live_id.replace('\n', '') for live_id in std_lines]


# 退出列表-列出退出容器的列表
def docker_get_exit_containers_list():
    container_exit_list = os.popen('docker ps -f STATUS=exited')
    temp_list = container_exit_list.readlines()
    temp_list = temp_list[1:]
    exit_list = []
    for line in temp_list:
        the_item = [item for item in line.split('  ') if len(item)]
        # 补全没有ports的情况
        if len(the_item) < 7:
            the_item.insert(5, '')
        obj = {
            'id': remove_newline(the_item[0] or ''),
            'container_id': remove_newline(the_item[0] or ''),
            'image': remove_newline(the_item[1] or ''),
            'command': remove_newline(the_item[2] or ''),
            'created': remove_newline(the_item[3] or ''),
            'status': remove_newline(the_item[4] or ''),
            'ports': remove_newline(the_item[5] or ''),
            'names': remove_newline(the_item[6] or '')
        }
        exit_list.append(obj)
    return exit_list


# 僵死列表-列出僵死容器的列表
def docker_get_dead_containers_list():
    all_containers = docker_get_all_containers_list()
    dead_ids = []
    for dead_id in all_containers:
        if docker_check_is_dead(dead_id):
            dead_ids.append(dead_id)
    return dead_ids


# 列出镜像列表
def docker_image_list():
    container_live_list = os.popen('docker images -q')
    std_lines = container_live_list.readlines()
    return [image_id.replace('\n', '') for image_id in std_lines]


# todo 获取通过id 获取name
def docker_get_name_by_container_id():
    pass

# todo 判断容器列表中，谁被关闭了


# if __name__ == "__main__":
#     docker_get_all_containers_list()
