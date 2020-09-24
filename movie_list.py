# coding:utf-8
import json
import time

import requests

from chrome_driver import ChromeDriver


class MovieList:
    def __init__(self):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
        f = open('url.txt', 'w+')
        f.close()

    def get_movie_list(self, page=1):
        url = 'https://www.ifvod.tv/list?keyword=&star=&page={0}&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'.format(
            page)
        self.driver.get(url)
        self.proxy.new_har("datayes" + str(page), options={'captureHeaders': True, 'captureContent': True})
        result = self.proxy.har
        time_start = time.time()
        flag = False
        while time.time() - time_start < 60:
            if 'log' in result is None or 'entries' in result['log']:
                result = self.proxy.har
            for entry in result['log']['entries']:
                if 'request' in entry and 'url' in entry['request']:
                    _url = entry['request']['url']
                    if "api/list/Search" in _url:
                        r = requests.get(_url)
                        flag = True
                        time_end = time.time()
                        with open('url.txt', 'a+') as file:
                            file.write(json.dumps(r.json()['data']['info'][0]['result'], ensure_ascii=False) + '\n')
                            print(_url, time_end - time_start)
            if flag:
                break
            result = self.proxy.har

        if not flag:
            print("quit chrome")
            self.driver.quit()
            self.server.stop()
            self.proxy.close()
            print("reopen chrome ")
            self.driver, self.server, self.proxy = ChromeDriver().get_driver()
            self.get_movie_list(page)
            return
        next_page = self.driver.find_elements_by_css_selector(
            'body > div.root-container > app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.d-flex.mb-5.page-controls.align-items-center.justify-content-center.ng-star-inserted > app-pager > ul > li')[
            -2]
        if next_page.get_attribute('class') == 'disabled':
            self.driver.quit()
            self.server.stop()
            self.proxy.close()
        page += 1
        self.get_movie_list(page)

if __name__ == '__main__':
    movie = MovieList()
    movie.get_movie_list()
