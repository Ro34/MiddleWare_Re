import multiprocessing as mp

from middleware_management import platform_heartbeat


def fun1():
    p1_heartbeat = mp.Process(target=platform_heartbeat())
    p1_heartbeat.start()


def fun2():
    p2_API = mp.Process()