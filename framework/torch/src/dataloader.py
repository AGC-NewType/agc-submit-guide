from glob import glob  # for open lots of file
from PIL import Image  # for open image file
from torch.utils.data.dataset import Dataset  # for custom dataloader

class MNIST_inference(Dataset):

    def __init__(self, data_dir, transform):
        self.data_dir = glob(data_dir + "/**/**.png")
        self.transform = transform

    def __len__(self):
        return len(self.data_dir)

    def __getitem__(self, idx):
        filepath = self.data_dir[idx]
        img = Image.open(filepath)
        if self.transform:
            img = self.transform(img)
        return img