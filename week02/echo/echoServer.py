# -*- encoding: utf-8 -*-
"""
@file: echoServer.py
@time: 2020/11/30 下午2:18
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import socket


class Server(object):
    def __init__(self, address, port):
        self.port = port
        self.address = address

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen(1)

    def run(self):
        while True:
            conn, client_ip = self.sock.accept()
            print("client ip: {}".format(client_ip))
            while True:
                data = conn.recv(1024)
                if isinstance(data, bytes) and data == b'exit':
                    break
                if isinstance(data, bytes):
                    conn.sendall(data)
                elif isinstance(data, str):
                    conn.sendall(data.encode())

            conn.close()
            break

        self.sock.close()


def my_server(address, port):
    print("init server ... ")
    server = Server(address, port)
    server.run()


if __name__ == '__main__':
    my_server('0.0.0.0', 8888)
