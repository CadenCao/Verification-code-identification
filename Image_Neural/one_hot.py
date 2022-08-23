 # 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/14
# text2vc用于将验证码转one-hot，vecText用于将one-hot转验证码
import torch
import common


# 字母转one-hot编码，如aabb转one-hot编码，词典为common.captcha_array
def text2vc(text):
    vec = torch.zeros(common.captcha_size, len(common.captcha_array))
    # print(vec)
    for i in range(len(text)):
        vec[i, common.captcha_array.index(text[i])] = 1
    return vec

# 还原，one-hot编码转字母
def vecText(vec):
    vec = torch.argmax(vec, dim=1)
    text = ''
    for i in vec:
        text += common.captcha_array[i]
    return text


if __name__ == "__main__":
    vec = text2vc('aab1cd')
    # vec = vec.view(1, -1)[0]
    print(vec, vec.shape)
    print(vecText(vec))

