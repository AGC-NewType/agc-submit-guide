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
    
    # define template json path
    template_path = '/home/agc2022/data/template.json'

    with torch.no_grad():
        # set progressbar with tqdm & return batch:int, img:torch.tensor by enumerate
        for batch, img in tqdm(enumerate(inference_data)):
            # load answer template
            with open(template_path,"r") as answer_json:
                json_data = json.load(answer_json)
                
            # attach device to tensor
            img=img.to(device)
            
            # get inference result
            output = model(img)
            
            ## set sigmoid to final layer output
            output = torch.sigmoid(output)
            probability, argmax = torch.max(output, 1)
            batch_label = argmax.tolist()

            # define tmp_answer for append to json_data['answer_sheet']:list
            for num,label in enumerate(batch_label):
                tmp_answer = {"no":str(num+1), "answer" : str(label)}
                json_data['answer_sheet'].append(tmp_answer)


            # # apply unicode to str json data
            data = json.dumps(json_data).encode('unicode-escape')
            
            # # request ready
            req =  request.Request(url, data=data)
            
            # # POST to API server
            resp = request.urlopen(req)
            
            # # check POST result
            status = resp.read().decode('utf8')
            if "OK" in status:
                print("batch : "+str(batch+1)+"'s result requests successful!!")