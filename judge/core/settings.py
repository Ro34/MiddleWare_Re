from enum import Enum


class Status(object):
    WrongAnswer = -1
    WA = -1
    Accept = 0
    AC = 0
    TimeLimitExceeded = 1
    TLE = 1
    MemoryLimitExceeded = 2
    MLE = 2
    RuntimeError = 3
    RE = 3
    CompileError = 4
    CE = 4
    JudgementError = 5


compile_cmd = {
    "Pascal": ["fpc", "code.pas", "-ocode"],
    "Pascal -O2": ["fpc", "code.pas", "-ocode", "-O2"],
    "C": ["gcc", "code.c", "-o", "code", "-lm", "-DONLINE_JUDGE"],
    "C -O2": ["gcc", "code.c", "-o", "code", "-O2", "-lm", "-DONLINE_JUDGE"],
    "C++": ["g++", "code.cpp", "-o", "code", "-DONLINE_JUDGE"],
    "C++ -O2": ["g++", "code.cpp", "-o", "code", "-O2", "-DONLINE_JUDGE"],
    "Java": ["javac", "Main.java", "-encoding", "UTF-8"],
    "Python 2.7": [],
    "Python 3.6": []
}

exec_file = {
    "Pascal": "code",
    "Pascal -O2": "code",
    "C": "code",
    "C -O2": "code",
    "C++": "code",
    "C++ -O2": "code",
    "Java": "Main.class",
    "Python 2.7": "code.py",
    "Python 3.6": "code.py"
}

run_cmd = {
    "Pascal": ["/home/judger/run_env/code"],
    "Pascal -O2": ["/home/judger/run_env/code"],
    "C": ["/home/judger/run_env/code"],
    "C -O2": ["/home/judger/run_env/code"],
    "C++": ["/home/judger/run_env/code"],
    "C++ -O2": ["/home/judger/run_env/code"],
    "Java": ["java", "-classpath", "/home/judger/run_env/", "Main"],
    "Python 2.7": ["python", "/home/judger/run_env/code.py"],
    "Python 3.6": ["python3", "/home/judger/run_env/code.py"]
}
judge_name = "JudgeCore"
compile_timeout = 10
