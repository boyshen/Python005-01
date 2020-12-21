# -*- encoding: utf-8 -*-
"""
@file: redis_count.py
@time: 2020/12/20 下午10:30
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  Python+redis 实现高并发的计数器功能
"""

import redis
import random

HOST = '192.168.10.43'
PORT = 6379
PASSWORD = 'P@ssw0rd'


class RedisCount(object):

    def __init__(self, host, port, password):
        self._host = host
        self._port = port
        self._password = password
        self.video = 'video'

        self.client = redis.Redis(host=self._host, port=self._port, password=self._password)

    def add_video(self, video_id):
        """
        添加视频信息到 redis
        :param video_id: (int or str)
        :return: (bool)
        """
        result = False
        if self.client.hexists(self.video, video_id):
            print("video: {} Already Exists".format(video_id))
            return result

        # 类型转换
        if isinstance(video_id, int):
            video_id = str(video_id)

        try:
            self.client.hset(self.video, video_id, '0')
        except Exception as e:
            raise e
        else:
            result = True
        finally:
            return result

    def counter(self, video_id):
        """
        视频计数
        :param video_id: (str)
        :return: (int)
        """
        value = 0
        if isinstance(video_id, int):
            video_id = str(video_id)

        try:
            if self.client.hexists(self.video, video_id):
                self.client.hincrby(self.video, video_id, amount=1)
                value = int(self.client.hget(self.video, video_id))
        except Exception as e:
            raise e
        finally:
            return value

    def close(self):
        self.client.close()


def main():
    videos = ['1001', '1002']
    redis_count = RedisCount(HOST, PORT, PASSWORD)

    try:
        for video in videos:
            redis_count.add_video(video)

        for i in range(10):
            index = random.randrange(0, len(videos))
            video = videos[index]
            result = redis_count.counter(video)
            print("video:{}, count:{}".format(video, result))

    except Exception as e:
        raise e
    finally:
        redis_count.close()


if __name__ == '__main__':
    main()
