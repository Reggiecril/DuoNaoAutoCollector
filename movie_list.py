# coding:utf-8

from selenium.common.exceptions import TimeoutException

from chrome_driver import ChromeDriver


class MovieList:
    def __init__(self):
        # 初始化Chrome
        self.driver, self.server, self.proxy = ChromeDriver().get_driver()
        self.driver.set_page_load_timeout(60)
        f = open('url.txt', 'w+')
        f.close()

    def get_movie_list(self, page=1):
        url = 'https://www.ifvod.tv/list?keyword=&star=&page={0}&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'.format(
            page)
        try:
            self.driver.get(url)
            result = self.proxy.new_har("datayes" + str(page), options={'captureHeaders': True, 'captureContent': True})

            while True:
                if result['log']['entries'] is None or len(result['log']['entries']) <= 0:
                    result = self.proxy.har
                flag = False
                for entry in result['log']['entries']:
                    _url = entry['request']['url']
                    if "api/list/Search" in _url:
                        flag = True
                if flag:
                    break
                result = self.proxy.har
        except TimeoutException:
            print("超时")
        movie_url_list = list()
        result = self.proxy.har
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # 根据URL找到数据接口
            if "api/list/Search" in _url:
                _response = entry['response']
                _content = _response['content']['text']
                print(_content)
                break
        # with open('url.txt', 'a+') as file:
        #     url_list = list()
        #     for i in movie_url_list:
        #         map = dict()
        #         map['id'] = i.get('href').split("=")[1]
        #         map['hot_count'] = count
        #         url_list.append(map)
        #         count += 1
        #     file.write(json.dumps(url_list, ensure_ascii=False) + '\n')
        #     print(json.dumps(url_list))
        page += 1
        self.get_movie_list(page)

    def __del__(self):
        self.driver.close()
        self.server.stop()


if __name__ == '__main__':
    movie = MovieList()
    movie.get_movie_list()
