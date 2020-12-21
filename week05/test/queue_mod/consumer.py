# -*- encoding: utf-8 -*-
"""
@file: consumer.py
@time: 2020/12/20 下午1:03
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  消费者
"""

import pika

QUEUE = 'test_queue_demo'


# 定义一个回调函数来处理队列消息
def callback(ch, method, properties, body):
    # 手动发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # 输出消息
    print(body.decode())


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

    # 声明消息队列
    # 建议消费者和生产者都进行声明
    # durable = False 是否队列进行持久化
    channel.queue_declare(queue=QUEUE, durable=False)

    # 定义从队列中获取消息，并使用回调函数处理
    channel.basic_consume(QUEUE, on_message_callback=callback)

    # 开始就接收消息，并进入阻塞状态
    channel.start_consuming()


if __name__ == '__main__':
    main()
