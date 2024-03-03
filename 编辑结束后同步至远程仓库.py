import subprocess

# 定义要执行的git命令，例如查看当前的git状态
command_status = ["git", "status"]
# 将所有.py为后缀的文件提交至缓存区
command_add_py = ["git", "add", "*.py"]
#将当前目录下所有的文件提交至缓存区
command_add_all = ["git", "add", "."]
# 将所有修改过的文件进行提交，并上传提交信息
command_commit = ["git", "commit", "--m"]
# 将远程仓库的文件同步至本地
command_pull = ["git", "pull"]
# 将本地仓库的信息同步至远程仓库
command_push = ["git", "push"]
# 运行命令并获取输出
def git_run_command(command):
    if command == ["git", "commit", "--m"]:
        command.append(input("提交信息（回车为无）: "))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()
    print("Git Command Output:\n", output)


git_run_command(command_add_all)
git_run_command(command_commit)
git_run_command(command_push)



