# -*- encoding: utf-8 -*-
"""
@file: short_message.py
@time: 2020/12/21 上午10:59
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，基于 Python 和 redis 实现如下的短信发送接口：
"""

import redis
import random
import time

HOST = '192.168.10.43'
PORT = 6379
PASSWORD = 'P@ssw0rd'

# 限制发送次数
COUNT = 5
# 限制时间。单位分钟
TIME_LIMIT = 1


class RedisMessage(object):

    def __init__(self, host, port, password, count=5, time_limit=1):
        """
        :param host: (str) Redis host
        :param port: (int) Redis 端口
        :param password: (str) Redis 密码
        :param count: (int) 限制次数
        :param time_limit: (int) 限制时间，单位分钟
        """
        self._host = host
        self._port = port
        self._password = password
        self.count = count
        self.time_limit = time_limit

        self.message_count = 'message_count'
        self.message_time = 'message_time'

        self.client = redis.Redis(host=self._host, port=self._port, password=self._password)

    def send_sms(self, telephone_number, content, key=None):
        """
        发送消息
        :param telephone_number: (str)
        :param content: (str)
        :param key: (None)
        :return: (bool)
        """
        # 获取当前时间
        current_time = int(time.time())

        if self.client.hexists(self.message_count, telephone_number):
            msg_count = int(self.client.hget(self.message_count, telephone_number))
            msg_time = int(self.client.hget(self.message_time, telephone_number))

            # 获取时间间隔
            interval_time = current_time - msg_time

            # 在限制时间发送
            if interval_time <= self.time_limit * 60:
                # 检查发送的次数是否达到限制
                if msg_count < self.count:
                    self.client.hset(self.message_count, telephone_number, msg_count + 1)
                    flag = True
                else:
                    flag = False
            # 已经过了限制时间。可以重新发送
            else:
                # 更新重新发送的时间和次数
                self.client.hset(self.message_count, telephone_number, 1)
                self.client.hset(self.message_time, telephone_number, current_time)
                flag = True

        else:
            # 第一次发送
            self.client.hset(self.message_count, telephone_number, 1)
            self.client.hset(self.message_time, telephone_number, current_time)
            flag = True

        if flag:
            print("{} 发送成功！context: {}".format(telephone_number, content))
        else:
            print("{} 在 {} 分钟内发送次数超过 {} 次, 请等待 {} 分钟".format(telephone_number, self.time_limit, self.count,
                                                             self.time_limit))

        return flag

    def close(self):
        self.client.close()


def main():
    redis_message = RedisMessage(host=HOST, port=PORT, password=PASSWORD, count=COUNT, time_limit=TIME_LIMIT)
    telephone_numbers = ['12345654321', '12345654321', '88887777666', '12345654321', '88887777666']

    try:
        for i in range(TIME_LIMIT * 60 * 2):
            index = random.randrange(0, len(telephone_numbers))
            telephone_num = telephone_numbers[index]
            redis_message.send_sms(telephone_num, 'hello world')
            time.sleep(1)

            if (i + 1) % 60 == 0:
                print()
                print("{} minute later ...".format((i + 1) / 60))

    except Exception as e:
        raise e
    finally:
        redis_message.close()


if __name__ == '__main__':
    main()
