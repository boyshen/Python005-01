# -*- encoding: utf-8 -*-
"""
@file: producer.py
@time: 2020/12/20 下午5:27
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import pika


def main():
    # 初始化连接参数。
    credential = pika.PlainCredentials(username='test', password='test')
    parameters = pika.ConnectionParameters(host='192.168.0.197',
                                           port=5672,
                                           virtual_host='/',
                                           credentials=credential)

    # 建立连接
    # 使用阻塞方法
    connection = pika.BlockingConnection(parameters=parameters)

    # 建立信道
    channel = connection.channel()

    # 声明交换机。 使用 fanout 模式
    # exchange 为对应交换机名称
    # fanout 为一对多模式
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # 发送消息到交换机
    channel.basic_publish(exchange='logs', routing_key='', body='send message to fanout')

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    main()
