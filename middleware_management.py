# 心跳包
import json

import requests

import urls


# 心跳包类
class HeartBeat:

    def __init__(self, url, data):
        self.url = url
        self.data = data

    def heartbeat(self):
        res = requests.post(url=self.url, headers={"Content-Type": "application/json"}, data=json.dumps(self.data))
        print("发送心跳包" + urls.url_to_platform_heartbeat)
        print(res.text)



# 向平台发送实例化
platform_heartbeat = HeartBeat(urls.url_to_platform_heartbeat, urls.data_to_platform_heartbeat)
