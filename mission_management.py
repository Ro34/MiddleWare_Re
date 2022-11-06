import json

import urls
import requests
import database_management
import middle_args


# 任务管理
class MissionReply:
    pass


# 任务开始
class MissionStart:
    host_ip = '0'
    port = '0'

    def __init__(self, m):
        self.mission_type = m['missionType']
        self.platform_context = m['platformContext']
        self.taskid = self.platform_context.split(",")[0].split(":")[-1]
        self.aiTaskType = self.platform_context.split(",")[1].split(":")[-1][1:-2]

    resources_status = 0

    def resources_query(self):
        #请求服务器接口,获得一个return,传给resources_status
        resources_status = 0
        return resources_status

    def mission_reply(self, host_ip, port, platformContext, serverContext):
        data = {
            # 'host' :'192.168.9.99'  ,  # 服务器的 IP 或域名
            # 'port' :60082  ,  # 接受任务的服务端口
            'host': host_ip,
            'port': port,
            'platformContext': platformContext,  # 平台上下文字段，来自于任务队列中消息携带的 context
            'serverContext': serverContext,  # 服务器上下文字段，之后来自平台的消息都会原封不动携带该字段
        }
        # 如何在urls中管理带参数的字典？？？
        #响应平台
        res = requests.post(url=urls.url_to_platform_accept_mission, headers=urls.headers, data=json.dumps(data))

        self.server_context = serverContext

        if res.status_code == 200:
            print("mission accepted")
        # 还需要写其他情况

    def mission_start_AI_training(self):
        pass

    def mission_start_AI_marking(self):
        conname1 = requests.get(url='http://139.196.192.142:8011/startcontainer')
        return conname1.json()

    def creating_mission_item(self):
        tasker = database_management.MissionInfo()
        tasker.insert_database(self.taskid, self.mission_type, 'accept', MissionStart.host_ip, MissionStart.port, '',
                               self.platform_context, self.server_context, 0, 0, '')


class MissionMaintain:
    def __init__(self):
        self.hbdict = middle_args.HEART_BEAT_DICT

    def parse_heartbeat(self):
        return self.hbdict

    def update_progress(self):
        task = database_management.MissionInfo()
        task.query_database('SERVERCONTEXT', self.hbdict['serverContext'])

        data = {
            "progressText": "训练轮数(" + str(self.hbdict['epoch']) + "/" + str(self.hbdict['total_epoch']) + ")",
            "progress": task.dict['progress'] * 100,
            "platformContext": task.dict['PLATFORMCONTEXT']
        }

        res = requests.post(url=urls.url_to_platform_progress, headers=urls.headers, data=json.dumps(data))
        print(res)

    def update_database(self):
        task = database_management.MissionInfo()
        task.update_database('MISSIONSTATUS', self.hbdict['mission_status'], 'SERVERCONTEXT',
                             self.hbdict['serverContext'])


class MissionStop:
    def __init__(self, m):
        self.mission_type = m['missionType']
        self.platform_context = m['platformContext']
        self.taskid = self.platform_context.split(",")[0].split(":")[-1]
        self.aiTaskType = self.platform_context.split(",")[1].split(":")[-1][1:-2]
        self.server_context = m['serverContext']

    def get_mission_info(self):
        task = database_management.MissionInfo()
        task.query_database('SERVERCONTEXT', self.server_context)
        return task.dict

    def mission_stop_AI_training(self, task_dict):
        kill_pid = task_dict['PID']
        data = {
            'server_pid': kill_pid
        }
        res = requests.post(url=urls.url_to_server_training_stop,headers=urls.headers,data=json.dumps(data))
        print(res)

    def mission_stop_AI_marking(self, task_dict):
        stop_conname = task_dict['CONTAINERNAME']
        data = {
            "container_name": stop_conname
        }

        res = requests.post(url=urls.url_to_server_marking_stop,
                      headers=urls.headers,
                      data=json.dumps(data))
        print(res)


