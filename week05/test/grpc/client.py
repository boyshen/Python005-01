# -*- encoding: utf-8 -*-
"""
@file: client.py
@time: 2020/12/20 下午8:13
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import grpc
import queue
from week05.test.grpc import schema_pb2
from week05.test.grpc import schema_pb2_grpc

q = queue.Queue()


def generate_message():
    while True:
        num = q.get()
        print(num)
        yield schema_pb2.Request(num=num)


def main():
    # 获取通信
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = schema_pb2_grpc.GatewayStub(channel)
        q.put(1)
        # 调用循环发送消息并接收消息
        resp = stub.Call(generate_message())
        for r in resp:
            num = r.num
            q.put(num)


if __name__ == '__main__':
    main()
