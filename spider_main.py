# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:27:14 2017

@author: Frank
"""

from luoo_songs_V3 import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    # 爬虫总调度程序会使用 url 管理器、 html 的下载器、解析器、输出器，下面初始化一下：
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.download = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url): # craw 方法，爬虫调度程序
        count = 1
        # 入口 url 添加到 url 管理器
        self.urls.add_new_url(root_url)

        # 启动爬虫循环
        while self.urls.has_new_url():
            try:
                # 当 url 管理器里待爬取的 url 时，获取一个 url
                new_url = self.urls.get_new_url()
                print('craw %d : %s' % (count, new_url)) # 打印传入的第几个 url
                # 启动下载器并存储
                html_cont = self.download.download(new_url)
                # 解析数据
                new_urls, new_data = self.parser.paser(new_url, html_cont)
                # 添加进 url 管理器
                self.urls.add_new_urls(new_urls)
                # 收集数据
                self.outputer.collect_data(new_data)

                if count == 5:
                    break
                count+=1
            except:
                print('crew faild:')

        # 输出收集好的数据
        self.outputer.output_html()

if __name__ == "__main__":
    root_url = 'http://www.luoo.net/vol/index/1152'
    obj_spider = SpiderMain()
    obj_spider.craw(root_url) # 启动爬虫
    
    