# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/13
# 获
from captcha.image import ImageCaptcha
import random
import time
captcha_array = list("123456789abcdefghijklmnopqrstuvwxyz")
captcha_size = 6


if __name__ == "__main__":
    for i in range(100):
        image = ImageCaptcha()
        image_text = "".join(random.sample(captcha_array, captcha_size))
        image_path = r".\dataset\test\{}_{}.png".format(image_text, int(time.time()))
        image.write(image_text, image_path)