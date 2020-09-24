from chrome_driver import ChromeDriver

driver, server, proxy = ChromeDriver().get_driver()
base_url = 'https://www.ifvod.tv/list?keyword=&star=&page=1&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'
driver.get(base_url)

result = proxy.har
while True:
    if result['log']['entries'] is None or len(result['log']['entries']) <= 0:
        result = proxy.har
    flag = False
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        if "api/list/Search" in _url:
            flag = True
    if flag:
        break
    result = proxy.har


for entry in result['log']['entries']:
    _url = entry['request']['url']
    # 根据URL找到数据接口
    if "api/list/Search" in _url:
        _response = entry['response']
        _content = _response['content']['text']
        # 获取接口返回内容
        print(_content)
driver.close()
server.stop()
