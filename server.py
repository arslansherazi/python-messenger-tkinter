import socket
import sys
from thread import *
import time

global clients


def threaded_function(client):
    name = client.recv(1024)
    names.append(name)
    clients.update({name: client})
    token = "name"
    for i in range(len(names) - 1):
        client.send(bytes(token, 'utf-8'))
        time.sleep(1)
        client.send(names[i])

    for i in range(len(names) - 1):
        clients[names[i]].send(bytes(token, 'utf-8'))
        time.sleep(1)
        clients[names[i]].send(name)

    start_new_thread(send, (client, name))


def send(client, name):
    while True:
        t = client.recv(1024)
        print(t)
        nam = client.recv(1024)
        print(nam)
        msg = client.recv(1024)
        print(msg)

        clients[nam].send(t)
        time.sleep(1)
        clients[nam].send(name)
        time.sleep(1)
        clients[nam].send(msg)
        time.sleep(1)


if __name__ == '__main__':
    clients = {}
    names = []
    num = 0

    HOST = ''
    PORT = 6470

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    s.listen(50)

    while True:
        c, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(threaded_function, (c,))

    s.close()
