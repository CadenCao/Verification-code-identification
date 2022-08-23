# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/14
# 用于最终模型的训练以及准确率测度
import torch
from torch import nn
from torch.optim import Adam
from mydataset import my_dataset
from torch.utils.data import DataLoader
from vkmodel import vkmodel

if __name__ == "__main__":
    # test_dataset = my_dataset(r'.\dataset\test')
    # test_dataloader = DataLoader(test_dataset, batch_size=40, shuffle=True)  # 数据预加载
    train_dataset = my_dataset(r'.\dataset\train2')
    train_dataloader = DataLoader(train_dataset, batch_size=30, shuffle=True)
    vkmodel = vkmodel()
    # 损失函数维多标签损失函数
    loss_fn = nn.MultiLabelSoftMarginLoss().cuda()
    optim = Adam(vkmodel.parameters(), lr=0.001)
    for epoch in range(15):
        print('外层训练次数{}'.format(epoch))
        for i, (images, labels) in enumerate(train_dataloader):
            images=images.cuda()
            labels=labels.cuda()
            # 模型标记为train
            vkmodel.train()
            output = vkmodel(images)
            loss = loss_fn(output, labels)
            optim.zero_grad()
            loss.backward()
            optim.step()
            if i % 500 == 0:
                print('训练次数{}，损失函数{}'.format(i, loss.item()))
# 模型保存
torch.save(vkmodel, 'model2.pth')
