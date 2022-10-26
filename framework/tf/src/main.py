import os
import time
import json
from pickletools import unicodestring8
import numpy as np
import tensorflow as tf
from urllib import request
from dataloader import MNIST_inference

def main():
    # load environment variable
    api_url = os.environ['REST_ANSWER_URL']
    data_path = '/home/agc2022/dataset/'

    # define dataloader
    inference_loader = MNIST_inference(file_path = data_path, batch_size=1)

    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    
    for batch,data in enumerate(inference_loader):        
        # define answer template per batch
        template = {
            "team_id": "userxx",
            "secret": "!@#$%^&*()",
            "answer_sheet": {}
        }
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        tmp_answer = {"no":str(batch+1), "answer" : str(batch_label[0])}
        template['answer_sheet'] = tmp_answer
        
        # apply unicode to str json data
        data = json.dumps(template).encode('unicode-escape')

        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        status = eval(resp.read().decode('utf8'))
        print("received message: "+status['msg'])

        if "OK" == status['result']:
            print("data requests successful!!")
        elif "ERROR" == status['result']:    
            raise ValueError("Receive ERROR status. Please check your source code.")    

    # request end of mission message
    message_structure = {
    "team_id": "userxx",
    "secret": "!@#$%^&*()",
    "end_of_mission": "true"
    }

    # json dump & encode unicode
    tmp_message = json.dumps(message_structure).encode('unicode-escape')
    request_message = request.Request(api_url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST

    status = eval(resp.read().decode('utf8'))
    print("received message: "+status['msg'])

    if "OK" == status['result']:
        print("data requests successful!!")
    elif "ERROR" == status['result']:    
        raise ValueError("Receive ERROR status. Please check your source code.")    
    
if __name__ == "__main__":
    main()
