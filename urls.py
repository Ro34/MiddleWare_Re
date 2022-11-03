
# 平台心跳包
TO_PLATFORM_HEARTBEAT_IP = 'http://192.168.9.81'
TO_PLATFORM_HEARTBEAT_PORT = '5013'
TO_PLATFORM_HEARTBEAT_SERVICE = '/AiServer/Heartbeat'
TO_PLATFORM_HEARTBEAT_DATA = {
        'host': '172.18.60.77',
        'description': '测 试',
        'ftpUsername': '张伟',
        'ftpPassword': '123',
        'version': '1.3'
    }
#


# urls
url_to_platform_heartbeat = '{}:{}{}'.format(TO_PLATFORM_HEARTBEAT_IP, TO_PLATFORM_HEARTBEAT_PORT, TO_PLATFORM_HEARTBEAT_SERVICE)
data_to_platform_heartbeat = TO_PLATFORM_HEARTBEAT_DATA
