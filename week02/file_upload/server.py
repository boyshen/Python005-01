# -*- encoding: utf-8 -*-
"""
@file: server.py
@time: 2020/12/3 上午11:09
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import socket
import json
import os
import hashlib

BUFF_SIZE = 1024

ADDRESS = "0.0.0.0"
PORT = 8888
SAVE_PATH = './upload_save'
CONNECTION_NUMBERS = 10


class SendMessage(object):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    def __init__(self, status="", msg=""):
        self.status = status
        self.msg = msg

    def __str__(self):
        return json.dumps({'status': self.status, 'msg': self.msg})


class ReceiverFileMessage(object):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    def __init__(self, message):
        self.status = message['status']
        self.name = message['name']
        self.size = message['size']
        self.md5 = message['md5']
        self.msg = message['msg']

    def __str__(self):
        return json.dumps({'status': self.status, 'name': self.name, 'size': self.size, 'md5': self.md5,
                           'msg': self.msg})


class File(object):
    """
    文件信息对象。
    """

    def __init__(self, file):
        """
        :param file:(str)
        """
        self.file = file

    @property
    def path(self):
        return os.path.dirname(self.file)

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def md5(self):
        try:
            with open(self.file, 'rb') as rf:
                hash_md5 = hashlib.md5()
                hash_md5.update(rf.read())
                md5_value = hash_md5.hexdigest()
            return md5_value
        except FileNotFoundError as e:
            print(e)
            print("File Not Found. File:{}".format(self.file))
        except Exception as e:
            print(e)
            print("Error: Get File md5 value {}".format(self.file))

    @property
    def size(self):
        try:
            size = os.path.getsize(self.file)
            return size
        except FileNotFoundError as e:
            print(e)
            print("File Not Found. File:{}".format(self.file))
        except Exception as e:
            print(e)
            print("Error: Get File Size. File:{}".format(self.file))


class Server(object):
    """
    服务端
    """

    def __init__(self, address, port, save_path=None, connection_num=10):
        self.address = address
        self.port = port
        self.save_path = save_path if save_path is not None else './upload_save'
        self.connection_num = connection_num

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.connection_num)

        self.__init_save_path__()
        print("Service startup! Listen：{}:{}".format(self.address, self.port))

    def __init_save_path__(self):
        if not os.path.isdir(self.save_path):
            os.makedirs(self.save_path)

    def upload_file_interface(self):
        while True:
            conn, client_address = self.sock.accept()

            # 接收文件信息
            receiver = conn.recv(BUFF_SIZE)
            file_info = ReceiverFileMessage(json.loads(receiver.decode("utf-8")))
            conn.sendall(str(SendMessage(status=SendMessage.STATUS_OK)).encode())
            print("Receiver from {} data: {}".format(client_address, file_info))

            # 接收文件内容
            file = os.path.join(self.save_path, file_info.name)
            with open(file, 'wb') as wf:
                size = 0
                while True:
                    data = conn.recv(BUFF_SIZE)
                    size += len(data)
                    if size == file_info.size:
                        wf.write(data)
                        break
                    wf.write(data)
            print("Success write file: {}".format(file))

            # 验证文件 md5 值并返回信息。
            _file = File(file)
            if _file.md5 == file_info.md5:
                msg = SendMessage(status=SendMessage.STATUS_OK)
            else:
                msg = SendMessage(status=SendMessage.STATUS_FAILED)

            conn.sendall(str(msg).encode())
            conn.close()

    def close(self):
        self.sock.close()


def main():
    server = Server(ADDRESS, PORT, SAVE_PATH, CONNECTION_NUMBERS)
    try:
        server.upload_file_interface()
    except KeyboardInterrupt as e:
        print(e)
    finally:
        server.close()


if __name__ == '__main__':
    main()
