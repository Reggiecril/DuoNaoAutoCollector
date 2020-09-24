import os
import time

import requests


class ImageSaver:
    def save_image(self, image_url, name):
        if not image_url:
            return False
        size = 0
        number = 0
        while size == 0:
            try:
                img_file = requests.get(image_url)
            except requests.exceptions.RequestException as e:
                print(e)
            file_path = self.image_path(name)
            # 保存
            with open(file_path, 'wb') as f:
                f.write(img_file.content)
            # 判断是否正确保存图片
            size = os.path.getsize(file_path)
            if size == 0:
                os.remove(file_path)
            # 如果该图片获取超过十次则跳过
            number += 1
            if number >= 10:
                break
        return (file_path if (size > 0) else False)

    '''
    图片保存的路径
    '''

    def image_path(self, image_name):
        # 文件夹
        file_dir = 'images/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 文件名
        file_name = str(time.time())
        # 文件后缀
        suffix = '.jpeg'
        return file_dir + image_name + suffix

    # 检查是否为图片类型
    def check_image(self, content_type):
        if 'image' in content_type:
            return False
        else:
            return True