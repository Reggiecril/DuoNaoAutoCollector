# coding:utf-8
import json
import re
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

from chrome_driver import ChromeDriver
from movie_list import MovieList


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
        try:
            self.driver.get('https://www.ifvod.tv/detaili?id=' + url)
        except TimeoutException:
            print(u'页面加载超过设定时间，超时')
            # 当页面加载时间超过设定时间，
            # 通过执行Javascript来stop加载，然后继续执行后续动作

        map = self.get_movie_info(hot_count)
        if map is not None:
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
        map['图片'] = source.find('app-gg-block').find('img').get('src')
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
if __name__ == '__main__':
    movie = MovieList(
        'https://www.ifvod.tv/list?keyword=&star=&page=1&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true')
    movie.get_movie_list()
    detail = MovieDetail()
    detail.start_crawl()
