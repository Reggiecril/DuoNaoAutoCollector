import requests

# 请求地址
url = "https://m8.ifvod.tv/api/list/Search?cinema=1&page=313&size=30&orderby=2&desc=1&cid=0,1,3&isserial=-1&isIndex=-1&isfree=-1&vv=d1f60397e99adacb0da224b901cb78b2&pub=1600936210122"
proxies = {'http': 'http://officepx.datayes.com:1080', 'https': 'http://officepx.datayes.com:1080'}
# 发送get请求
r = requests.get(url, proxies=proxies)
# 获取返回的json数据
print(r.json()['data']['info'][0]['result'])
