# header
headers = {
    "Content-Type": "application/json"
}

# 平台心跳包
PLATFORM_IP = 'http://192.168.9.81'
PLATFORM_PORT = '5013'
TO_PLATFORM_HEARTBEAT_SERVICE = '/AiServer/Heartbeat'
TO_PLATFORM_HEARTBEAT_DATA = {
    'host': '172.18.60.77',
    'description': '测 试',
    'ftpUsername': '张伟',
    'ftpPassword': '123',
    'version': '1.3'
}
# 接受任务
TO_PLATFORM_ACCEPT_MISSION_SERVICE = '/AiServer/AcceptMission'

TO_PLATFORM_ACCEPT_MISSION_DATA = {
    'host': {},
    'port': {},
    'platformContext': {},  # 平台上下文字段，来自于任务队列中消息携带的 context
    'serverContext': {}
}

# urls
url_to_platform_heartbeat = '{}:{}{}'.format(PLATFORM_IP, PLATFORM_PORT,
                                             TO_PLATFORM_HEARTBEAT_SERVICE)
data_to_platform_heartbeat = TO_PLATFORM_HEARTBEAT_DATA

url_to_platform_accept_mission = '{}:{}{}'.format(PLATFORM_IP, PLATFORM_PORT,
                                                  TO_PLATFORM_ACCEPT_MISSION_SERVICE)
data_to_platform_accept_mission = TO_PLATFORM_ACCEPT_MISSION_DATA, (host_ip)
