import subprocess
import webbrowser


def launch_neo4j():
    execution_path = 'neo4j-community-5.17.0/bin'
    proc = subprocess.Popen(["neo4j", "console"], cwd=execution_path, shell=True)
    proc.wait()


url = "http://localhost:7474/"
launch_neo4j()
webbrowser.open(url)
