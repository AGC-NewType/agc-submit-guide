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


if __name__ == "__main__":
    from torchvision.transforms import transforms
    from torch.utils.data.dataloader import DataLoader

    dir = "C:/Users/bomeb/jh/agc-submit-guide/mnist_inference"
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor()
    ])

    inference = MNIST_inference(data_dir=dir, transform=transform)
    inference_loader = DataLoader(inference, batch_size=2, shuffle=True, num_workers=0)
    
    for img, label in inference_loader:
        print(img)
        import sys;
        sys.exit(0)