# -*- encoding: utf-8 -*-
"""
@file: service.py
@time: 2020/12/20 下午7:50
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import grpc
import time
# schema_pb2 和 schema_pb2_grpc 为使用 proto 文件生成的模块
from week05.test.grpc import schema_pb2
from week05.test.grpc import schema_pb2_grpc
from concurrent import futures


# 1. 要求继承 proto 生成的服务class
# 2. 实现 proto 中定义的函数
# 3. 请求和返回的格式结构体
class GatewayServer(schema_pb2_grpc.GatewayServicer):
    def Call(self, request_iterator, context):
        for req in request_iterator:
            yield schema_pb2.Response(num=req.num + 1)
            time.sleep(1)


def main():
    # 定义线程池连接数
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 将服务与线程池绑定
    schema_pb2_grpc.add_GatewayServicer_to_server(GatewayServer(), server)
    # 定义端口并启动服务
    server.add_insecure_port('[::]:50051')
    server.start()

    # 阻塞运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()


if __name__ == '__main__':
    main()
