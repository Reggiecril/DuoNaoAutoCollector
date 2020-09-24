# coding:utf-8
import json
import re
import time
import uuid

from bs4 import BeautifulSoup

from chrome_driver import ChromeDriver
from image_saver import ImageSaver


class MovieDetail:
    def __init__(self):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
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
        ImageSaver().save_image(source.find('app-gg-block').find('img').get('src'), imager_name)
        return map

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
                l.append(self.convert_json(line))
        with open('movie_detail.json', 'w+') as f:
            f.write(json.dumps(l, ensure_ascii=False))

    def convert_json(self, line):
        static_map = dict()
        static_map["语言"] = "language"
        static_map["年份"] = "publishYear"
        static_map["图片"] = "image"
        static_map["简介"] = "brief"
        static_map["评论"] = "review"
        static_map["添加"] = "addDate"
        static_map["踩"] = "unlike"
        static_map["区域"] = "region"
        static_map["热度排名"] = "hotRank"
        static_map["主演"] = "actor"
        static_map["频道"] = "channel"
        static_map["电影名"] = "name"
        static_map["导演"] = "director"
        static_map["赞"] = "like"
        static_map["分类"] = "category"
        map = json.loads(line)
        return_map = dict()
        for i in map:
            return_map[static_map[i]] = map[i]
        return return_map


if __name__ == '__main__':
    m = list()
    with open('url.json', 'r') as f:
        m = json.loads(f.read())
    print([i['key'] for i in m])
