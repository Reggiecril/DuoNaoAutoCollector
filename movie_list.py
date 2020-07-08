#coding:utf-8
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from chrome_driver import ChromeDriver


class MovieList:
    def __init__(self,url,driver):
        # 初始化Chrome
        self.driver = driver
        self.driver.set_page_load_timeout(10)
        self.driver.maximize_window()
        try:
            self.driver.get(url)
            movie = driver.find_element_by_css_selector(
                'body > div.root-container > app-root > app-search > div > div.page-container.list > div.search-top.ng-star-inserted > div:nth-child(1) > div > app-search-filter:nth-child(1) > div > div.d-flex > div.filter-button.mr-2.mb-1.ng-star-inserted')
            movie.click()
            time.sleep(3)
        except TimeoutException:
            print(u'页面加载超过设定时间，超时')
            # 当页面加载时间超过设定时间，
            # 通过执行Javascript来stop加载，然后继续执行后续动作
    def get_movie_list(self):
        source = BeautifulSoup(self.driver.page_source, "lxml")

        current = self.driver.current_url
        movie_url_list = source.select(
            'app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.search-results.d-flex.flex-wrap.justify-content-between.ng-star-inserted > app-video-teaser > div > a ')
        for i in movie_url_list:
            print(i.get('href'))
            detail='https://www.ifvod.tv'+i.get('href')
            print(detail)
            self.driver.get(detail)
            time.sleep(2)
        self.next_page(current)

    def get_movie_detail(self,url):
        pass

    def next_page(self, url):
        self.driver.get(url)
        time.sleep(3)
        next_page = driver.find_elements_by_css_selector('body > div.root-container > app-root > app-search > div > div.page-container.list > div.inner.d-flex.flex-wrap > div > div.d-flex.mb-5.page-controls.align-items-center.justify-content-center.ng-star-inserted > app-pager > ul > li')[-2]
        if next_page.get_attribute('class') =='disabled':
            self.driver.close()
            sys.exit(0)
        else:
            self.driver.close()
            next_page.click()
            self.get_movie_list()

if __name__ == '__main__':
    driver = ChromeDriver().driver
    movie=MovieList('https://www.ifvod.tv/list',driver)
    movie.get_movie_list()
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