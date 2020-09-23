# coding:utf-8
import json
import os
import re
import time
import uuid

import requests
from bs4 import BeautifulSoup

from chrome_driver import ChromeDriver


class MovieDetail:
    def __init__(self):
        # 初始化Chrome
        self.driver = ChromeDriver().driver
        # self.driver.set_page_load_timeout(10)
        f = open('movie_detail.json', 'w+')
        f.close()

    def start_crawl(self):
        url_list = self.load_file()
        for i in url_list:
            for j in i:
                self.get_movie_detail(j['id'], j['hot_count'])
                print(j['id'], j['hot_count'])
        self.save_as_json()

    def get_movie_detail(self, url, hot_count=0, file_name='movie_detail.json'):
        map = dict()
        while len(map) <= 0 or map is None:
            try:
                self.driver.get('https://www.ifvod.tv/detaili?id=' + url)
                map = self.get_movie_info(hot_count)
            except Exception:
                continue
            with open(file_name, 'a+') as file:
                file.write(json.dumps(map, ensure_ascii=False) + '\n')
                print(json.dumps(map, ensure_ascii=False))

    def get_movie_info(self, hot_count):
        map = dict()
        movie_info = list()
        source = BeautifulSoup(self.driver.page_source, "lxml")
        timer = 0
        while movie_info is None or len(movie_info) <= 0:
            source = BeautifulSoup(self.driver.page_source, "lxml")
            for i in source.select(
                    'body > div.root-container > app-root > app-index > div.border-warp > div.container >div.page-container >div.d-flex > app-video-info > div.video-detail > div'):
                movie_info.append(i.get_text())
            time.sleep(0.5)
            timer += 1
            if timer % 10 == 0:
                self.driver.execute_script("location.reload()")
            if timer > 50:
                return None
        map['电影名'] = movie_info[0]
        movie_info = movie_info[2:]
        for i in movie_info:
            map[i.split('：')[0].strip()] = i.split('：')[1].strip()
        number = source.select(
            'body > div.root-container > app-root > app-index > div.border-warp > div.container > div.page-container > app-video-user-data-bar > div > div.d-flex > div.ico > div.d-flex')
        map['评论'] = re.sub("\D", "", number[0].get_text())
        map['赞'] = re.sub("\D", "", number[1].get_text())
        map['踩'] = re.sub("\D", "", number[2].get_text())
        brief = source.find('app-summary')
        map['简介'] = brief.get_text()
        map['热度排名'] = hot_count
        imager_name = str(uuid.uuid1())
        map['图片'] = imager_name
        self.save_image(source.find('app-gg-block').find('img').get('src'), imager_name)
        return map

    def __del__(self):
        self.driver.close()

    def load_file(self):
        url_list = list()
        with open("url.txt", "r") as file:
            text_lines = file.readlines()
            for line in text_lines:
                url_list.append(json.loads(line))
        return url_list

    def save_as_json(self):
        l = list()
        with open('movie_detail.json', 'r') as file:
            text_lines = file.readlines()
            for line in text_lines:
                l.append(json.loads(line))
        with open('movie_detail.json', 'w+') as f:
            f.write(json.dumps(l, ensure_ascii=False))

    def save_image(self, image_url, name):
        if not image_url:
            return False
        size = 0
        number = 0
        while size == 0:
            try:
                proxy = {'http': 'http://officepx.datayes.com:1080/', 'https': 'http://officepx.datayes.com:1080/'}
                img_file = requests.get(image_url, proxies=proxy)
            except requests.exceptions.RequestException as e:
                raise e
            file_path = self.image_path(name)
            # 保存
            with open(file_path, 'wb') as f:
                f.write(img_file.content)
            # 判断是否正确保存图片
            size = os.path.getsize(file_path)
            if size == 0:
                os.remove(file_path)
            # 如果该图片获取超过十次则跳过
            number += 1
            if number >= 10:
                break
        return (file_path if (size > 0) else False)

    '''
    图片保存的路径
    '''

    def image_path(self, image_name):
        # 文件夹
        file_dir = 'images/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 文件名
        file_name = str(time.time())
        # 文件后缀
        suffix = '.jpeg'
        return file_dir + image_name + suffix

    # 检查是否为图片类型
    def check_image(self, content_type):
        if 'image' in content_type:
            return False
        else:
            return True
if __name__ == '__main__':
    # movie = MovieList(
    #     'https://www.ifvod.tv/list?keyword=&star=&page=1&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true')
    # movie.get_movie_list()
    detail = MovieDetail()
    detail.start_crawl()
