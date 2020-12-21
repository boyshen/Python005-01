# -*- encoding: utf-8 -*-
"""
@file: producer.py
@time: 2020/12/20 下午12:47
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  生产者
"""
import pika

QUEUE = 'test_queue_demo'


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
    # durable = False 是否队列进行持久化。
    channel.queue_declare(queue=QUEUE, durable=False)

    # 指定交换机并发送消息
    # exchange 交换机。队列模式下，没有交换机。所以为 ''
    # routing_key 为声明的消息队列名称
    # body 为发送的消息内容
    channel.basic_publish(exchange='',
                          routing_key=QUEUE,
                          body='Produce send message',
                          properties=pika.BasicProperties(
                              delivery_mode=2  # 设置消息为持久化模式。1 为非持久化
                          ))

    # 关闭与 RabbitMQ 的连接
    connection.close()


if __name__ == '__main__':
    main()
