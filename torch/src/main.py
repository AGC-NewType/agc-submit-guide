import os
import json
import torch
import requests
from torchvision import transforms
from dataloader import MNIST_inference
from inference import inference
from model import linear_model

def main():
    url = 'http://'+ os.environ['REST_URL'] + ':30000'
    
    data_path = os.environ['DATA_PATH']
    
    # inference data loader define
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize(( 0.5), (0.5))])
    inference_loader = MNIST_inference(data_dir = data_path, transform = transform)

    # model weight load
    model = linear_model()
    model.load_state_dict(torch.load('./my_model/mnist_net.pth'))

    # model result
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")            
    answer=inference(model=model, inference_data= inference_loader,device=device)
    answer_dict = {'answer' : answer}
    data = json.dumps(answer_dict)
    
    # request result to API
    response = requests.post(url, data=data)
    print("response: ", response)
    print("response.text: ", response.text)

if __name__ == "__main__":
    main()