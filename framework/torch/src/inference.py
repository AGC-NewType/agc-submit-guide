import time
import json
import torch
from tqdm import tqdm
from urllib import request

def inference(model, inference_data, device, url):
    # set inference mode
    model.eval()
    
    # attach device to model ['cpu','cuda']
    model.to(device)

    with torch.no_grad():
        # set progressbar with tqdm & return batch:int, img:torch.tensor by enumerate
        for batch, img in tqdm(enumerate(inference_data)):

            # define answer template per batch
            template = {
                "team_id": "userxx",
                "secret": "!@#$%^&*()",
                "answer_sheet": {}
            }
                
            # attach device to tensor
            img=img.to(device)
            
            # get inference result
            output = model(img)
            
            ## set sigmoid to final layer output
            output = torch.sigmoid(output)
            probability, argmax = torch.max(output, 1)
            batch_label = argmax.tolist()

            # define tmp_answer for append to json_data['answer_sheet']:dict
            tmp_answer = {"no":str(batch+1), "answer" : str(batch_label[0])}
            template['answer_sheet'] = tmp_answer


            # apply utf-8 to str json data
            data = json.dumps(template).encode('utf-8')
            
            # request ready
            req =  request.Request(url, data=data)
            
            # POST to API server
            resp = request.urlopen(req)
            
            # # check POST result
            resp_json = eval(resp.read().decode('utf-8'))
            print("received message: "+resp_json['msg'])

            if "OK" == resp_json['status']:
                print("data requests successful!!")
            elif "ERROR" == resp_json['status']:    
                raise ValueError("Receive ERROR status. Please check your source code.")    