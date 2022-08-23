# -*- coding:utf-8 -*-
# author : Caden Cao time:2021/11/30
# 获取取出噪音后的图片，降噪方法为8邻域降噪
import os
from PIL import Image
# import pytesseract
from concurrent.futures import ThreadPoolExecutor
# import keyboard
import base64
import requests
# from aip import AipOcr


def remove_noise(img2, k=4):
    #    img处理数据，k过滤条件
    # 转化为黑白相片（一个通道）转换公式为：L = R * 299/1000 + G * 587/1000+ B * 114/1000
    img2 = img2.convert('L')
    # 获取图片的长宽
    w, h = img2.size

    def get_neighbors(img, r, c):
        count = 0
        for i in [r - 1, r, r + 1]:
            for j in [c - 1, c, c + 1]:
                # 获取某坐标为i，j像素点的像素值
                if img.getpixel((i,j)) > 220:  # 纯白色
                    count += 1
        return count

    #   两层for循环判断所有的点
    for x in range(w):
        for y in range(h):
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                # 边缘均赋值为白色
                img2.putpixel((x, y), 255)
            else:
                n = get_neighbors(img2, x, y)  # 获取邻居数量，纯白色的邻居
                if n > k:
                    img2.putpixel((x, y), 255)
    return img2


if __name__ == "__main__":
    filename = os.listdir(r'.\dataset\train2')
    for i in filename:
        filepath = os.path.join(r'.\dataset\train2', i)
        img1 = Image.open(filepath)
        result = remove_noise(img1)
        result.show()
        input('下一个')
