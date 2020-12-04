# -*- encoding: utf-8 -*-
"""
@file: echoClient.py
@time: 2020/11/30 下午2:18
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
import socket


class Client(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))

    def send(self, message):
        self.sock.sendall(message.encode())

    def receive(self):
        data = self.sock.recv(1024)
        return data.decode('utf-8')

    def close(self):
        self.sock.close()


def my_client(address, port):
    client = Client(address, port)
    while True:
        message = input("Input >")

        if message == 'exit':
            client.send(message)
            break

        client.send(message)
        info = client.receive()
        print(info)

    client.close()


if __name__ == '__main__':
    my_client("127.0.0.1", 8888)
