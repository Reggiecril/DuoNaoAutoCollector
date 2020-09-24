# coding:utf-8
import time

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
        while time.time() - time_start < 100:
            if result['log']['entries'] is None or len(result['log']['entries']) <= 0:
                result = self.proxy.har
            for entry in result['log']['entries']:
                _url = entry['request']['url']
                if "api/list/Search" in _url:
                    _response = entry['response']
                    _content = _response['content']['text']
                    flag = True
                    time_end = time.time()
                    with open('url.txt', 'a+') as file:
                        file.write(_content + '\n')
                        print(_url, time_end - time_start)
            if flag:
                break
            result = self.proxy.har
        if not flag:
            print("quit chrome")
            self.driver.quit()
            print("reopen chrome ")
            self.driver, self.server, self.proxy = ChromeDriver().get_driver()
            self.get_movie_list(page)

        movie_url_list = list()
        # result = self.proxy.har
        # for entry in result['log']['entries']:
        #     _url = entry['request']['url']
        #     # 根据URL找到数据接口
        #     if "api/list/Search" in _url:
        #         _response = entry['response']
        #         _content = _response['content']['text']
        #         print(_content)
        #         break
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
        self.driver.quit()
        self.server.stop()


if __name__ == '__main__':
    movie = MovieList()
    movie.get_movie_list()
