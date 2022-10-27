import os
import json
import torch
from urllib import request
from model import linear_model
from inference import inference
from torchvision import transforms
from dataloader import MNIST_inference

def main():
    # load environment variable
    api_url = os.environ['REST_ANSWER_URL']
    data_path = '/home/agc2022/dataset/'

    # inference data loader define
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize(( 0.5), (0.5))])
    
    # load inference set & inference loader
    inference_set = MNIST_inference(data_dir = data_path, transform = transform)
    inference_loader =torch.utils.data.DataLoader(inference_set, batch_size=1,shuffle=False,num_workers=1)

    # define device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device : "+ str(device))
    
    # model weight load
    model = linear_model()
    model.load_state_dict(torch.load('./my_model/mnist_net.pth', map_location=device))

    # model result
    inference(model=model, inference_data= inference_loader,device=device,url=api_url)
    
    # request end of mission message
    message_structure = {
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "end_of_mission": "true"
    }

    # json dump & encode utf-8
    tmp_message = json.dumps(message_structure).encode('utf-8')
    request_message = request.Request(api_url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST

    resp_json = eval(resp.read().decode('utf-8'))
    print("received message: "+resp_json['msg'])

    if "OK" == resp_json['status']:
        print("data requests successful!!")
    elif "ERROR" == resp_json['status']:    
        raise ValueError("Receive ERROR status. Please check your source code.")    
    
if __name__ == "__main__":
    main()