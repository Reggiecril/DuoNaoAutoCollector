from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

server = Server(r'/root/browsermob-proxy-2.1.4/bin/browsermob-proxy')
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
prefs = {'profile.managed_default_content_settings.images': 2}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以开发者模式
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
driver = webdriver.Chrome(options=chrome_options)

base_url = 'https://www.ifvod.tv/list?keyword=&star=&page=1&pageSize=30&cid=0,1,3&year=-1&language=-1&region=-1&status=-1&orderBy=2&desc=true'
proxy.new_har("datayes", options={'captureHeaders': True, 'captureContent': True})
driver.get(base_url)

result = proxy.har

for entry in result['log']['entries']:
    _url = entry['request']['url']
    # 根据URL找到数据接口
    if "api/list/Search" in _url:
        _response = entry['response']
        _content = _response['content']['text']
        # 获取接口返回内容
        print(_content)

server.stop()
