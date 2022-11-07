import multiprocessing as mp

from api import run_api
from judge.judger import run_judger
from middleware_management import platform_heartbeat


def fun1():
    platform_heartbeat.heartbeat()


def fun2():
    run_api()

def fun3():
    run_judger()


def run():
    # p1 = mp.Process(target=fun1)

    # p2 = mp.Process(target=fun2)

    p3 = mp.Process(target=fun3)

    # p1.start()
    # p2.start()
    p3.start()


if __name__ == "__main__":
    run()
