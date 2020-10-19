# import os
#
# import paramiko
#
#
# def send_file(file_name):
#     client = paramiko.SSHClient()  # 获取SSHClient实例
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect(hostname="122.51.155.8", username="ubuntu", password="Cloud19961008", port=22)  # 连接SSH服务端
#     transport = client.get_transport()  # 获取Transport实例
#
#     # 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
#     sftp = paramiko.SFTPClient.from_transport(transport)
#
#     for root, dirs, files in os.walk(file_name):
#         path = '/home/ubuntu' + root.replace(file_name, '') + '/'
#         if path == '/home/ubuntu//':
#             path = '/home/ubuntu/'
#         print('当前目录路径', path)  # 当前目录路径
#         print('当前路径下所有非目录子文件', files)  # 当前路径下所有非目录子文件
#         for i in files:
#             print(path + i)
#             print(root + '/' + i)
#             sftp.put(root + '/' + i, path + i)
#     sftp.close()
#     # 关闭连接
#     client.close()
#
#
# count = 0
# url = '/Users/xieyuncheng/Desktop/github/python/duoNaoAutoCollector/project/'
# print(url[:-1])
import json

l = list()
with open('movie_detail.json', 'r') as file:
    text_lines = file.readlines()
    for line in text_lines:
        l.append(json.loads(line))
with open('movie_detail.json', 'w+') as f:
    f.write(json.dumps(l, ensure_ascii=False))
