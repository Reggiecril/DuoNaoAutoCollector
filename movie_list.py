# coding:utf-8
import json
import math
import os
import time

import requests

from chrome_driver import ChromeDriver
from mysql import Database


class MovieList:
    def __init__(self, project_path='/root/project/'):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
        self.project_path = project_path
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        f = open(project_path + 'url.json', 'w+')
        f.close()

    def start_crawl(self):
        limitation = self.get_limitation()
        for i in range(1, limitation):
            flag = self.get_movie_list(i)
            while not flag:
                print("quit chrome")
                self.driver.quit()
                self.server.stop()
                time.sleep(5)
                print("reopen chrome ")
                self.driver, self.server, self.proxy = ChromeDriver().get_driver()
                flag = self.get_movie_list(i)
        self.driver.quit()
        self.server.stop()
        time.sleep(5)
        self.rewrite_result()

    def rewrite_result(self):
        db_id = Database().get_all_id()
        local_id = self.load_file()
        final_list = list()
        for i in local_id:
            if i not in db_id:
                final_list.append(i)
        with open(self.project_path + "url.json", "w+") as file:
            file.write(json.dumps(final_list, ensure_ascii=False))

    def load_file(self):
        url_list = list()
        with open(self.project_path + "url.json", "r") as file:
            text_lines = file.readlines()
            for line in text_lines:
                url_list.extend(json.loads(line))
        return url_list

    def get_movie_list(self, page):
        url = 'https://www.ifvod.tv/list?keyword=&star=&page={0}&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'.format(
            page)
        self.driver.get(url)
        self.proxy.new_har("datayes", options={'captureHeaders': True, 'captureContent': True})
        result = self.proxy.har
        time_start = time.time()
        flag = False
        while time.time() - time_start < 10:
            if 'log' in result is None or 'entries' in result['log']:
                result = self.proxy.har
            for entry in result['log']['entries']:
                if 'request' in entry and 'url' in entry['request']:
                    _url = entry['request']['url']
                    if "api/list/Search" in _url:
                        r = requests.get(_url)
                        flag = True
                        time_end = time.time()
                        with open(self.project_path + 'url.json', 'a+') as file:
                            file.write(json.dumps([i['key'] for i in r.json()['data']['info'][0]['result']],
                                                  ensure_ascii=False) + '\n')
                            print(_url, time_end - time_start)
            if flag:
                break
            result = self.proxy.har
        return flag


    def get_limitation(self):
        url = 'https://www.ifvod.tv/list?keyword=&star=&page={0}&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'.format(
            1)
        self.driver.get(url)
        self.proxy.new_har("datayes-1", options={'captureHeaders': True, 'captureContent': True})
        result = self.proxy.har
        time_start = time.time()
        while time.time() - time_start < 60:
            if 'log' in result is None or 'entries' in result['log']:
                result = self.proxy.har
            for entry in result['log']['entries']:
                if 'request' in entry and 'url' in entry['request']:
                    _url = entry['request']['url']
                    if "api/list/Search" in _url:
                        r = requests.get(_url)
                        print(_url)
                        return math.ceil(int(r.json()['data']['info'][0]['recordcount']) / 30)


if __name__ == '__main__':
    movie = MovieList()
    movie.start_crawl()
