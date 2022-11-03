import shutil
import sys, argparse
import os
import settings
from settings import Status
import json
import subprocess
from time import sleep


result = {}
config = {}

def substring(str, length=200):
    if len(str) <= length:
        return str
    else:
        return str[:length - 3] + "..."

def compile():
    print("compiling...")
    command = settings.compile_cmd[config["language"]]
    execute = settings.exec_file.get(config["language"])
    if command == []:
        print("skipped compile")
    else:
        try:
            out_bytes = subprocess.check_output(["timeout", str(settings.compile_timeout)] + command, stderr=subprocess.STDOUT)
            print("compile success")
        except subprocess.TimeoutExpired:
            return False
        except subprocess.CalledProcessError as e:
            out_bytes = e.output
            result["result"] = Status.CompileError
            if e.returncode == 124:
                result["compileErrorInfo"] = "compile time out."
            else:
                result["compileErrorInfo"] = substring(str(out_bytes))
            return False
    os.system("chown judger:judger " + execute)
    shutil.move(execute, "/home/judger/run_env")
    return True

def run_case(id, input_file, input_file_mode, output_file, output_file_mode, stdout_file):
    print(" ".join(["running test:", input_file, stdout_file]))
    output_file = output_file if output_file_mode else "user_output.txt" 
    case_result = {"id": id}

    time_limit = config["limitTime"] / 1000
    memory_limit = config["limitMemory"]

    
    command = ["/usr/bin/time", "-f", "%e %M", "-o", "time.txt", "timeout", str(time_limit + 0.1), "sudo", "-u", "judger"] + settings.run_cmd[config["language"]]
    try:
        input_opened = None if input_file_mode else open(input_file, 'r')
        output_opened = None if output_file_mode else open(output_file, 'w')
        subprocess.check_call(command, stdin=input_opened, stdout=output_opened, timeout=time_limit)
    except subprocess.TimeoutExpired:
        case_result["status"] = Status.TimeLimitExceeded
        sleep(0.1)
        return case_result
    except subprocess.CalledProcessError:
        case_result["status"] = Status.RuntimeError
        return case_result
    try:
        with open("time.txt") as ftime:
            time, memory = map(float, ftime.readline().split())
            time = int(time * 1000)
            memory = int(memory)
    except:
        case_result["status"] = Status.RuntimeError
        return case_result
            
    case_result["timeUsage"] = time
    case_result["memoryUsage"] = memory
    if (memory > memory_limit):
        case_result["status"] = Status.MemoryLimitExceeded
        return case_result
    
    try:
        judger = config.get("judge", "BaseChecker")
        module = __import__(judger)
        checker = getattr(module, judger)
        case_result["status"], message = checker().check(input_file, output_file, stdout_file)
        if message != "":
            case_result["message"] = substring(message)
    except:
        case_result["status"] = Status.JudgementError
    finally:
        return case_result

def run():
    result["result"] = Status.Accept
    result["cases"] = []
    os.system("chown judger:judger /root/judge_file")
    input_file_mode = "inputFileName" in config
    output_file_mode = "outputFileName" in config
    input_file_name = config.get("inputFileName", None)
    output_file_name = config.get("outputFileName", None)
    
    for (id, datafile) in config["data"].items():
        input_file, stdout_file = datafile
        if input_file_mode:
            shutil.copy(input_file, input_file_name)
            os.system("chown judger:judger " + input_file_name)
            input_file = input_file_name
        if output_file_mode:
            open(output_file_name, 'w')
            os.system("chown judger:judger " + output_file_name)
        case_result = run_case(id, input_file, input_file_mode, output_file_name, output_file_mode, stdout_file)
        if input_file_mode:
            os.remove(input_file)
        if output_file_mode:
            os.remove(output_file_name)
        result["cases"].append(case_result)
        result["result"] = max(result["result"], case_result["status"])


# if __name__ == '__main__':
global args
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", default=".")
parser.add_argument("-c", "--config", default="config.json")
parser.add_argument("-r", "--result", default="result.json")
args = parser.parse_args()
os.chdir(args.dir)
config = json.load(open(args.config, "r"))
if compile():
    run()
json.dump(result, open(args.result, "w"))

