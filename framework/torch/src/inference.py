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
            # attach device to tensor
            img=img.to(device)
            
            # get inference result
            output = model(img)
            
            ## set sigmoid to final layer output
            output = torch.sigmoid(output)
            probability, argmax = torch.max(output, 1)
            batch_label = argmax.tolist()
            batch_answer = {'answer' : batch_label}
            
            # # apply unicode to str json data
            data = json.dumps(batch_answer).encode('unicode-escape')
            
            # # request ready
            req =  request.Request(url, data=data)
            
            # # POST to API server
            resp = request.urlopen(req)
            
            # # check POST result
            status = resp.read().decode('utf8')
            if "OK" in status:
                print("batch : "+str(batch+1)+"'s result requests successful!!")