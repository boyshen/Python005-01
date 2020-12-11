# -*- encoding: utf-8 -*-
"""
@file: insert.py
@time: 2020/12/9 下午2:23
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  使用 pymysql 插入数据。
"""
import random
import pymysql
import datetime
from configparser import ConfigParser

CONFIG = './conf.ini'


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def read_config(config, section):
    parser = ConfigParser()
    parser.read(config)

    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise "Exception: {} File Not Found section:{}".format(config, section)
    return dict(items)


class User(object):
    WOMAN = 'woman'
    MAN = 'man'

    def __init__(self, host, port, user, password, database):
        self.table = 'user'
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.charset = 'utf8mb4'

        self.__init_connection__()

    def __init_connection__(self):
        self.connection = pymysql.connect(host=self.__host,
                                          port=self.__port,
                                          user=self.__user,
                                          password=self.__password,
                                          db=self.__database,
                                          charset=self.charset,
                                          cursorclass=pymysql.cursors.DictCursor)

    def insert(self, name, age, birthday, gender, education):
        create_time = get_time()
        update_time = get_time()
        try:
            with self.connection.cursor() as cursor:
                # sql = "INSERT INTO `user` " \
                #       "(`name`, `age`, `birthday`, `gender`, `education`, `create_time`, `update_time`) " \
                #       "VALUES (%s, %s, %s, %s, %s, %s, %s)"

                sql = "INSERT INTO `user` " \
                      "(`name`, `age`, `birthday`, `gender`, `education`, `create_time`, `update_time`) " \
                      "VALUES (%(name)s, %(age)s, %(birthday)s, %(gender)s, %(education)s, %(create_time)s, " \
                      "%(update_time)s)"

                args = {'name': name, 'age': age, 'birthday': birthday, 'gender': gender, 'education': education,
                        'create_time': create_time, 'update_time': update_time}
                cursor.execute(sql, args)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e

    def close(self):
        self.connection.close()


def t_insert(num):
    test_name = ('张三', '李四', '王五', '赵六')
    test_age = (27, 28, 29, 30)
    test_gender = (User.WOMAN, User.MAN)
    test_birthday = ("1993-02-23", "1992-01-28", "1991-10-21", "1990-08-04")
    test_education = ('本科', '专科', '博士', '研究生')

    config = read_config(CONFIG, 'mysql')
    print(config)
    user = User(user=config['user'], password=config['password'], host=config['host'], port=int(config['port']),
                database=config['database'])
    try:
        for i in range(num):
            index = random.randint(0, len(test_name) - 1)
            gender_index = random.randint(0, len(test_gender) - 1)
            user.insert(name=test_name[index],
                        age=test_age[index],
                        birthday=test_birthday[index],
                        gender=test_gender[gender_index],
                        education=test_education[index])
    except Exception as e:
        raise e
    finally:
        user.close()


if __name__ == '__main__':
    t_insert(3)
