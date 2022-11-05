import urls
import requests
import database_management
# 任务管理
class MissionReply:




#
class MissionStart:

    host_ip = '0'
    port = '0'

    def __init__(self, m):
        self.mission_type = m['missionType']
        self.platform_context = m['platformContext']
        self.taskid = self.platform_context.split(",")[0].split(":")[-1]
        self.aiTaskType = self.platform_context.split(",")[1].split(":")[-1][1:-2]

    resources_status = 0

    def resources_query(self, resources_status):
        MissionStart.resources_status = 0


    def mission_distribute(self,host_ip,port,platformContext,serverContext):

        data = {
            # 'host' :'192.168.9.99'  ,  # 服务器的 IP 或域名
            # 'port' :60082  ,  # 接受任务的服务端口
            'host': host_ip,
            'port': port,
            'platformContext': platformContext,  # 平台上下文字段，来自于任务队列中消息携带的 context
            'serverContext': serverContext,  # 服务器上下文字段，之后来自平台的消息都会原封不动携带该字段
        }
        #如何在urls中管理带参数的字典？？？
        res = requests.post(url=urls.url_to_platform_accept_mission,headers=urls.headers,data=data)

        self.server_context = serverContext

        if res.status_code == 200:
            print("mission accepted")
        #还需要写其他情况

    def mission_start_AI_training(self):
        pass

    def mission_start_AI_marking(self):
        #调用接口
        #启动脚本
        pass


    def creating_mission_item(self):

        tasker = database_management.MissionInfo()
        tasker.insert_database(self.taskid, self.mission_type, 'accept', MissionStart.host_ip, MissionStart.port, '', self.platform_context, self.server_context, 0, 0, '')


class MissionMaintain:

    def parse_heartbeat(self):
        pass

    def update_progress(self):
        pass

    def update_database(self):
        pass


class MissionStop:

    def get_mission_info(self):
        pass

    def mission_stop_AI_training(self):
        pass

    def mission_stop_AI_marking(self):
        pass
