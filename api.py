from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

import middle_args


class train_mission_paras(BaseModel):
    server_pid: int
    serverContext: str


class marking_mission_paras(BaseModel):
    container_name: str


class interaction_para(BaseModel):
    service_status: str


class progress_params(BaseModel):
    server_pid: int
    epoch: int
    total_epoch: int
    progress: float
    serverContext: str


class mission_info_para(BaseModel):
    serverContext: str
    mission_status: list
    server_status: str
    status_code: int
    training_epoch: int = None
    training_total_epoch: int = None
    training_pid: int = None
    training_progress: int = None
    marking_container_name: str = None
    dataset_total: int = None
    dataset_done: int = None



class resources_ok_para(BaseModel):
    resources_situation: str
    status_code: int


app1 = FastAPI()


@app1.post("/mission_info")
async def get_mission_info(item: mission_info_para):
    print("------------------------------------------")
    middle_args.HEART_BEAT_DICT = item.dict()
    print(item)
    print(type(middle_args.HEART_BEAT_DICT))

    return {"new ok ==== " + str(item)}

@app1.post('/resources_info')
async def get_resources_info(item:resources_ok_para):
    print("------------------------------------------")
    middle_args.RESOURCES_DICT = item.dict()
    print(middle_args.RESOURCES_DICT)

    return {"resources_info_get"+str(item)}


# 其他
@app1.post("/progress/send_progress")
async def send_progress(item: progress_params):
    global mission_progress
    global epoch_
    global total_epoch_
    global server_pid
    global serverContext
    mission_progress = item.progress
    epoch_ = item.epoch
    total_epoch_ = item.total_epoch
    server_pid = item.server_pid
    serverContext_ = item.serverContext
    # print(item.progress)
    # print(item.serverContext)
    print(mission_progress)

    # conn = sqlite3.connect('mission.db')
    # c = conn.cursor()
    # c.execute("UPDATE training_list SET PROGRESS=? WHERE SERVERCONTEXT=?", (mission_progress, serverContext_,))
    # c.execute("UPDATE training_list SET PID=? WHERE SERVERCONTEXT=?", (server_pid, serverContext_,))
    # c.execute("SELECT PLATFORMCONTEXT FROM training_list WHERE SERVERCONTEXT=?", (serverContext_,))
    #
    # platformContext = str(c.fetchone())[2:-3]
    # c.close()
    # conn.commit()
    # report_progress(platformContext, epoch_, total_epoch_, mission_progress)

    return "ok"


# 获取模型任务进度
@app1.get('/progress/get_progress')
async def get_progress():
    global mission_progress
    global epoch_
    global total_epoch_
    global server_pid
    global serverContext_
    if epoch_ == total_epoch_:
        mission_progress = 1

    print("任务进度：" + str(mission_progress))
    print("epoch" + str(epoch_))
    print("total_epoch" + str(total_epoch_))
    print(serverContext_)
    return [server_pid, mission_progress, epoch_, total_epoch_, serverContext_]


# print(progress_params)

# 停止模型训练任务
# @app1.post("/mission/send_kill_mission")
# async def get_kill_pid(item: train_mission_paras):
#     global killing_pid
#     killing_pid = item.server_pid
#     # 杀死进程
#     stopMission.kill_pid(killing_pid)
#     return {"Prepare to stop mission"}


# 获取kill_pid
@app1.get('/mission/get_kill_mission')
async def root():
    global killing_pid
    print(killing_pid)
    return killing_pid


# @app1.post("/marking_mission/stop_mission")
# async def stop_marking_mission(item: marking_mission_paras):
#     global killing_conname
#     killing_conname = item.container_name
#     runshell.stop_container(killing_conname)
#     # stopMission.kill_pid(killing_pid)
#     return {"marking_mission_stopped"}


# @app.get('/marking_mission/get_stop_mission')
# async def get_stop_marking():
#     global killing_pid
#     print(killing_pid)
#     return (killing_pid)


@app1.get('/test')
async def apitest():
    return {"service OK"}


@app1.post("/marking_service_status")
async def marking_service_ok(item: interaction_para):
    global interaction_service_status
    interaction_service_status = item.service_status
    return {"ok"}


@app1.post("/mission_info")
async def get_mission_info(item: mission_info_para):
    print("------------------------------------------")

    print(item)

    return {"new ok ==== " + str(item)}


@app1.get("/get_marking_service")
async def get_marking():
    global interaction_service_status
    return interaction_service_status


def run_api():
    uvicorn.run(app='api:app1', host="0.0.0.0", port=8006, reload=True, debug=False)


if __name__ == "__main__":
    run_api()
