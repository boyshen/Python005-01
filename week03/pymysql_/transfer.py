# -*- encoding: utf-8 -*-
"""
@file: transfer.py
@time: 2020/12/9 下午3:41
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 模拟实现转账功能。
"""
import uuid
import pymysql
import datetime
import json
from configparser import ConfigParser

# 数据库配置文件
CONFIG = './conf.ini'


def get_time():
    """
    获取当前时间。精确到毫秒
    :return: (str)
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def read_config(config, section):
    """
    读取数据库配置信息
    :param config: (str)
    :param section:  (str)
    :return: (dict)
    """
    parser = ConfigParser()
    parser.read(config)

    if parser.has_section(section):
        items = parser.items(section)
    else:
        raise "Exception: {} File Not Found section:{}".format(config, section)
    return dict(items)


# 应用层。用户对象和注册层。
# 提供用户注册，注册成功之后返回 User 对象。
# 使用 User 对象可以进行转账，查询，充值等相关操作。
class Register(object):
    def __init__(self, user_table, assets_table, audit_table):
        self.__user_table = user_table
        self.__assets_table = assets_table
        self.__audit_table = audit_table

    def register(self, name):
        # 注册用户。
        msg = self.__user_table.add(name)
        if msg.status == Message.FAILED:
            print("User Registration Failed! ")
            return None

        # 注册成功。初始化用户资产表为 0.0
        uid = msg.user_info.uid
        name = msg.user_info.name
        msg = self.__assets_table.add(uid, 0)
        if msg.status == Message.FAILED:
            print("Failed to initialize user assets!")
            return None

        return User(uid=uid, name=name, user_table=self.__user_table, assets_table=self.__assets_table,
                    audit_table=self.__audit_table)


class User(object):
    """
    用户对象。 (应用层)
    """

    def __init__(self, uid, name, user_table, assets_table, audit_table):
        self.__uid = uid
        self.__name = name

        self.__user_table = user_table
        self.__assets_table = assets_table
        self.__audit_table = audit_table

    def transfer(self, collection_uid, money):
        """
        用户转账
        :param collection_uid: (str) 收账用户uid
        :param money: (int)
        :return: (bool)
        """
        # 获取当前用户资产
        assets = self.assets()

        # 检查当前余额
        if assets < money:
            print("余额不足！")
            return True

        # 更新转账和收账用户资产
        msg = self.__assets_table.update_transfer(self.__uid, collection_uid, money)
        if msg.status == Message.FAILED:
            print("转账失败，数据库异常!")
            return False

        # 记录日志
        msg = self.__audit_table.add(self.__uid, collection_uid, money)
        if msg.status == Message.FAILED:
            print("Failed to write log:{uid: {}, collection uid:{}, money:{}}".format(self.__uid,
                                                                                      collection_uid, money))

        print("转账成功!")
        return True

    def recharge(self, money):
        """
        充值
        :param money: (int)
        :return: (bool)
        """
        msg = self.__assets_table.update(self.__uid, money)
        if msg.status == Message.SUCCESS:
            print("充值成功! 当前余额: {}".format(self.assets()))
            return True

        print("充值失败! 当前余额: {}".format(self.assets()))
        return False

    def assets(self):
        """
        用户当前资产
        :return: (int)
        """
        msg = self.__assets_table.query(self.__uid)
        if msg.status == Message.SUCCESS:
            return msg.user_info.assets
        else:
            return 0

    def query_transfer(self):
        """
        查询当前用户转账信息
        :return: (bool)
        """
        msg = self.__audit_table.query(self.__uid, self.__user_table.table, self.__user_table.column_uid,
                                       self.__user_table.column_name)
        if msg.status == Message.SUCCESS:
            print("| {:<4} | {:<24} | {:<8} | {:<24} |".format('编号', '收账用户', '金额', '时间'))
            for i, item in enumerate(msg.transfer_info):
                print("| {:<4} | {:<24} | {:<8} | {:<24} |".format(i + 1, item.name, item.money,
                                                                   item.update_time.strftime('%Y-%m-%d %H:%M:%S')))
            return True
        return False

    @property
    def uid(self):
        return self.__uid

    @property
    def name(self):
        return self.__name


# 控制层。包括用户信息表、资产表、审计表的初始化，查询、修改、插入等操作。
class AuditTable(object):
    """
    审计表
    """

    def __init__(self, mysql):
        self.table = 'audit'
        self.column_transfer_uid = 'transfer_uid'
        self.column_receivable_uid = 'receivable_uid'
        self.column_money = 'money'
        self.column_update_time = 'update_time'
        self.mysql = mysql

        self.__init_table__()

    def __init_table__(self):
        sql = "CREATE TABLE IF NOT EXISTS `{}`(" \
              "`{}` VARCHAR(128) NOT NULL," \
              "`{}` VARCHAR(128) NOT NULL," \
              "`{}` SMALLINT NOT NULL," \
              "`{}` timestamp NOT NULL," \
              "INDEX `t_uid` (`{}`))".format(self.table,
                                             self.column_transfer_uid,
                                             self.column_receivable_uid,
                                             self.column_money,
                                             self.column_update_time,
                                             self.column_transfer_uid)
        self.mysql.execute_(sql)

    def add(self, transfer_uid, receivable_uid, money):
        sql = "INSERT INTO `{}` " \
              "(`{}`, `{}`, `{}`, `{}`)  " \
              "VALUES ('{}', '{}', {}, '{}')".format(self.table,
                                                     self.column_transfer_uid,
                                                     self.column_receivable_uid,
                                                     self.column_money,
                                                     self.column_update_time,
                                                     transfer_uid,
                                                     receivable_uid,
                                                     money,
                                                     get_time())
        msg = self.mysql.execute_(sql)
        return msg

    def query(self, uid, u_table, u_uid_field, u_name_field):
        """
        查询转账记录。
        :param uid: (str) 用户 uid
        :param u_table: (str) 用户表名
        :param u_uid_field: (str) 用户表uid字段名
        :param u_name_field: (str) 用户表name字段名
        :return: (Message)
        """
        sql = "SELECT `{}`.`{}`, `{}`.`{}`, `{}`.`{}`, " \
              "`{}`.`{}`, `{}`.`{}` " \
              "FROM `{}` " \
              "INNER JOIN `{}` " \
              "ON `{}`.`{}`=`{}`.`{}` " \
              "WHERE `{}`.`{}`='{}'".format(self.table, self.column_receivable_uid,
                                            self.table, self.column_money,
                                            self.table, self.column_update_time,
                                            u_table, u_uid_field, u_table, u_name_field,
                                            self.table,
                                            u_table,
                                            u_table, u_uid_field, self.table, self.column_receivable_uid,
                                            self.table, self.column_transfer_uid, uid)
        msg = self.mysql.query_all(sql)
        # 提取保存查询到的信息。
        if msg.status == Message.SUCCESS:
            for item in msg.result:
                info = Message.TransferInfo(name=item[u_name_field],
                                            money=item[self.column_money],
                                            update_time=item[self.column_update_time])
                msg.transfer_info.append(info)
            msg.result = None
        return msg


class AssetsTable(object):
    """
    资产表
    """

    def __init__(self, mysql):
        self.table = 'assets'
        self.column_uid = 'uid'
        self.column_assets = 'assets'
        self.mysql = mysql

        self.__init_table__()

    def __init_table__(self):
        sql = "CREATE TABLE IF NOT EXISTS `{}`(" \
              "`{}` VARCHAR(128) NOT NULL," \
              "`{}` SMALLINT NOT NULL, " \
              "PRIMARY KEY(`{}`))".format(self.table, self.column_uid, self.column_assets, self.column_uid)
        self.mysql.execute_(sql)

    def add(self, uid, money):
        """
        用户充值
        :param uid: (str)
        :param money: (int)
        :return: (Message)
        """
        money = self._mul(money)
        sql = "INSERT INTO `{}` (`{}`, `{}`) VALUES ('{}', {})".format(self.table, self.column_uid, self.column_assets,
                                                                       uid, money)
        msg = self.mysql.execute_(sql)
        return msg

    def query(self, uid):
        """
        查询当前用户资产
        :param uid: (str)
        :return: (Message)
        """
        sql = "SELECT `{}` FROM `{}` WHERE `uid`='{}'".format(self.column_assets, self.table, uid)
        msg = self.mysql.query_one(sql)
        if msg.status == Message.SUCCESS:
            msg.user_info.assets = self._div(msg.result[self.column_assets])
            msg.result = None
        return msg

    def update(self, uid, money):
        """
        更新用户资产
        :param uid: (str)
        :param money: (int)
        :return: (Message)
        """
        money = self._mul(money)
        sql = "UPDATE `{}` SET `{}` = {} WHERE `{}`='{}'".format(self.table, self.column_assets, money, self.column_uid,
                                                                 uid)
        msg = self.mysql.execute_(sql)
        return msg

    def update_transfer(self, transfer_uid, receivable_uid, money):
        """
        更新转账资产
        :param transfer_uid: (str)
        :param receivable_uid:  (str)
        :param money:  (int)
        :return:  (Message)
        """
        money = self._mul(money)
        sql = "UPDATE `{}` u1, `{}` u2 " \
              "SET u1.{}=u1.{}-{}, " \
              "u2.{}=u2.{}+{} " \
              "WHERE u1.uid='{}' and u2.uid='{}'".format(self.table, self.table,
                                                         self.column_assets, self.column_assets, money,
                                                         self.column_assets, self.column_assets, money,
                                                         transfer_uid, receivable_uid)
        msg = self.mysql.execute_(sql)
        return msg

    def _mul(self, money):
        # 乘以 100 精确到小数点后两位。保存整数。
        return int(money * 100)

    def _div(self, money):
        # 还原数值，除以 100 转换成浮点数。
        return money / 100


class UserTable(object):
    """
    用户信息表
    """

    def __init__(self, mysql):
        self.table = 'user_info'
        self.column_uid = 'uid'
        self.column_name = 'name'
        self.mysql = mysql

        self.__init_table__()

    def __init_table__(self):
        sql = "CREATE TABLE IF NOT EXISTS `{}`(" \
              "`{}` VARCHAR(128) NOT NULL," \
              "`{}` VARCHAR(50) NOT NULL," \
              "PRIMARY KEY(`{}`))".format(self.table, self.column_uid, self.column_name, self.column_uid)
        self.mysql.execute_(sql)

    def add(self, name):
        """
        添加用户到表
        :param name: (str)
        :return: (Message) uid
        """
        uid = str(uuid.uuid4())
        sql = "INSERT INTO `{}` (`{}`, `{}`)  " \
              "VALUES ('{}', '{}')".format(self.table, self.column_uid, self.column_name, uid, name)
        msg = self.mysql.execute_(sql)
        if msg.status == Message.SUCCESS:
            msg.user_info.uid = uid
            msg.user_info.name = name
        return msg

    def query(self, uid):
        """
        通过uid查询用户信息
        :param uid: (str)
        :return: (Message)
        """
        sql = "SELECT `{}`, `{}` FROM `{}` WHERE `{}` = '{}'".format(self.column_uid, self.column_name,
                                                                     self.table, self.column_uid, uid)
        msg = self.mysql.query_one(sql)
        if msg.status == Message.SUCCESS:
            # 提取出查询的信息。并保存在 user_info 对象中。并将 msg.result 设置为 None
            if msg.result is not None:
                msg.user_info.uid = msg.result[self.column_uid]
                msg.user_info.name = msg.result[self.column_name]
            msg.result = None

        return msg


# 数据库层。执行数据的相关操作。
# 为控制层提供的 SQL 语句进行执行。并返回相关信息
class Mysql(object):
    def __init__(self, host, port, user, password, database):
        """ 初始化数据库 """
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.charset = 'utf8mb4'

        # 模拟测试 mysql 事务。
        self.affair = False

        self.__init_connection__()

    def __init_connection__(self):
        self.connection = pymysql.connect(host=self.__host,
                                          port=self.__port,
                                          user=self.__user,
                                          password=self.__password,
                                          db=self.__database,
                                          charset=self.charset,
                                          cursorclass=pymysql.cursors.DictCursor)

    def execute_(self, sql):
        """
        执行语句。
        :param sql: (str)
        :return: (Message)
        """
        msg = Message()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            # 模拟测试。插入异常语句。测试转账时候，出现异常。是否转账成功。
            if self.affair:
                a = 1 / 0
            self.connection.commit()
            msg.status = Message.SUCCESS
        except Exception as e:
            # print("Failed to execute database. SQL：{}".format(sql))
            self.connection.rollback()
            msg.status = Message.FAILED
            raise e
        finally:
            return msg

    def query_one(self, sql):
        """
        执行查询。获取一个结果
        :param sql: (str)
        :return: (Message)
        """
        msg = Message()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
            self.connection.commit()
            msg.status = Message.SUCCESS
            msg.result = result
        except Exception as e:
            print("Failed to execute database. SQL：{}".format(sql))
            msg.status = Message.FAILED
            raise e
        finally:
            return msg

    def query_all(self, sql):
        """
        执行查询。获取一个结果
        :param sql: (str)
        :return: (Message)
        """
        msg = Message()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            self.connection.commit()
            msg.status = Message.SUCCESS
            msg.result = result
        except Exception as e:
            print("Failed to execute database. SQL：{}".format(sql))
            msg.status = Message.FAILED
            raise e
        finally:
            return msg

    def close(self):
        self.connection.close()


class Message(object):
    """
    上下文交互信息对象。用于在数据库层、控制层、应用层进行信息传递。
    """
    SUCCESS = 'success'
    FAILED = 'fail'

    class UserInfo(object):
        """
        用户信息。内部类。
        """

        def __init__(self, name=None, uid=None, assets=None):
            self.name = name
            self.uid = uid
            self.assets = assets

        def __str__(self):
            return json.dumps({'name': self.name,
                               'money': self.uid,
                               'update_time': self.assets})
            # return "{name:{}, uid:{}, assets:{}}".format(self.name, self.uid, self.assets)

    class TransferInfo(object):
        """
        转账信息。内部类
        """

        def __init__(self, name=None, money=None, update_time=None):
            self.name = name
            self.money = money
            self.update_time = update_time

        def __str__(self):
            return json.dumps({'name': self.name,
                               'money': self.money,
                               'update_time': self.update_time.isoformat()})

    def __init__(self, status=None, msg=None, result=None):
        self.status = status
        self.msg = msg
        self.result = result
        self.user_info = Message.UserInfo()
        self.transfer_info = []

    def __repr__(self):
        res = {'status': self.status,
               'msg': self.msg,
               'result': str(self.result),
               'user_info': str(self.user_info),
               'transfer_info': str(self.transfer_info)}

        return json.dumps(res)


def init():
    """
    初始化
    :return:
    """
    config = read_config(CONFIG, 'mysql')
    # print(config)

    # 初始化 mysql
    mysql = Mysql(user=config['user'], password=config['password'], host=config['host'], port=int(config['port']),
                  database=config['database'])

    # 初始化表
    user_table = UserTable(mysql)
    assets_table = AssetsTable(mysql)
    audit_table = AuditTable(mysql)

    # 初始化用户注册机制
    register = Register(user_table, assets_table, audit_table)
    return register, mysql


def main():
    register, mysql = init()
    try:
        # 注册两个用户。一个转账，一个收账。
        user_name1 = "Mora"
        user_name2 = "Edna"
        transfer_user = register.register(user_name1)
        collection_user = register.register(user_name2)

        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 转账用户先充值
        print()
        print("{:*^64}".format("充值 100￥"))
        transfer_user.recharge(100)
        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 模拟转账 1. 期望提示转账成功
        print()
        print("{:*^64}".format("转账 50￥"))
        transfer_user.transfer(collection_user.uid, 50)
        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 模拟转账 2. 期望提示转账成功
        print()
        print("{:*^64}".format("转账 20￥"))
        transfer_user.transfer(collection_user.uid, 20)
        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 模拟转账. 期望提示转账失败，余额不足
        print()
        print("{:*^64}".format("转账 100￥"))
        transfer_user.transfer(collection_user.uid, 100)
        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 模拟转账. 期望提示转账失败，数据库操作异常
        print()
        print("{:*^64}".format("转账 5￥ (启动异常语句)"))
        # 开启异常
        mysql.affair = True
        transfer_user.transfer(collection_user.uid, 5)
        print("转账用户 {} 资产: {}".format(user_name1, transfer_user.assets()))
        print("收账用户 {} 资产: {}".format(user_name2, collection_user.assets()))

        # 查询用户转账信息
        print()
        print("{:*^64}".format("查看转账信息"))
        transfer_user.query_transfer()

    except Exception as e:
        print(e)
    finally:
        mysql.close()


if __name__ == '__main__':
    main()
