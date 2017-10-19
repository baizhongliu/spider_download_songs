# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:26:51 2017

@author: Frank
"""

import csv
import requests
import os

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    ##输出成html&&CSV等外部文件
    def output_html(self):
        
        with open("output_test_0930.csv","w",encoding='utf-8',newline="") as datacsv:
            #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
            csvwriter = csv.writer(datacsv,dialect = ("excel"))
            #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            csvwriter.writerow(['url', 'vol.title', 'vol.no','vol.summary','vol.cover.url','song_order','song_name','artist','album','lyric','song_play_url','song_cover_url'])
            #第一行：文件名
            index_page = 0
            for data in self.datas:
                ##记录正在下载页面的顺序编号
                index_page += 1
                for sub_data in data:
                    csvwriter.writerow([sub_data['url'],sub_data['Vol.title'],sub_data['Vol.no'],sub_data['Vol.summary'],sub_data['Vol.cover.url'],sub_data['Song_order'],sub_data['Song_name'],sub_data['Artist'],sub_data['Album'],sub_data['Lyric'],sub_data['Song_play_url'],sub_data['Song_cover_img_url']])
                    
                    ##下载歌曲的链接
                    url_song = sub_data['Song_play_url']
                    ##下载歌曲的输出地址信息
                    new_dir = 'C:\\Python work file\\luoo_download\\'
                    number_cont = sub_data['Vol.no']
                    title_cont = sub_data['Vol.title']
                    output_dir = new_dir+number_cont+'.'+title_cont
                    song_name = sub_data['Song_name']
                    song_order = sub_data['Song_order']
                    
                    ##如果歌曲本身已经存在，那么不进行下载；否则进行下载
                    if not(os.path.exists(output_dir+'\\'+song_name+'.mp3')):
                        print('Downloading：page'+str(index_page)+' song'+song_order)
                        try:
                            r = requests.get(url_song,stream=True)
                            with open(output_dir+'\\'+song_name+'.mp3','wb') as fd:
                                for chunk in r.iter_content():
                                    fd.write(chunk)
                                fd.close()
                        except:
                            print('request download song failed：'+url_song)
                    else:
                        print('Song already exist!')

                
    
        
                
                    