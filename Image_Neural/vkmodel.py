# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/14
# 用于构建CNN模型，返回图片的最终特征
from torch import nn
import torch
import common


class vkmodel(nn.Module):
    def __init__(self):
        super(vkmodel, self).__init__()
        self.layer1 = nn.Sequential(
            # 图片通道为1,卷积核数量为64个，卷积核为3*3大小，上下填充为1
            nn.Conv2d(in_channels=1, out_channels=64, kernel_size=3, padding=1),
            # 激活层为relu
            nn.ReLU(),
            # 池化层大小为2*2，步幅默认为池化窗口大小一致，也即stride=(2*2)
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.layer5 = nn.Sequential(
            # 将数据展平为2维，第一个维度是图片个数
            nn.Flatten(),
            # 全连接层1
            nn.Linear(in_features=10240, out_features=4056),
            nn.Dropout(0.2),
            nn.ReLU(),
            # 全连接层2，输出维度维验证码长度（6）乘字典个数
            nn.Linear(in_features=4056, out_features=common.captcha_size*common.captcha_array.__len__())
        )

    def forward(self, x):
        # 若X为【64，2，60，160】,则第一层输出【64，64，30，80】
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        return x


if __name__ == "__main__":
    data = torch.ones(64, 1, 36, 170)
    m = vkmodel()
    x = m(data)     # 使用了__call__函数，使得实例化对象可以当函数使用
    print(x.shape)