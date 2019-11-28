import  re 
import  os 
import time
IP_MAPS={
    "127.0.0.1":"张三",
    "192.168.1.1":"李四"
}
# 根据ip获取用户名称
def get_name_by_ip(ip):
    return IP_MAPS[ip] or "未知"

# 返回{时间:ip}
def host_who():
    who=os.popen('who')
    std_lines= who.readlines()
    time_ip_map={}
    for line in std_lines:
        time_and_ip=re.sub(r'^.*        ','',line.strip())
        time_and_ip=time_and_ip.split(' (')
        ip=""
        time=time_and_ip[0]+'00'
        if len(time_and_ip)==2:
            ip=time_and_ip[1][0:-1]
        time_ip_map[time]=ip
        print('---------')
        print(line)
        print('=========')
    print(time_ip_map)
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
def time_to_timestmap(time_str):
    # 转为时间数组
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

if  __name__ == "__main__":
    # host_who()
    time_to_timestmap('2019-11-28 22:11:00')