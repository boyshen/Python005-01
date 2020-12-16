# -*- encoding: utf-8 -*-
"""
@file: crawling.py
@time: 2020/12/14 上午10:58
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 从豆瓣中爬取数据信息并写入到数据库中
"""
import re
import requests
import pymysql
import uuid
from lxml import etree
from fake_useragent import UserAgent

# cookie
COOKIE = './cookie.txt'

MYSQL_HOST = '192.168.10.43'
MYSQL_PORT = 3306
MYSQL_USER = 'ekpapi'
MYSQL_PASSWORD = 'P@ssw0rd'
MYSQL_DATABASE = 'test'


class Crawling(object):
    def __init__(self, cookie):
        self.time_out = 60
        self.cookie = cookie
        self.sess = requests.Session()

        self.url = "https://movie.douban.com/subject/34454004/comments?start={}&limit={}&status=P&sort=new_score"
        self.limit = 20

        self.__init_headers__()
        self.__init_xpath__()

    def __init_headers__(self):
        self.user_agent = UserAgent(verify_ssl=False)
        self.headers = {
            'user-agent': self.user_agent.random,
            'cookie': self.cookie
        }

    def __init_xpath__(self):
        self.xpath_movie = "//div[@id='content']/h1/text()"
        self.xpath_star = "//div[@id='content']//div[@class='comment']/h3//span[@class='comment-info']/span[2]/@class"
        self.xpath_date = "//div[@id='content']//div[@class='comment']/h3//span[@class='comment-info']/span[3]/text()"
        self.xpath_comment = "//div[@id='content']//div[@class='comment']/p/span/text()"

    def crawling(self, url):
        """
        爬取数据
        :return: (str)
        """
        print("start crawling data ...")
        text = ""
        try:
            response = self.sess.get(url, headers=self.headers, timeout=self.time_out)
        except requests.Timeout as e:
            print("Request Time Out. url:{}".format(url))
            raise e
        except Exception as e:
            print("Failed Request url:{}".format(url))
            raise e
        else:
            text = response.text
        finally:
            return text

    def parser(self, text):
        """
        解析数据
        :param text: (str)
        :return: (dict)
        """
        print("start parser data ...")
        if len(text) == 0 or text == '':
            return {}

        html = etree.HTML(text)
        movie = html.xpath(self.xpath_movie)
        assert len(movie) == 1, print("Check the Xpath for movie.")

        stars = html.xpath(self.xpath_star)
        dates = html.xpath(self.xpath_date)
        comments = html.xpath(self.xpath_comment)

        result = []
        for star, date, comment in zip(stars, dates, comments):
            star = re.search('[0-5]{1}', star)
            if star is None:
                continue
            star = int(star.group())
            date = date.strip()
            comment = re.sub("(\\n)", "", comment)
            result.append({'star': star, 'date': date, 'comment': comment})

        return {'info': result, 'movie': movie[0]}

    def run(self, num):
        """
        爬取并解析数据
        :param num: (int) 获取数据的轮次。每轮次 20 条数据
        :return: (dict)
        """
        res = {'info': [], 'movie': ''}
        for i in range(num):
            start = i * self.limit
            url = self.url.format(start, self.limit)

            text = self.crawling(url)
            result = self.parser(text)

            if len(result) != 0:
                res['info'] = result['info'] + res['info']
                res['movie'] = result['movie']

        return res

    def close(self):
        self.sess.close()


class Movie(object):
    def __init__(self, mysql):
        self.mysql = mysql
        self.table = 'movie'
        self.mid = 'mid'
        self.name = 'name'

        self.__init_table__()

    def __init_table__(self):
        sql = "CREATE TABLE IF NOT EXISTS `{table}`(" \
              "`{mid}` VARCHAR(128) NOT NULL," \
              "`{name}` VARCHAR(50) NOT NULL," \
              "PRIMARY KEY(`{mid}`))".format(table=self.table, mid=self.mid, name=self.name)
        self.mysql.execute_(sql)

    def add(self, mid, name):
        sql = "INSERT INTO `{table}` " \
              "(`{mid}`, `{name}`) " \
              "VALUES ('{mid_value}', '{name_value}')".format(table=self.table,
                                                              mid=self.mid,
                                                              name=self.name,
                                                              mid_value=mid,
                                                              name_value=name)
        self.mysql.execute_(sql)


class Comment(object):
    def __init__(self, mysql):
        self.mysql = mysql
        self.table = 'comment'
        self.id = 'id'
        self.mid = 'mid'
        self.comment = 'comment'
        self.date = 'date'
        self.star = 'star'

        self.__init_table()

    def __init_table(self):
        sql = "CREATE TABLE IF NOT EXISTS `{table}`(" \
              "`{id}` BIGINT(20) NOT NULL AUTO_INCREMENT," \
              "`{mid}` VARCHAR(128) NOT NULL," \
              "`{star}` INT NOT NULL," \
              "`{comment}` TEXT NOT NULL," \
              "`{date}` DATETIME NOT NULL," \
              "PRIMARY KEY(`id`)," \
              "INDEX `mid` (`mid`)" \
              ")".format(table=self.table, id=self.id, mid=self.mid, star=self.star, comment=self.comment,
                         date=self.date)
        self.mysql.execute_(sql)

    def add(self, mid, star, comment, date):
        sql = "INSERT INTO `{table}` " \
              "(`{mid}`, `{star}`, `{comment}`, `{date}`)  " \
              "VALUES ('{mid_value}', {star_value}, '{comment_value}', '{date_value}')".format(table=self.table,
                                                                                               mid=self.mid,
                                                                                               star=self.star,
                                                                                               comment=self.comment,
                                                                                               date=self.date,
                                                                                               mid_value=mid,
                                                                                               star_value=star,
                                                                                               comment_value=comment,
                                                                                               date_value=date)
        self.mysql.execute_(sql)


class Mysql(object):
    def __init__(self, host, port, user, password, database):
        """ 初始化数据库 """
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

    def execute_(self, sql):
        """
        执行语句。
        :param sql: (str)
        :return: (Message)
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            # print("Failed to execute database. SQL：{}".format(sql))
            self.connection.rollback()
            # self.connection.commit()
            raise e
        else:
            self.connection.commit()

    def close(self):
        self.connection.close()


def init():
    # 初始化 cookie
    with open(COOKIE, 'r') as f:
        cookie = f.read()

    # 初始化 mysql
    mysql = Mysql(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)

    # 初始化表
    movie = Movie(mysql)
    comment = Comment(mysql)

    # 初始化爬虫
    crawling = Crawling(cookie=cookie)

    return mysql, movie, comment, crawling


def main(num):
    mysql, movie, comment, crawling = init()
    try:
        result = crawling.run(num)
        if result:
            mid = str(uuid.uuid4())
            movie.add(mid=mid, name=result['movie'])
            for item in result['info']:
                comment.add(mid=mid, star=item['star'], comment=item['comment'], date=item['date'])
        print("write data over! ")
    except Exception as e:
        raise e
    finally:
        crawling.close()
        mysql.close()


if __name__ == '__main__':
    main(10)
