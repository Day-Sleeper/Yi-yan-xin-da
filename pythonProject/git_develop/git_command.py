import subprocess
"""目前遗留问题，输出信息乱码，格式不规范"""
# 定义要执行的git命令，例如查看当前的git状态
command_status = ["git", "status"]
# 将所有.py为后缀的文件提交至缓存区
command_add_py = ["git", "add", "*.py"]
# 将当前目录下所有的文件提交至缓存区
command_add_all = ["git", "add", "."]
# 将所有修改过的文件进行提交，并上传提交信息
command_commit = ["git", "commit", "--m"]
# 将远程仓库的文件同步至本地
command_pull = ["git", "pull"]
# 将本地仓库的信息同步至远程仓库
command_push = ["git", "push"]
# 创建用户名称
command_name = ["git","config","--global","user.name"]
# 创建用户邮箱
command_email = ["git","config","--global","user.email"]
# 列出当前用户信息
command_list = ['git','config','--global','--list']
# 默认保存当前用户信息，避免下次输入
command_store = ['git','config','--global','credential.helper', 'store']
#安全路径预留命令
command_safe = "在此处输入git的提示语句".split(sep=" ")
# 克隆远程仓库
command_clone = ["git", "clone", "https://github.com/WFCT-Share/HRIS-remote.git"]
# 运行命令并获取输出
def git_run_command(command):
    if command == ["git", "commit", "--m"]:
        command.append(input("提交信息（回车为无）: "))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Git Command Output:\n", process.communicate())



def ini_git(command_name, command_email, command_store, command_list, command_clone):
    command_name.append('"' + input("输入您的用户名（英文）：") + '"')
    command_email.append(input("输入您的邮箱（完整）："))
    process1 = subprocess.Popen(command_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process2 = subprocess.Popen(command_email, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Git Command Output:\n", process1.communicate().decode())
    print("Git Command Output:\n", process2.communicate().decode())
    git_run_command(command_store)
    git_run_command(command_list)
    git_run_command(command_clone)

