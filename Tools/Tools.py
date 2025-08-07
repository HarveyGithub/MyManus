
import os
import subprocess
from Tools.File_Operation import *

def Run_Command(Command):
    """跨平台命令执行函数"""
    # print(Command)
    result = subprocess.run(
        'cd ./WorkSpace/ && ' + Command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
        env=os.environ.copy()
    )
    if result.stdout or result.stderr:
        if result.stdout and result.stderr:
            return f"Stdout:{result.stdout} Stderr:{result.stderr}"
        elif result.stdout:
            return f"Stdout:{result.stdout}"
        else:
            return f"Stderr:{result.stderr}"
    return "Ran command successfully"