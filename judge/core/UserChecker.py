import settings
from BaseChecker import BaseChecker

class UserChecker(BaseChecker):
    def __init__(self):
        pass

    def judge(self, input, output, stdout):
        return settings.Status.Accept, ""
        """
        input:  A opened file of input
        output: A opened file of output
        stdout: A opened file of answer
        ***
        ATENTION: input, output and stdout are opened file rather than filename, 
                    which means that you can use file method such as "input.readline()".
        ***
        return: status, message
        status: see settings.Status
        message: report message. For example, the differences bewteen output and answer

        There is an example:

        for line, stdline in enumerate(stdout.readlines()):
            outline = output.readline()
            if outline.strip() != stdline.strip(): 
                message = "line" + str(line) + ":\n"
                message += "answer_out: " + stdline + "\n"
                message += "your_out: " + outline + "\n"
                return settings.Status.WrongAnswer, message
        return settings.Status.Accept, ""

        """
