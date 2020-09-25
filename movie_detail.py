# coding:utf-8
import json
import time
import uuid

import requests

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
            self.get_movie_detail(i)
            print(i)
        self.save_as_json()

    def get_movie_detail(self, url, file_name='movie_detail.json'):
        self.driver.get('https://www.ifvod.tv/detaili?id=' + url)
        self.proxy.new_har(url, options={'captureHeaders': True, 'captureContent': True})
        result = self.proxy.har
        time_start = time.time()
        flag = False
        while time.time() - time_start < 30:
            if 'log' in result is None or 'entries' in result['log']:
                result = self.proxy.har
            for entry in result['log']['entries']:
                if 'request' in entry and 'url' in entry['request']:
                    _url = entry['request']['url']
                    if "api/video/detail" in _url:
                        r = requests.get(_url)
                        flag = True
                        result = self.get_movie_info(r.json())
                        with open(file_name, 'a+') as file:
                            file.write(json.dumps(result, ensure_ascii=False) + '\n')
                            print(json.dumps(result, ensure_ascii=False))
                        time_end = time.time()
                        print(time_end - time_start)

            if flag:
                break
            result = self.proxy.har
        if not flag:
            print("quit chrome")
            self.driver.quit()
            self.server.stop()
            self.proxy.close()
            time.sleep(10)
            print("reopen chrome ")
            self.driver, self.server, self.proxy = ChromeDriver().get_driver()
            self.get_movie_detail(url)

    def get_movie_info(self, json_dic):
        info = json_dic['data']['info'][0]
        result = dict()
        result["language"] = info['vl']['lang']
        result["publishYear"] = info['post_Year']
        result["brief"] = info['contxt']
        result["review"] = info['commentNumber']
        result["addDate"] = info['add_date']
        result["unlike"] = info['vl']['dc']
        result["region"] = info['vl']['regional']
        result["hotRank"] = info['vl']['hot']
        result["actor"] = info['vl']['starring']
        result["channel"] = info['channel']
        result["name"] = info['vl']['title']
        result["director"] = info['vl']['director']
        result["like"] = info['vl']['dd']
        result["category"] = info['videoType']
        image_name = str(uuid.uuid1())
        result['image'] = image_name
        ImageSaver().save_image('https:' + info['imgPath'], image_name)
        return result

    def load_file(self):
        url_list = list()
        with open("url.json", "r") as file:
            text_lines = file.readlines()
            for line in text_lines:
                url_list.extend(json.loads(line))
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
    MovieDetail().start_crawl()
