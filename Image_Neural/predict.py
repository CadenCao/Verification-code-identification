# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/16
# 该模块用于预测
import os
import random
from torch.utils.data import DataLoader
from mydataset import my_dataset
import one_hot
import common
import torch
import shutil
from torchvision import transforms
import noise_getout
import PIL

# 单张图片验证
def predict_single(Image_path):
    image = PIL.Image.open(Image_path)
    image = noise_getout.remove_noise(image, k=4)
    trans = transforms.Compose(
        [
            transforms.ToTensor(),  # 转化为张量
            transforms.Resize((36, 170)),  # 固定像素变化，防止不一致
        ]
    )
    img_tensor = trans(image)
    img_tensor = img_tensor.reshape((1, 1, 36, 170))
    m = torch.load('model2.pth')
    output = m(img_tensor)
    output = output.view(-1, common.captcha_array.__len__())
    output_label = one_hot.vecText(output)
    return output_label

# 多图片验证
def predict_group(path):  # path为待验证的验证码文件地址
    test_dataset = my_dataset(path)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True)
    test_len = test_dataset.__len__()
    correct = 0
    for i, (images, labels) in enumerate(test_dataloader):
        images = images.cuda()
        labels = labels.cuda()
        labels = labels.view(-1, common.captcha_array.__len__())
        label_text = one_hot.vecText(labels)
        m = torch.load('model2.pth')
        output = m(images)
        output = output.view(-1, common.captcha_array.__len__())
        output_test = one_hot.vecText(output)
        if label_text == output_test:
            correct += 1
            print('正确值：{}，预测值：{}'.format(label_text, output_test))
        else:
            print('正确值{}，预测值{}'.format(label_text, output_test))
    print("测试样本总数{},预测正确率：{}".format(len(os.listdir(path)),
                                     correct / len(os.listdir(path)) * 100))

# 多验证码图片验证
if __name__ == '__main__':
    print(predict_single(r'.\dataset/test2/7gfX8a.png'))