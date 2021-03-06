import os

import requests


class ImageSaver:
    def save_image(self, image_url, file_dir, name):
        if not image_url:
            return False
        size = 0
        number = 0
        while size == 0:
            img_file = requests.get(image_url)
            file_path = file_dir + name
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
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

    '''
    图片保存的路径
    '''

    def image_path(self, image_name):
        return image_name
