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
        self.chrome_options = Options()
        prefs = {'profile.managed_default_content_settings.images': 2}
        self.chrome_options.add_experimental_option('prefs', prefs)
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 以开发者模式

    def get_driver(self):
        return webdriver.Chrome(options=self.chrome_options)
        #
