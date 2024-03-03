import subprocess
import os
# 打开新的命令提示符并更改标题
subprocess.Popen(["start", "cmd", "/k"], shell=True)
os.system("echo Hello from a new terminal!")
