import  re 
import  os 
IP_MAPS={
    "127.0.0.1":"张三",
    "192.168.1.1":"李四"
}
# 根据ip获取用户名称
def get_name_by_ip(ip):
    return IP_MAPS[ip] or "未知"

def host_who():
    who=os.popen('who')
    std_lines= who.readlines()
    time_ip_map={}
    for line in std_lines:
        time_and_ip=re.sub(r'^.*        ','',line.strip())
        time_and_ip=time_and_ip.split(' (')
        time_ip_map[time_and_ip[0]]=time_and_ip[1][0:-1]
        print('---------')
        print(line)
        print('=========')
    print(time_ip_map)

# 2019-11-28 22:11 转时间戳 => 1574950260
def time_to_timestmap():
    pass

if  __name__ == "__main__":
    host_who()