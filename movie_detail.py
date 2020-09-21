# coding:utf-8
import json
import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

from chrome_driver import ChromeDriver


class MovieDetail:
    def __init__(self, url):
        # 初始化Chrome
        self.driver = ChromeDriver().driver
        self.driver.set_page_load_timeout(10)
        self.driver.maximize_window()
        try:
            self.driver.get(url)
            f = open('movie_detail.txt', 'w+')
            f.close()
        except TimeoutException:
            print(u'页面加载超过设定时间，超时')
            # 当页面加载时间超过设定时间，
            # 通过执行Javascript来stop加载，然后继续执行后续动作

    def get_movie_detail(self):
        time.sleep(1)
        source = BeautifulSoup(self.driver.page_source, "lxml")
        self.get_movie_info(source)
        # with open('movie_detail.txt','a+') as file:
        #     for i in movie_url_list:
        #         file.write(json.dumps(map))
        #         print(json.dumps(map))

    def get_movie_info(self, source):
        movie_info = list()
        for i in source.select(
                'body > div.root-container > app-root > app-index > div.border-warp > div.container >div.page-container >div.d-flex > app-video-info > div.video-detail > div'):
            movie_info.append(i.get_text())
        print(movie_info)

        count = source.select(
            'body > div.root-container > app-root > app-index > div.border-warp > div.container > div.page-container > app-video-user-data-bar > div > div.d-flex > div.ico > div.d-flex')
        for i in count:
            print(i.get_text().strip(), ' ')

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    url_list = list()
    with open("url.txt", "r") as file:
        text_lines = file.readlines()
        for line in text_lines:
            url_list.append(json.loads(line))

    detail = MovieDetail('https://www.ifvod.tv/detail?id=zZNjvZ3GLEA')
    detail.get_movie_detail()
    # movie.get_movie_list()
    # movie = driver.find_element_by_css_selector(
    #     'body > div.root-container > app-root > app-search > div > div.page-container.list > div.search-top.ng-star-inserted > div:nth-child(1) > div > app-search-filter:nth-child(1) > div > div.d-flex > div.filter-button.mr-2.mb-1.ng-star-inserted')
    # movie.click()
    # time.sleep(2)
    # # source = BeautifulSoup(driver.page_source, "lxml")
    # text=driver.find_elements_by_css_selector('body > div.root-container > app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.d-flex.mb-5.page-controls.align-items-center.justify-content-center.ng-star-inserted > app-pager > ul > li')
    #
    # if text[-2].get_attribute('class') == 'disabled':
    #     print('yes')
    # driver.close()
