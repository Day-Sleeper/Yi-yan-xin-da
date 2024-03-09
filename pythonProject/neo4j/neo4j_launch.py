import subprocess

def launch_neo4j():
    command = ["neo4j", "console"]
    execution_path = 'neo4j-community-5.17.0/bin'
    proc = subprocess.Popen(["neo4j", "console"], cwd=execution_path, shell=True)
    proc.wait()
    # url = 'http://localhost:7474/'
    # subprocess.run(['start', url], shell=True)
    # proc.wait()
"""目标网址： http://localhost:7474/"""
launch_neo4j()