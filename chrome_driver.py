from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from selenium.webdriver.chrome.options import Options


class ChromeDriver:
    def get_driver(self):
        # /root/browsermob-proxy-2.1.4/bin/browsermob-proxy
        server = Server(r'/root/browsermob-proxy-2.1.4/bin/browsermob-proxy')
        server.start()
        proxy = server.create_proxy()
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"
        chrome_options = Options()
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        prefs = {'profile.managed_default_content_settings.images': 2}
        # chrome_options.add_experimental_option('prefs', prefs)
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以开发者模式
        chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
        drive = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
        proxy.new_har("datayes", options={'captureHeaders': True, 'captureContent': True})
        return drive, server, proxy
        #
