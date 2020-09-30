# coding:utf-8
import json
import os
import time
import uuid

import requests

from chrome_driver import ChromeDriver
from image_saver import ImageSaver


class Banner:
    def __init__(self, project_path='project/'):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
        self.project_path = project_path
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        f = open(project_path + 'banner.json', 'w+')
        f.close()

    def get_limitation(self):
        url = 'https://www.ifvod.tv/movies'
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
                    time_end = time.time()
                    if "/api/home/getflashbanner" in _url:
                        r = requests.get(_url)
                        m = r.json()
                        info = m['data']['info']
                        for i in info:
                            image_name = str(uuid.uuid1())
                            ImageSaver().save_image('https:' + i['img'], 'banner_image/', image_name + '.png')
                        with open(self.project_path + 'banner.json', 'w+') as f:
                            f.write(json.dumps(json.dumps(info, ensure_ascii=False)))
                        print(_url, time_end - time_start)
                        return True

        self.driver.quit()
        self.server.stop()


if __name__ == '__main__':
    banner = Banner()
    banner.get_limitation()
