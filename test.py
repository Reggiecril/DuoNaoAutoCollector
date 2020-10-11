import os

count = 0
url = '/Users/xieyuncheng/Desktop/github/python/duoNaoAutoCollector/project/'
path = '~/project'
for root, dirs, files in os.walk(url):
    count += 1
    print(count)
    print('当前目录路径', path + root.replace(url, '') + '/')  # 当前目录路径
    print('当前路径下所有非目录子文件', files)  # 当前路径下所有非目录子文件
