# -*- encoding: utf-8 -*-
"""
@file: client.py
@time: 2020/12/3 上午11:09
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:

在运行服务端之后。通过执行 python client.py file 进行上传。

example：
    python client.py ./test_file/text.txt
    上传 text.txt 文件。

example:
    python client.py text.txt --address 127.0.0.1 --port 9999
    --address   设置连接服务端的地址
    --port      设置连接服务端的端口

example:
    python client.py --help
    --help      查看帮助
"""
import os
import hashlib
import socket
import json
import argparse

BUFF_SIZE = 1024

ADDRESS = '127.0.0.1'
PORT = 8888


class SendFileMessage(object):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    def __init__(self, name, size, md5, status, msg=""):
        self.name = name
        self.size = size
        self.md5 = md5
        self.status = status
        self.msg = msg

    def __str__(self):
        return json.dumps({'name': self.name, 'size': self.size, 'md5': self.md5,
                           'status': self.status, 'msg': self.msg})


class ReceiverMessage(object):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    def __init__(self, message):
        self.status = message['status']
        self.msg = message['msg']

    def __str__(self):
        return json.dumps({'status': self.status, 'msg': self.msg})


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


class Client(object):
    """
    客户端
    """

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))

    def upload_file(self, file):
        """
        上传文件
        :param file: (str) 文件
        :return: (bool)
        """
        _file = File(file)
        if self.send_file_info(_file.name, _file.size, _file.md5):
            message = self.send_file(file, _file.size)
            if message.status == ReceiverMessage.STATUS_OK:
                print("Upload File:{} Success!".format(file))
                return True
        print("Upload File:{} Failed! ".format(file))
        return False

    def send_file_info(self, name, size, md5):
        """
        发送文件信息。
        :param name: (str) 文件名
        :param size: (int) 文件大小
        :param md5: (str) 文件 md5 值
        :return: (bool)
        """
        try:
            msg = SendFileMessage(name=name, size=size, md5=md5, status=SendFileMessage.STATUS_OK)
            self.sock.sendall(str(msg).encode())
            receive = self.sock.recv(BUFF_SIZE)
            receive_data = ReceiverMessage(json.loads(receive.decode('utf-8')))
            if receive_data.status == ReceiverMessage.STATUS_OK:
                # print("Receiver Server data: {}".format(receive_data))
                return True
            return False
        except (socket.herror, socket.gaierror, socket.timeout) as e:
            print(e)
            print("Network error")
        except Exception as e:
            print(e)

    def send_file(self, file, size):
        """
        发送文件内容
        :param file: (str) 文件名
        :param size: (int) 文件大小
        :return:
        """
        i = 1
        try:
            with open(file, 'rb') as rf:
                while True:
                    data = rf.read(BUFF_SIZE)
                    if not data or data == b'':
                        break
                    self.sock.sendall(data)
                    progress = 1.0 if (BUFF_SIZE * i) >= size else (BUFF_SIZE * i) / size
                    print("File Upload Progress: {:.1f} %".format(progress * 100), end='\r', flush=True)
                    i += 1
            print()
            receive = self.sock.recv(BUFF_SIZE)
            receive_data = ReceiverMessage(json.loads(receive.decode("utf-8")))
            return receive_data

        except Exception as e:
            print("Upload Failed. File: {}".format(file))
            print(e)

    def close(self):
        self.sock.close()


def input_args():
    """
    读取输入的参数信息。
    :return: (args) 对象
    """
    parser = argparse.ArgumentParser(description="1. Upload Files")
    parser.add_argument("file", metavar="File to be uploaded",
                        help="python client.py text.txt. text.txt file to be uploaded")
    parser.add_argument("--address", dest="address", action='store', type=str, default=ADDRESS,
                        help="Set server address")
    parser.add_argument("--port", dest="port", action='store', type=int, default=PORT,
                        help="Set server port")

    args = parser.parse_args()
    return args


def main():
    # 获取参数
    args = input_args()

    if not os.path.isfile(args.file):
        print("File not found! File:{}".format(args.file))
        return False

    client = Client(args.address, args.port)
    try:
        client.upload_file(args.file)
    except Exception as e:
        print(e)
    finally:
        client.close()


def test():
    file = "./test_file/timg.jpeg"
    client = Client("127.0.0.1", 9999)
    try:
        client.upload_file(file)
    except Exception as e:
        print(e)
    finally:
        client.close()


if __name__ == '__main__':
    main()
