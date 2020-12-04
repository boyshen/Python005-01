# -*- encoding: utf-8 -*-
"""
@file: crawling.py
@time: 2020/12/1 下午4:01
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:
"""
import os
import re
import json
import requests
import unittest
from tqdm import tqdm
from lxml import etree
from fake_useragent import UserAgent


class CrawlingStruct(object):
    HTML = 'html'
    JSON = 'json'

    def __init__(self, qid=None, content_type=None, status=None, text=None):
        self.qid = qid
        self.content_type = content_type
        self.status = status
        self.text = text


class ParserStruct(object):
    def __init__(self, qid=None, question=None, question_desc=None):
        self.qid = qid
        self.question = question
        self.question_desc = question_desc
        self.answer_author = []
        self.answer_vote = []
        self.answer = []


class Crawling(object):
    """
    爬取网页内容
    """
    # 排序方式。default 为默认排序。 updated 为按时间排序
    DEFAULT = "default"
    UPDATED = "updated"

    def __init__(self, questions, cookie, sort_by=DEFAULT, timeout=60, number=0):
        """
        :param questions: (list or tuple) 知乎问题 id
        :param cookie: (str) cookie 信息
        :param sort_by: (str) 排序方式。默认排序和按时间排序
        :param timeout: (int) 请求超时时间
        :param number: (int) 指定需要保留答案的数量。如果为 0 则默认保存全部。
        """
        self.questions = questions
        self.__cookie = cookie
        self.sort_by = sort_by
        self.timeout = timeout
        self.number = number
        self.sess = requests.Session()

        # 获取问题页面的模板
        self.url = "https://www.zhihu.com/question/{}"

        # 获取问题答案的接口模板。来自 "www.zhihu.com" 。其中几个重要的参数。
        # 问题 id
        # limit   ==> 每次获取多少条答案。
        # offset  ==> 从第几条开始。
        # sort_by ==> default 为默认排序。 updated 为按时间排序
        self.answer_url = "https://www.zhihu.com/api/v4/questions/{}/answers?" \
                          "include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%" \
                          "2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%" \
                          "2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%" \
                          "2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%" \
                          "2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%" \
                          "2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%" \
                          "2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%" \
                          "2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos" \
                          "%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%" \
                          "3Bsettings.table_of_content.enabled%3B&limit={}&offset={}&platform=desktop&sort_by={}"

        self.__init_headers__()

    def __init_headers__(self):
        self.user_agent = UserAgent(verify_ssl=False)
        self.headers = {
            'user-agent': self.user_agent.random,
            'cookie': self.__cookie,
        }

    def run(self):
        """
        爬取问题和答案信息。
        :return: (list[CrawlingStruct]) 列表格式。保存爬取的网页内容信息。
        """
        print("start crawling ...")
        arr = []
        for qid in self.questions:
            arr.append(self.crawling_question(qid=qid))
            arr.extend(self.crawling_answer(qid=qid))
        return arr

    def get_request_url(self, qid):
        """
        拼接请求问题的 url
        :param qid: (str) 问题 id 值
        :return: (str) url
        """
        return self.url.format(qid)

    def get_answer_url(self, qid, limit=1, offset=0):
        """
        获取回答值
        :param qid: (str) 问题 id
        :param limit: (int) 每次获取多少条答案。默认为 1 条
        :param offset: (int) 从第几条开始。
        :return: (str) url
        """
        return self.answer_url.format(qid, limit, offset, self.sort_by)

    def crawling_question(self, qid):
        """
        爬取问题网页信息。
        :return:  (CrawlingStruct) 保存爬取的网页内容信息。
        """
        url = self.get_request_url(qid)
        try:
            response = self.sess.get(url, headers=self.headers, timeout=self.timeout)
            node = CrawlingStruct(qid=qid, content_type=CrawlingStruct.HTML, text=response.text,
                                  status=response.status_code)
            return node
        except requests.Timeout as e:
            print(e)
            print("Request Time out. url:{}".format(url))
        except Exception as e:
            print(e)
            print("Failed request. url:{}".format(url))

    def crawling_answer(self, qid):
        """
        爬取问题答案信息。
        :return: (list[CrawlingStruct]) 列表格式。保存爬取的网页内容信息。
        """
        url = self.get_answer_url(qid=qid, limit=1, offset=0)
        try:
            response = self.sess.get(url, headers=self.headers, timeout=self.timeout)
            totals = json.loads(response.text)['paging']['totals']
            totals = min(totals, self.number) if self.number != 0 else totals
            return self._iter_crawling_answer(qid, totals)
        except requests.Timeout as e:
            print(e)
            print("Request Time out. url:{}".format(url))
        except Exception as e:
            print(e)
            print("Failed request. url:{}".format(url))

    def _iter_crawling_answer(self, qid, totals):
        """
        循环获取批次答案
        :param qid: (str) 问题 id
        :param totals:  (int) 总共的答案
        :return: (list[CrawlingStruct]) 列表格式。保存爬取的网页内容信息。
        """
        arr = []
        for item in tqdm(range(totals)):
            url = self.get_answer_url(qid=qid, limit=1, offset=item)
            try:
                response = self.sess.get(url, headers=self.headers, timeout=self.timeout)
                node = CrawlingStruct(qid=qid, content_type=CrawlingStruct.JSON, status=response.status_code,
                                      text=response.text)
                arr.append(node)
            except requests.Timeout as e:
                print(e)
                print("Request Time out. url:{}".format(url))
            except Exception as e:
                print(e)
                print("Failed request. url:{}".format(url))
        return arr


class Parser(object):
    """
    解析网页内容
    """
    # 获取网页的状态信息
    STATUS_200 = 200

    # xpath：获取问题
    XPATH_PROB = "//div[@class='QuestionPage']//div[@class='QuestionHeader-main']/h1/text()"

    # xpath：获取问题的详细描述
    XPATH_PROB_DESC = "//div[@class='QuestionPage']//div[@class='QuestionHeader-main']/div[2]/div/div/div/span/text()"

    # # xpath：获取回答问题的作者
    # XPATH_ANSWER_AUTHOR = "//div[@class='List-item']//div[@class='ContentItem-meta']/div/meta[1]/@content"
    #
    # # xpath: 获取回答的答案中有多少个赞
    # XPATH_FABULOUS = \
    #     "//div[@class='List-item']//div[@class='ContentItem AnswerItem']//meta[@itemprop='upvoteCount']"
    #
    # # xpath: 获取回答的详细信息
    # XPATH_ANSWER = \
    #     "//div[@class='List-item']//div[@class='RichContent RichContent--unescapable']" \
    #     "/div[@class='RichContent-inner']/span/text()"

    def __init__(self, data):
        """
        :param data: (list[CrawlingStruct]) 列表格式。保存爬取的网页内容信息。
        """
        self.data = data

    def run(self):
        """
        解析网页内容。
        :return: (dict[ParserStruct]) 字典格式
        """
        print("start parser ...")
        arr_dict = {}
        for item in tqdm(self.data):
            node = arr_dict.get(item.qid, ParserStruct(qid=item.qid))
            if item.content_type == CrawlingStruct.HTML and item.status == Parser.STATUS_200:
                html = etree.HTML(item.text)
                prob = html.xpath(Parser.XPATH_PROB)
                prob_desc = html.xpath(Parser.XPATH_PROB_DESC)

                assert len(prob) == len(prob_desc) == 1, \
                    print("Check the XPath for the prob and the prob desc. pid:{}".format(item.pid))

                node.question = prob
                node.question_desc = prob_desc

            elif item.content_type == CrawlingStruct.JSON and item.status == Parser.STATUS_200:
                json_data = json.loads(item.text)['data']
                for data in json_data:
                    node.answer_vote.append(data["voteup_count"])
                    node.answer_author.append(data["author"]["name"])
                    content = re.sub("""<[a-zA-Z]+.*?>|<\/[a-zA-Z]+.*?>""", "", data["content"])
                    node.answer.append(content)

                    assert len(node.answer_author) == len(node.answer_vote) == len(node.answer), \
                        print("Check json data. qid:{}, author:{}".format(item.qid, node.answer_author))

            arr_dict[item.qid] = node
        return arr_dict


class WriteFile(object):
    """
    写入文件
    """

    def __init__(self, file):
        """
        :param file: (str) 文件名
        """
        self.file = file
        self.__init_path__()

    def __init_path__(self):
        self.path = os.path.dirname(self.file)
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def write(self, data):
        """
        :param data: (list[ParserStruct])
        :return:
        """
        with open(self.file, 'a+', encoding='utf-8') as wf:
            for qid, node in data.items():
                question = node.question
                question_desc = node.question_desc
                for author, vote, answer in zip(node.answer_author, node.answer_vote, node.answer):
                    data = {'qid': qid,
                            'question': question,
                            'question_desc': question_desc,
                            'author': author,
                            'vote': vote,
                            'answer': answer}
                    wf.write(json.dumps(data, ensure_ascii=False) + '\n')

        print("write file over. File:{}".format(self.file))


class Engine(object):
    def __init__(self, question, cookie, result_file, answer_number, sort_by):
        self.question = question
        self.cookie = cookie
        self.result_file = result_file
        self.answer_number = answer_number
        self.sort_by = sort_by

    def run(self):
        crawling = Crawling(questions=self.question, cookie=self.cookie, number=16, sort_by=self.sort_by)
        data = crawling.run()

        parser = Parser(data)
        parser_data = parser.run()

        wf = WriteFile(self.result_file)
        wf.write(parser_data)


class TestCrawlingZhiHu(unittest.TestCase):
    """
    测试模块
    """
    def test_crawling(self):
        questions = ["52368821"]
        with open('./cookie.txt', 'r') as f:
            cookie = f.read()

        crawling = Crawling(questions, cookie, number=16)
        data = crawling.run()
        self.assertEqual(len(data), 17)
        for item in data:
            print(item.qid)
            print(item.status)
            print(item.content_type)
            print(item.text)

    def test_parser(self):
        questions = ["52368821"]
        with open('./cookie.txt', 'r') as f:
            cookie = f.read()

        crawling = Crawling(questions, cookie, number=16)
        data = crawling.run()
        self.assertEqual(len(data), 17)

        parser = Parser(data)
        parser_data = parser.run()
        for qid in questions:
            node = parser_data[qid]
            print(node.qid)
            print(node.question)
            print(node.question_desc)
            print(node.answer_author)
            print(node.answer_vote)
            print(node.answer)

    def test_writer(self):
        questions = ["52368821"]
        with open('./cookie.txt', 'r') as f:
            cookie = f.read()

        crawling = Crawling(questions, cookie, number=16)
        data = crawling.run()
        self.assertEqual(len(data), 17)

        parser = Parser(data)
        parser_data = parser.run()

        wf = WriteFile('./result/result.json')
        wf.write(parser_data)


if __name__ == '__main__':
    unittest.main()
