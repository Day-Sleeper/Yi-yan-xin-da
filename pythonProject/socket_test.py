import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP Socket
s.bind(('127.0.0.1', 12345))  # 绑定地址
s.listen()                   # 监听
conn, addr = s.accept()      # 接受连接
s.connect(('127.0.0.1', 12345))  # 连接服务器
# 客户端发送
s.sendall(b'Hello, server')

# 服务器接收
data = conn.recv(1024)
s.close()  # 关闭Socket
