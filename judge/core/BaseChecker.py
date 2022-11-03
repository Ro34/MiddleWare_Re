import settings
import os

def replaceRN(str):
    return str.replace('\r\n','\n').rstrip()

def getCleanLines(lines):
    lines = list(map(replaceRN,lines))
    length = len(lines)
    for lineNumber, lineContent in enumerate(reversed(lines)):
        if not lineContent:
            lines.pop(length-lineNumber-1)
        if lineContent:
            break
    return lines

class BaseChecker(object):
    def __init__(self):
        pass

    def judge(self, input, output, stdout):
        outputLines = getCleanLines(output.readlines())
        stdoutLines = getCleanLines(stdout.readlines())
   
        for lineNumber, stdLine in enumerate(stdoutLines):

            if lineNumber >= len(outputLines):
                return settings.Status.WrongAnswer, "标准输出行数比你的行数多"

            outLine = outputLines[lineNumber]
            if stdLine != outLine:
                message = "行号" + str(lineNumber) + ":\n"
                message += "标准输出: " + stdLine + "\n"
                message += "你的输出: " + outLine + "\n"
                return settings.Status.WrongAnswer, message

        if len(stdoutLines) < len(outputLines):
            return settings.Status.WrongAnswer, "你的输出比标准输出的行数多"

        return settings.Status.Accept, ""

    def check(self, input, output, stdout):
        if not os.path.exists(stdout):
            return settings.Status.JudgementError, "缺少标准文件，遇到此错误请联系管理员"
        if not os.path.exists(output):
            return settings.Status.RuntimeError, "没有输出文件"
        if os.path.getsize(output) > 1024 * 1024 * 30:
            return settings.Status.RuntimeError, "输出文件过大"

        try:
            return self.judge(open(input, 'r', encoding='utf8'), 
                              open(output, 'r', encoding='utf8'), 
                              open(stdout, 'r', encoding='utf8'))
        except Exception as e:
            return settings.Status.WrongAnswer, str(e)
        
