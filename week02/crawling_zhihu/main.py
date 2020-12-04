# -*- encoding: utf-8 -*-
"""
@file: main.py
@time: 2020/12/3 上午10:18
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:
"""

import requests
from fake_useragent import UserAgent

try:
    from week02.crawling_zhihu.crawling import Engine
    from week02.crawling_zhihu.crawling import Crawling
except ModuleNotFoundError:
    import sys

    sys.path.append('./')
    from .crawling import Engine
    from .crawling import Crawling

# 问题ID. www.zhihu.com 网页上对应的问题 id 值。例如：https://www.zhihu.com/question/52368821 最后的字符串
QUESTIONS = ["52368821", "301253397"]

# cookie 文件。已经登录网页的 cookie 信息。
COOKIE_FILE = './cookie.txt'

# 保存结果的文件。
RESULT_FILE = './result/result.json'

# 获取答案的数量。如果为 0 则获取页面中所有的答案。
ANSWER_NUMBER = 16

# 选择答案的排序的方式。 zhihu 页面上提供了两种排序的方式。分别是 default(默认排序) 和 updated(按时间排序) 。
SORTED_BY = "default"


def main():
    """
    主程序
    :return:
    """
    # 读取cookie
    with open(COOKIE_FILE, 'r') as rf:
        cookie = rf.read()

    # 去除重复的id
    question = (set(QUESTIONS))

    # 检查配置
    if not check_config(cookie, SORTED_BY):
        return False

    # 执行
    engine = Engine(question=question, cookie=cookie, result_file=RESULT_FILE, answer_number=ANSWER_NUMBER,
                    sort_by=SORTED_BY)
    engine.run()


def check_cookie(cookie):
    """
    检查 cookie 是否可以登陆。
    :param cookie: (str) cookie
    :return: (bool)
    """
    user_agent = UserAgent(verify_ssl=False)
    headers = {
        'user-agent': user_agent.random,
        'cookie': cookie,
    }

    login_url = "https://www.zhihu.com/signup"
    response = requests.get(login_url, headers=headers, allow_redirects=False)
    if response.status_code == 302:
        return True
    print("Invalid cookie !")
    return False


def check_sort_by(sort_by):
    """
    检查爬取的排序方式。
    :param sort_by: (str) default 或 updated
    :return: (bool)
    """
    _sort = (Crawling.UPDATED, Crawling.DEFAULT)
    if sort_by not in _sort:
        print("Invalid config of SORT_BY. SORT_BY in [{}]".format(_sort))
        return False
    return True


def check_config(cookie, sort_by):
    """
    检查配置信息
    :param cookie: (str) cookie
    :param sort_by: (str) sort_by
    :return: (bool)
    """
    if not check_cookie(cookie):
        return False
    if not check_sort_by(sort_by):
        return False
    return True


if __name__ == '__main__':
    main()
