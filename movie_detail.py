# coding:utf-8
import json
import os
import shutil
import time
import uuid

import paramiko
import requests

from banner import Banner
from chrome_driver import ChromeDriver
from image_saver import ImageSaver
from movie_list import MovieList


class MovieDetail:
    def __init__(self, project_path='/root/project/'):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
        self.project_path = project_path
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        # self.driver.set_page_load_timeout(10)
        f = open(project_path + 'movie_detail.json', 'w+')
        f.close()
        file_dir = project_path + 'images/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            shutil.rmtree(file_dir)
            os.makedirs(file_dir)

    def start_crawl(self):
        url_list = self.load_file()
        count = 1
        time_start = time.time()
        for i in url_list:
            flag = self.get_movie_detail(i)
            while not flag:
                print("quit chrome", '=' * 50)
                self.driver.quit()
                print("driver.quit", '=' * 50)
                self.server.stop()
                print("server.stop", '=' * 50)
                time.sleep(10)
                print("reopen chrome ", '=' * 50)
                self.driver, self.server, self.proxy = ChromeDriver().get_driver()
                flag = self.get_movie_detail(i)
            print(count, i)
            count += 1
        self.save_as_json()
        self.driver.quit()
        self.server.stop()
        print('程序运行时间:', time.time() - time_start, '=' * 40)
        self.send_file(self.project_path)

    def load_file(self):
        url_list = list()
        with open(self.project_path + "url.json", "r") as file:
            url_list.extend(json.loads(file.read()))
        return url_list
    def get_movie_detail(self, url, file_name='movie_detail.json'):
        self.driver.get('https://www.ifvod.tv/detaili?id=' + url)
        self.proxy.new_har('datayes', options={'captureHeaders': True, 'captureContent': True})
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
                        r = None
                        count = 0
                        while r is None and count < 3:
                            r = requests.get(_url)
                            count += 1
                        if r is None:
                            return True
                        flag = True
                        res = self.get_movie_info(r.json())
                        with open(self.project_path + file_name, 'a+') as file:
                            file.write(json.dumps(res, ensure_ascii=False) + '\n')
                            print(_url)
                        time_end = time.time()
                        print(time_end - time_start)

            if flag:
                break
            result = self.proxy.har
        return flag

    def get_movie_info(self, json_dic):
        info = json_dic['data']['info'][0]
        result = dict()
        result["duonaoId"] = info['key']
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
        result["interest"] = info['vl']['dd']
        result["category"] = info['videoType']
        image_name = str(uuid.uuid1())
        result['image'] = image_name
        ImageSaver().save_image('https:' + info['imgPath'], self.project_path + 'images/', image_name + '.jpeg')
        return result

    def save_as_json(self):
        l = list()
        with open(self.project_path + 'movie_detail.json', 'r') as file:
            text_lines = file.readlines()
            for line in text_lines:
                l.append(json.loads(line))
        with open(self.project_path + 'movie_detail.json', 'w+') as f:
            f.write(json.dumps(l, ensure_ascii=False))

    def send_file(self, file_name):
        client = paramiko.SSHClient()  # 获取SSHClient实例
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect("122.51.155.8", username="ubuntu", password="Cloud19961008")  # 连接SSH服务端
        transport = client.get_transport()  # 获取Transport实例

        # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 将本地 api.py 上传至服务器 /www/test.py。文件上传并重命名为test.py
        sftp.put(file_name, "~/{}".format(file_name))

        # 关闭连接
        client.close()

if __name__ == '__main__':
    Banner().get_limitation()
    MovieList().start_crawl()
    MovieDetail().start_crawl()
