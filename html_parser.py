# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:26:40 2017

@author: Frank
"""

import os
#import shutil
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import json

class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.html
        links = soup.find_all('a', href=re.compile(r'http://www.luoo.net/vol/index/\d+'))
        for link in links:
            new_url = link['href']
            # 让 new_url 以 page_url 为模板拼接成一个全新的 url
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            #print(new_url) 
            #print(new_full_url) 
            new_urls.add(new_full_url)
        return new_urls


    def _get_new_data(self, page_url, soup):
        
        ##定义一个函数来获取歌曲的函数
        def get_lyric(data_sid):
            lrc_url = 'http://www.luoo.net/single/lyric/'+data_sid
            lyric = requests.get(lrc_url)
            json_obj = lyric.text
            j = json.loads(json_obj)
            lrc = j['lyric']
            
            if lrc == '':
                return ''
            else:
                song_lyric = lrc['content'].split('</div>')[1]
                return song_lyric.replace('<br>\n',',')

        #期刊的标题、期刊号码、简介、期刊封面图片网址、
        title_node = soup.find('span', class_ = "vol-title")
        number_node = soup.find('span', class_ = "vol-number rounded")
        desc_node = soup.find('div', class_ = 'vol-desc')
        vol_img_node = soup.find('img', class_ = 'vol-cover')
        
        
        title_cont = title_node.get_text()
        number_cont = number_node.get_text()
        desc_cont = desc_node.get_text()
        vol_img_url = vol_img_node['src']
        
        ##对于每一个期刊创建一个文件夹作为：期刊封面图片、下载歌曲的输出
        ##如果该目录不存在则创建，否则不做操作
        current_dir = 'C:\\Python work file\\luoo_download'
        dir_new = current_dir+'\\'+number_cont+'.'+title_cont
        if not(os.path.exists(dir_new)):
            os.mkdir(dir_new)
        else:
            print('Directory already exist!')
        ##在该路径下存放对应期刊的封面图片，如果图片不存在才进行图片下载
        if not(os.path.exists(dir_new+'\\'+'Cover.jpg')):
            try:    
                urllib.request.urlretrieve(vol_img_url,dir_new+'\\'+'Cover.jpg')
            except:
                print('download cover failed：',vol_img_url)
        else:
            print('Cover already exist!')
            
        
        #页面内歌曲列表信息，添加歌曲播放地址、歌曲封面图片地址
        songs_list = []
        songs_nodes = soup.find_all('li',class_ = 'track-item rounded')
        
        for song_node in songs_nodes:
            name_node = song_node.find('a',class_ = 'trackname btn-play')
            artist_node = song_node.find('p',class_ = 'artist')
            album_node = song_node.find('p',class_ = 'album')
            lyric_node = song_node.find('a',class_ = 'icon-info')
            
            #如果没找到相关类直接以空值''替代
            if name_node == None:
                name_song = ''
            else:
                name_song = name_node.get_text()
                
            if artist_node == None:
                artist_song = ''
            else:
                artist_song = artist_node.get_text()
            
            if album_node == None:
                album_song = ''
            else:
                album_song = album_node.get_text()
                
            if lyric_node == None:
                data_sid = ''
            else:
                data_sid = lyric_node['data-sid']
                
            ##歌曲播放网址
            song_order = name_song.split('.')[0]
            song_play_url = 'http://mp3-cdn2.luoo.net/low/luoo/radio'+number_cont+'/'+song_order+'.mp3'
            ##歌曲封面图片网址
            link_song_img=song_node.find('img',class_='cover rounded')
            if link_song_img == None:
                url_song_img = ''
            else:
                url_song_img = link_song_img['src']

                
            ##将歌曲的信息合并，加入list中
            ##返回一个列表，里面储存的是歌曲的信息 && 每一个列表中的元素是一个dict
            song_dict = {}
            song_dict['url'] = page_url
            song_dict['Vol.title'] = title_cont
            song_dict['Vol.no'] = number_cont
            song_dict['Vol.summary'] = desc_cont
            song_dict['Vol.cover.url'] = vol_img_url
            song_dict['Song_order'] = song_order
            song_dict['Song_name'] = re.sub("\d+\.","",name_song).strip()
            song_dict['Artist'] = artist_song.replace('Artist:','').strip()
            song_dict['Album'] = album_song.replace('Album:','').strip()
            song_dict['Lyric'] = get_lyric(data_sid).strip()
            song_dict['Song_play_url'] = song_play_url
            song_dict['Song_cover_img_url'] = url_song_img
            
            songs_list.append(song_dict)
                        
        return songs_list
    

    def paser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding = 'utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
    