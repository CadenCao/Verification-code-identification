# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2022/1/13
# 将验证码图片转为张量，以及验证码转为一阶张量
import os
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
# from torch.utils.tensorboard import SummaryWriter
import one_hot
import noise_getout


class my_dataset(Dataset):
    def __init__(self, root_dir):
        super(my_dataset, self).__init__()
        self.image_path = [os.path.join(root_dir, image_name) for image_name in os.listdir(root_dir)]
        # 将图片转化成torch可识别
        self.transforms = transforms.Compose(
            [
                transforms.ToTensor(),  # 转化为张量
                transforms.Resize((36, 170)),  # 固定图片分辨力 ，防止不一致
            ]
        )

    def __len__(self):
        return self.image_path.__len__()

    def __getitem__(self, index):
        image_path = self.image_path[index]
        # 去除了了噪声（8邻域降噪）
        image = noise_getout.remove_noise(Image.open(image_path), k=4)
        # 将图片转化成torch可识别形状
        image = self.transforms(image)
        label = image_path.split('\\')[-1]
        # 训练图片的标签
        label = label.split('.')[0].casefold()
        # 将验证码（文本）转one-hot编码
        label_tensor = one_hot.text2vc(label)
        # 将验证码的one-hot编码变成一维数据，维度为【1,216】,216=36*6，36为词典长度，6为验证码个数
        label_tensor = label_tensor.view(1, -1)[0]
        # 输出特征的标签，image维度为【batch_size,图片长，图片宽】，label_tensor维度为【batch_size，6*36】
        return image, label_tensor


if __name__ == "__main__":
    train_data = my_dataset(r'./dataset/train2')
    # print(train_data)
    img, label = train_data[0] # 对__getitem__函数传入参数0
    print(img.shape, label)