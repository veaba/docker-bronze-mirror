# docker-bronze-mirror docker青铜镜


## 功能

- 分布式，集群监控(webscoket主动监控)
- HTTPS 加密 （todo）
- docker 精密级监控
- 自动检测xxx


## 吐槽！

网上的python版本的socket.io 是什么情况？？？恩？？？？

我都想重写一个python 版本的socket.io了！

宕机、容器启动等通过websocket 推送消息


- actions       动作
- containers    容器
- images        镜像
- app           应用
- docker        docker
- screens       大屏
- status        状态
- websocket     websocket
- healthy       心跳
- host 宿主     宿主机
- notify        通知
- webhooks      webhooks
- im            即时消息
- channel       通道
- utils         工具类库
# python 版本 3.7.2 32-bit 

## 如果出现 

可能是项目顶层文件存在诸如websocket.py 的文件！

> AttributeError: module 'socketio' has no attribute 'Server'

(这个dir 打印奇葩的是，过一会才出现，这更好玩)


## notify

<font color=\"warning\">【B级】：<font>检测到容器退出！\n 

> 节点 159.138.2.51 
> 容器ID：3df85570271c
> 服务名称：distracted_margulis
> 状态：Exited (0)
> 威胁等级 →_→：获得残暴（Burtal）记录


## 线程

### 相互之前不影响的线程定时器独立
- 某a 每1s 执行一次
- 某b 每2s 执行一次


## refenerce

- https://tutorialedge.net/python/python-socket-io-tutorial/