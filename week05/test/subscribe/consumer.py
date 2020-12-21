# -*- encoding: utf-8 -*-
"""
@file: consumer.py
@time: 2020/12/20 下午5:38
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import pika


# 定义一个回调函数来处理队列消息
def callback(ch, method, properties, body):
    # 输出消息
    print(body.decode())
    # 手动发送确认消息
    # ch.basic_ack(delivery_tag=method.delivery_tag)


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

    # 声明队列
    # exclusive = True 仅允许访问当前的队列。当消费者关闭时，队列也消失。则不再往里写消息
    # queue ='' 即可以自动创建队列
    que = channel.queue_declare(queue='', exclusive=True)

    # 绑定队列到交换机，实现交换机发送消息到队列
    channel.queue_bind(exchange='logs', queue=que.method.queue)

    # 接收消息并进行处理
    # auto_ack = True 自动回复
    channel.basic_consume(queue=que.method.queue,
                          on_message_callback=callback,
                          auto_ack=True)

    # 开始接收消息，并进入阻塞状态
    channel.start_consuming()


if __name__ == '__main__':
    main()
