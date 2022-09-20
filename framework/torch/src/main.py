import os
import torch
from model import linear_model
from inference import inference
from torchvision import transforms
from dataloader import MNIST_inference



def main():
    # load environment variable
    api_url = os.environ['REST_URL']
    data_path = '/home/agc2022/data'
    
    # inference data loader define
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize(( 0.5), (0.5))])
    
    # load inference set & inference loader
    inference_set = MNIST_inference(data_dir = data_path, transform = transform)
    inference_loader =torch.utils.data.DataLoader(inference_set, batch_size=10,shuffle=False,num_workers=1)

    # define device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device : "+ str(device))
    
    # model weight load
    model = linear_model()
    model.load_state_dict(torch.load('./my_model/mnist_net.pth', map_location=device))

    # model result
    inference(model=model, inference_data= inference_loader,device=device,url=api_url)

if __name__ == "__main__":
    main()