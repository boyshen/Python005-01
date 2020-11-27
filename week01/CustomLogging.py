# -*- encoding: utf-8 -*-
"""
@file: CustomLogging.py
@time: 2020/11/25 下午5:30
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
import os
import time
import random
import logging
import logging.config

# 日志保存目录
LOGGING_PATH = "./log/"

# 日志分割时间，每隔多久一次， 如 'M' 则是每隔1分钟执行一次分割。
# 'M' ==> 分钟
# 'H' ==> 小时
# 'D' ==> 天
# 'W0'-'W6'  ==> '0' 表示周一、
# 参考 logging 文档
LOGGING_SPLIT_TIME = 'M'

# 保存分割日志的数量的。如果超过指定数量将删除最早的版本。
LOGGING_BACKUP_COUNT = 2


class CustomLogging(object):

    def __init__(self):
        self._config = {
            "version": 1,
            "formatters": {
                "detailed": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s %(name)s %(levelname)s %(client)s %(ip)s %(module)s %(func)s "
                              "%(processName)s %(lineno)s %(message)s ",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG"
                },
                "acc_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": "acc.log",
                    "when": "M",
                    "backupCount": 3,
                    "level": "DEBUG",
                    "formatter": "detailed"
                }
            },
            "loggers": {
                "acc": {
                    "level": "INFO",
                    "handlers": ["acc_file", "console"]
                }
            }
        }

        if not os.path.exists(LOGGING_PATH):
            os.makedirs(LOGGING_PATH)

        self._update()
        logging.config.dictConfig(self._config)
        self.acc = logging.getLogger("acc")

    def _update(self):
        filename = self._config['handlers']['acc_file']['filename']
        self._config['handlers']['acc_file']['filename'] = os.path.join(LOGGING_PATH, filename)

        self._config['handlers']['acc_file']['when'] = LOGGING_SPLIT_TIME
        self._config['handlers']['acc_file']['backupCount'] = LOGGING_BACKUP_COUNT


class AccessLogging(CustomLogging):
    def __init__(self, func):
        super(AccessLogging, self).__init__()
        self.func = func

    def __call__(self, *args, **kwargs):
        result, device, ip = self.func(*args, **kwargs)
        self.acc.info("Logging Console Message:{}".format(result),
                      extra={"client": device, "ip": ip, "func": self.func.__name__})
        return result


@AccessLogging
def example(output, device, ip):
    print("This example output: {}".format(output))
    return output, device, ip


@AccessLogging
def example1(output, device, ip):
    print("This example1 output: {}".format(output))
    return output, device, ip


def main(minutes):
    status = ["200", "404", "502", "400"]
    device = ["PC", "Android", "ios", "Web"]
    ip = ["192.168.1.12", "192.168.1.25", "192.168.1.100", "10.10.1.134"]
    for i in range(minutes):
        for j in range(60):
            index = random.randrange(0, 4)
            example(status[index], device[index], ip[index])
            example1(status[index], device[index], ip[index])
            time.sleep(1)
            print("Run time remaining: {}:{}".format(minutes - i - 1, 60 - j - 1))


if __name__ == '__main__':
    # 程序运行时间(分钟)
    main(3)
