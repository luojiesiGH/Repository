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
import time
from openpyxl import Workbook


class XlsOutputer():
    def __init__(self, InfoQueue):
        self.queue = InfoQueue
        self.wb = Workbook()

    def output_xls(self):
        ws = self.wb.active
        count = 0
        fout = open('前程无忧.txt', 'a+', encoding='utf-8')
        while True:
            time.sleep(10)
            count = count + 1
            if count == 3:
                print("output ending")
                break
            try:
                while not self.queue.empty():
                    count = 0
                    data = self.queue.get()
                    ws.append(list(data.values()))
                    info = ""
                    for value in data.values():
                        info = info + value + "\t"
                    fout.write(info)
                    fout.write("\n")
                    self.queue.task_done()
            except Exception as e:
                print("pass")
            print("waitting info")
        self.wb.save("前程.xlsx")
        fout.close()
