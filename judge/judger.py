import sqlite3
from multiprocessing import Queue
import requests
import pika
# pika==0.13.0
import os
import json
import time
import logging
import logging.config

import database_management
import mission_management

from judge.aliyun_env import *
from concurrent.futures import ThreadPoolExecutor
import threading


# import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def Console(message):
    logger = logging.getLogger("infoLogger")

    logger.info("[{0}] {1}".format(Judgername, message))


def ErrorConsole(message):
    logger = logging.getLogger("errorLogger")

    logger.error("[{0}] {1}".format(Judgername, message))


def ConnectRabbitMQ(host, port, virtualHost, username, password, heartbeat):
    Console('connecting RabbitMQ(host={}, port={}, virtualHost={}, user={}, heartbeat={})'.format(
        host, port, virtualHost, username, heartbeat))
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.9.82',
        port=5672,
        virtual_host=virtualHost,
        credentials=pika.PlainCredentials(
            username='yijiahe',
            password='yjh@123'
        ),
        heartbeat=heartbeat
    ))
    Console('RabbitMQ connected.')
    return connection


def GetRabbitMQChannel(connection, queue_name, consumer):
    Console('creating RabbitMQ.Channel(queue={})'.format(queue_name))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True,
                          arguments={"x-max-priority": 10})
    channel.basic_qos(prefetch_count=30)
    channel.basic_consume(queue=queue_name, consumer_callback=consumer, no_ack=False)
    Console('channel created.')

    return channel


def TaskEnded(method):
    global rabbitMQChannel
    global rabbitMQConnection
    # Console('telling server the task is processed...')
    while True:
        try:
            if rabbitMQConnection.is_closed or rabbitMQChannel.is_closed:
                raise Exception('closed connection')
            rabbitMQChannel.basic_ack(delivery_tag=method.delivery_tag)
            Console('told.')
            break
        except:
            # traceback.print_exc()
            ErrorConsole(
                'failed to execute channel.basic_ack, trying to recreate channel...')
            while True:
                try:
                    rabbitMQChannel = GetRabbitMQChannel(
                        rabbitMQConnection, MQQueueName, Consumer)
                    break
                except:
                    # traceback.print_exc()
                    ErrorConsole(
                        'failed to recreate channel, trying to reconnect server...')
                    while True:
                        try:
                            rabbitMQConnection = MQConnector()
                            break
                        except:
                            # traceback.print_exc()
                            ErrorConsole(
                                'failed to reconnect server, waiting to reconnect again in 5 second(s)...')
                            time.sleep(5)


def main_process(m, channel, method):
    m_start = mission_management.MissionStart(m)
    m_stop = mission_management.MissionStop(m)
    # 应该是我去请求服务器接口判断资源情况

    if m_start.mission_type == 'AiModelTraining':
        channel.basic_ack(delivery_tag=method.delivery_tag)
        m_start.resources_query()
        m_start.mission_reply('172.18.60.77', 60090, m_start.platform_context, m_start.taskid)
        m_start.creating_mission_item()
        m_start.mission_start_AI_training()
        m_start.creating_mission_item()

    if m_start.mission_type == 'AiInteractiveMarking':
        channel.basic_ack(delivery_tag=method.delivery_tag)
        m_start.resources_query()
        conname = m_start.mission_start_AI_marking()
        print('coname+++++++'+conname)
        co_port = conname[-5:]
        tasker = database_management.MissionInfo()
        print(co_port)
        m_start.mission_reply('139.196.192.142', co_port, m_start.platform_context, m_start.taskid)
        m_start.creating_mission_item()
        tasker.update_database('CONTAINERNAME', conname, 'SERVERCONTEXT', m_start.server_context)
        tasker.update_database('MISSIONSTATUS', 'running', 'SERVERCONTEXT', m_start.server_context)


    if m_start.mission_type == 'StopMission':
        channel.basic_ack(delivery_tag=method.delivery_tag)

        if m_start.aiTaskType == 'AiModelTraining':
            m_stop.mission_stop_AI_training()

        if m_start.aiTaskType == 'AiInteractiveMarking':
            m_stop.mission_stop_AI_marking()


def Consumer(channel, method, properites, body):
    message = eval(body)
    pool = ThreadPoolExecutor(max_workers=2)
    future1 = pool.submit(main_process, (message, channel, method))
    main_process(message, channel, method)

    # mission = mission_management.MissionStart(m)

    # missionType = message['missionType']
    # platformContext = message['platformContext']
    # # serverContext = m['serverContext']
    # # indexstr1 = '"TaskId":'
    # # indexstr2 = ',"AiTask'
    # # taskid = platformContext[platformContext.index(indexstr1):platformContext.index(indexstr2)]
    #
    # taskid = platformContext.split(",")[0].split(":")[-1]
    # aiTaskType = platformContext.split(",")[1].split(":")[-1][1:-2]
    # # print(serverContext)
    # print(platformContext)
    # print('任务参数')
    # print(message)
    # print('任务类型')
    # print(message['missionType'])

    # 写入数据库
    #
    # if missionType == 'AiModelTraining':
    #     channel.basic_ack(delivery_tag=method.delivery_tag)
    #     # print("test")
    #
    #     Mission_Judgment.mission_judgment(platformContext=platformContext, host_ip='172.18.60.77', port=60090,
    #                                       serverContext=taskid)
    #     conn = sqlite3.connect('mission.db')
    #     c = conn.cursor()
    #     # init
    #
    #     # add
    #     c.execute(
    #         "insert into training_list(ID,TASKID,MISSIONTYPE,PLATFORMCONTEXT,SERVERCONTEXT,PID,PROGRESS) values (NULL,?,?,?,?,NULL,0)",
    #         (taskid, missionType, platformContext, taskid))
    #     c.close()
    #     conn.commit()
    #     print("sql done")
    #     # url = "http://192.168.9.99:6080/mmdetection/mmdet_model_train?"
    #
    #     # datas = []
    #     # message_dict = json.loads(body)
    #     # for k, v in message_dict.items():
    #     #     if k == 'missionType':
    #     #         continue
    #     #     else:
    #     #         if type(v) == str:
    #     #             v_new = v.replace('/', '%2F')
    #     #             datas.append(f'{k}={v_new}')
    #     # para = '&'.join(datas)
    #     # # print(para)
    #     # params = m
    #     # url += para
    #     # print(url)
    #     # res = requests.get(url=url, params=params)
    #     # print('获取进度')
    #     # # print(res.text)
    #     # # server_pid = res.json()['process_id']
    #     # # print(server_pid)
    #     #
    #     # 获取进度
    #     # 需要判断任务启动成功
    #
    #     # time.sleep(20)
    #     # while True:
    #     #     res = requests.get(url='http://139.196.192.142/progress/get_progress')
    #     #     # if res.status_code == 200:
    #     #     #     break
    #     #     print(res)
    #     #     # server_pid = res.json()[3]
    #     #     # if res.json()[1]==None:
    #     #     mission_progress = res.json()[0]
    #     #     total_epoch = max(res.json()[1], res.json()[2])
    #     #     epoch = min(res.json()[1], res.json()[2])
    #     #
    #     #     # 回报进度
    #     #     report_progress(platformContext, epoch, total_epoch, mission_progress)
    #     #     time.sleep(5)
    #     #     if mission_progress == 1:
    #     #         break
    # if missionType == 'AiInteractiveMarking':
    #     # print(11111)
    #
    #     channel.basic_ack(delivery_tag=method.delivery_tag)
    #     # time.sleep(20)
    #     # conname = runshell.start_container()
    #     conname1 = requests.get(url='http://139.196.192.142:8011/startcontainer')
    #     print(22)
    #     global conname
    #     conname = conname1.json()
    #     # print(type(conname))
    #     # print(conname)
    #     # print(conname1)
    #     # 需要判断 容器能否创建成功
    #     # time.sleep(20)
    #     conport = conname[-5:]
    #     conn = sqlite3.connect('mission.db')
    #     c = conn.cursor()
    #     # init
    #
    #     # add
    #     c.execute(
    #         "insert into marking_list(ID,TASKID,MISSIONTYPE,PLATFORMCONTEXT,SERVERCONTEXT,CONTAINERNAME) values (NULL,?,?,?,?,?)",
    #         (taskid, missionType, platformContext, taskid, conname))
    #     c.close()
    #     conn.commit()
    #     print("sql done")
    #     Mission_Judgment.mission_judgment(platformContext=platformContext, host_ip='139.196.192.142', port=conport,
    #                                       serverContext=taskid)
    #     print(conname)
    #
    #     time.sleep(20)
    #     # while True:
    #     #     res = requests.get(url='http://139.196.192.142/get_interaction_service')
    #     #     if res is not None:
    #     #         print(res)
    #     #         break
    # if missionType == 'AiImageMatting':
    #     channel.basic_ack(delivery_tag=method.delivery_tag)
    # if missionType == 'StopMission':
    #     print("Stop")
    #     # 上下文判断任务类型
    #     channel.basic_ack(delivery_tag=method.delivery_tag)
    #     print(aiTaskType)
    #     if aiTaskType == 'AiModelTraining':
    #         conn = sqlite3.connect('mission.db')
    #         c = conn.cursor()
    #         c.execute("SELECT PID FROM training_list WHERE TASKID=?", (message['serverContext'],))
    #         # print(c.fetchone())
    #         # print(type(c.fetchone()))
    #         # print(type(c.fetchall()))
    #         pid_temp = str(c.fetchone())
    #         print(pid_temp)
    #         pid = pid_temp[1:-2]
    #         print(pid)
    #         kill_pid(pid)
    #         c.execute("UPDATE training_list SET PROGRESS =? WHERE TASKID=?", (0, message['serverContext'],))
    #         conn.commit()
    #
    #     if aiTaskType == 'AiInteractiveMarking':
    #         conn = sqlite3.connect('mission.db')
    #         c = conn.cursor()
    #         c.execute("SELECT CONTAINERNAME FROM marking_list WHERE TASKID=?", (message['serverContext'],))
    #         stop_conname = str(c.fetchone())[1:-3]
    #         print(stop_conname)
    #         # stopconport = m["port"]
    #         requests.post(url='http://139.196.192.142:8011/stopcontainer',
    #                       headers={"Content-Type": "application/json"},
    #                       data=json.dumps({"container_name": stop_conname}))
    #         c.execute("UPDATE marking_list SET CONTAINERNAME ='stopped' WHERE TASKID=?", (message['serverContext'],))
    #         conn.commit()
    #         print(message['serverContext'])
    #         print('stopped')


def ErrorConsumer(channel, method, properites, body):
    TaskEnded(method)
    channel.stop_consuming()


def MQConnector():
    return ConnectRabbitMQ(host=MQHost, port=MQPort, virtualHost=VirtualHost, username=MQUsername, password=MQPassword,
                           heartbeat=MQHeartBeat)


def run_judger():
    global rabbitMQChannel
    global rabbitMQConnection
    while True:

        failed_last_time = False
        try:

            rabbitMQConnection = MQConnector()

            if not failed_last_time:

                rabbitMQChannel = GetRabbitMQChannel(
                    rabbitMQConnection, MQQueueName, Consumer)

                print("GetChannel Successful")

                rabbitMQChannel.start_consuming()

            else:
                rabbitMQChannel = GetRabbitMQChannel(
                    rabbitMQConnection, MQQueueName, ErrorConsumer)
                rabbitMQChannel.start_consuming()
                rabbitMQChannel = GetRabbitMQChannel(
                    rabbitMQConnection, MQQueueName, Consumer)
                rabbitMQChannel.start_consuming()
                failed_last_time = False


        except Exception as e:
            failed_last_time = True
            ErrorConsole(
                'connection lost, waiting to reconnect in 5 second(s)...')
            print(e)
            time.sleep(5)


if __name__ == "__main__":
    # res = requests.get(url='http://172.18.60.173:8006/progress/get_progress')
    # # if res.status_code == 200:
    # #     break
    # print(res)
    # missionType = "aaa"
    # server_pid = res.json()[0]
    # # if res.json()[1]==None:
    # print(server_pid)
    # mission_progress = res.json()[1]
    # print(mission_progress)
    # epoch = res.json()[2]
    # print(epoch)
    # total_epoch = res.json()[3]
    # print(total_epoch)
    # # progress = res.text.lstrip('[').rstrip(']')
    # # print(progress)
    # create_list()
    #
    # init_list()
    # add_info(server_pid, missionType, epoch, total_epoch, mission_progress)
    # # report_progress(5, 8, progress)
    # # 回报进度
    # report_progress("platformContext", epoch, total_epoch, mission_progress)
    # time.sleep(5)
    run_judger()
