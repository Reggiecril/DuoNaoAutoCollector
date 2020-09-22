from selenium import webdriver

from selenium.webdriver.chrome.options import Options


class ChromeDriver:
    def __init__(self):
        """
        构建chrome driver
        :param window_w: 设置窗口宽度
        :param window_h: 设置窗口高度
        :param wait_sec: 最大等待时间，单位：秒
        """
        chrome_options = Options()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以开发者模式
        driver = webdriver.Chrome(options=chrome_options)
        #
        self.driver = driver
