import urls
import requests
import database_management
import middle_args
# 任务管理
class MissionReply:
    pass



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

    def __init__(self):
        self.hbdict = middle_args.HEART_BEAT_DICT

    def parse_heartbeat(self):
        return self.hbdict

    def update_progress(self):
        task = database_management.MissionInfo()
        task.query_database('SERVERCONTEXT', self.hbdict['serverContext'])
        
        data = {
            "progressText": "训练轮数(" + str(epoch) + "/" + str(total_epoch) + ")",
            "progress": dict['progress']*100,
            "platformContext": task.dict['PLATFORMCONTEXT']
        }

        res = requests.post(url=urls.url_to_platform_progress,headers=urls.headers,data=data)

    def update_database(self):
        task = database_management.MissionInfo()
        task.update_database('MISSIONSTATUS', self.hbdict['mission_status'], 'SERVERCONTEXT', self.hbdict['serverContext'])
        #多次更新或者函数中更新所有值


class MissionStop:

    def get_mission_info(self,server_context):
        tasker = database_management.MissionInfo()
        tasker.query_database(SERVERCONTEXT, server_context)
        return tasker.dict
        

    def mission_stop_AI_training(self,task_dict):
        kill_pid = task_dict['PID']
        #调接口

    def mission_stop_AI_marking(self,task_dict):
        container_name = task_dict['CONTAINERNAME']
        #调接口
