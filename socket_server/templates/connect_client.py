import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
enter = '172.20.10.2'
port = 5050
client.connect((enter, port))

while True:
    client.send(input('msg: ').encode())
