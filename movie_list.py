# coding:utf-8
import json
import sys
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

from chrome_driver import ChromeDriver


class MovieList:
    def __init__(self, url):
        # 初始化Chrome
        self.driver = ChromeDriver().driver
        # self.driver.set_page_load_timeout(10)
        # self.driver.maximize_window()
        try:
            self.driver.get(url)
            f = open('url.txt', 'w+')
            f.close()
        except TimeoutException:
            print(u'页面加载超过设定时间，超时')
            # 当页面加载时间超过设定时间，
            # 通过执行Javascript来stop加载，然后继续执行后续动作

    def get_movie_list(self, count=1):
        movie_url_list = list()
        timer = 0
        while len(movie_url_list) <= 0 or movie_url_list is None:
            source = BeautifulSoup(self.driver.page_source, "lxml")
            time.sleep(0.5)
            movie_url_list = source.select(
                'app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.search-results.d-flex.flex-wrap.justify-content-between.ng-star-inserted > app-video-teaser > div > a ')
            timer += 1
            if timer % 20 == 0:
                self.driver.execute_script("location.reload()")
        with open('url.txt', 'a+') as file:
            url_list = list()
            for i in movie_url_list:
                map = dict()
                map['id'] = i.get('href').split("=")[1]
                map['hot_count'] = count
                url_list.append(map)
                count += 1
            file.write(json.dumps(url_list, ensure_ascii=False) + '\n')
            print(json.dumps(url_list))
        next_page = self.driver.find_elements_by_css_selector(
            'body > div.root-container > app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.d-flex.mb-5.page-controls.align-items-center.justify-content-center.ng-star-inserted > app-pager > ul > li')[
            -2]
        if next_page.get_attribute('class') == 'disabled':
            self.driver.close()
            sys.exit(0)
        else:
            next_page.click()
            try:
                self.get_movie_list(count)
            except Exception:
                self.driver.execute_script("location.reload()")
                self.get_movie_list(count)


    def next_page(self, url):
        self.driver.get(url)
        next_page = self.driver.find_elements_by_css_selector(
            'body > div.root-container > app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.d-flex.mb-5.page-controls.align-items-center.justify-content-center.ng-star-inserted > app-pager > ul > li')[
            -2]
        if next_page.get_attribute('class') == 'disabled':
            self.driver.close()
            sys.exit(0)
        else:
            next_page.click()
            self.get_movie_list()

    def __del__(self):
        self.driver.close()
