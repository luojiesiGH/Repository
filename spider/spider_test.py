#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '爬虫'
__author__ = 'Dadrk'
__mtime__ = '3/14/2018'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

from urllib.request import urlopen
from urllib import error
from bs4 import BeautifulSoup
import xls_outputer
import threading
from queue import Queue
from openpyxl import Workbook
import time


class BS4Parser(object):
    def __init__(self):
        self.spiderpools = []
        # 页面链接队列
        self.urlq = Queue()
        # 页面返回信息队列
        self.infoq = Queue()

    def craw(self):
        self.outputer = xls_outputer.XlsOutputer(self.infoq)
        curlsT = threading.Thread(
            target=self.collecturls, name="CollectUrl", args=(1,))
        curlsT.start()
        for i in range(10):
            self.spiderpools.append(
                threading.Thread(target=self.collectpageinfo))
        self.spiderpools.append(threading.Thread(
            target=self.outputer.output_xls))
        for thread in self.spiderpools:
            thread.start()
        for thread in self.spiderpools:
            thread.join()
    # 获取招聘信息

    def collectpageinfo(self):
        count = 0
        while True:
            # 等待10s。等爬取页面链接的爬虫返回信息
            time.sleep(10)
            count = count+1
            # 设置定时，当等待时间超过20s，队列中还没信息时认为爬取完成
            if count == 2:
                print("urlq empty===========================================")
                break
            while not self.urlq.empty():
                count = 0
                CompanyPageUrl = self.urlq.get()
                data = {}
                try:
                    response = urlopen(CompanyPageUrl)
                    CompanyPage = BeautifulSoup(response, "html5lib")
                    self.crawcount = self.crawcount + 1
                    print("collect info %d" % self.crawcount)
                    try:
                        data["postion"] = CompanyPage.find(
                            "div", "tHeader tHjob").find("h1")["title"]
                        data["lname"] = CompanyPage.find(
                            "div", "tHeader tHjob").find("span", "lname").string
                        data["strong"] = CompanyPage.find(
                            "div", "tHeader tHjob").find("strong").string
                        data["cname"] = CompanyPage.find("div", "tHeader tHjob").find(
                            "p", "cname").find("a")["title"]
                        data["url"] = CompanyPageUrl
                        data["request"] = ""
                        for p in CompanyPage.find("div", "bmsg job_msg inbox").get_text().split():
                            if p == "分享":
                                break
                            data["request"] += p
                        self.infoq.put(data)
                    except Exception as e:
                        # print(e.reason)
                        print(CompanyPageUrl)
                except Exception as e:
                    print("craw page faild,putting in the queue~~~~~~~~~~~~~~~~~")
                    # print(e.reason)
                    self.urlq.put(CompanyPageUrl)
            print("Waitting Urls")

    # 获取招聘详细信息网页链接
    def collecturls(self, pagenumber):
        root_url = "http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,{page}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        try:
            print("craw page :" + str(pagenumber))
            # if pagenumber%10 == 0:
            #     print("craw page :"+ str(pagenumber))
            response = urlopen(root_url.format(page=pagenumber))
            page = BeautifulSoup(response, "html5lib")

            # 判断页面是否存在
            if len(page.find("div", "dw_table").find_all("div", {"class": "el"})) == 1:
                return

            # 搜集页面中的职位链接，添加到url队列中
            for div in page.find("div", "dw_table").find_all("div", {"class": "el"})[1:]:
                self.urlq.put(div.find("a")["href"])

            # 设置爬取的页面数(测试)
            if pagenumber == 3:
                print("urls collecting end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return
            # 如果存在下一页，跳转到下一页继续爬取
            pagenumber = pagenumber + 1
            self.collecturls(pagenumber)

        except error.URLError as e:
            # print(e.reason)
            print("faild to request from %d ,try again............" % pagenumber)
            self.collecturls(pagenumber)


if __name__ == "__main__":
    spider = BS4Parser()
    spider.craw()
