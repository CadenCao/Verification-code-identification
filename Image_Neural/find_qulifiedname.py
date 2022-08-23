# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/16
import os


dir = os.listdir(r'.\dataset\train2')
A = [name.split('.')[0] for name in dir]
# 判断验证所有字符是否为基本字符
for i in A:
    for j in i:
        if j.casefold() not in "123456789abcdefghijklmnopqrstuvwxyz":
            print(i)
    else:
        continue
# 判断验证码长度是否为6
# for i in A:
#     if len(i) != 6:
#         print(i)
#     else:
#         continue
