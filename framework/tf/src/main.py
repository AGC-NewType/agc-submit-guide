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
            "hash": "!@#$%^&*()",
            "report_no": "001",
            "report_part": str(batch),
            "answer": {}
        }
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        tmp_answer = {"no":str(batch+1), "answer" : str(batch_label[0])}
        template['answer'] = tmp_answer
        
        # apply utf-8 to str json data
        data = json.dumps(template).encode('utf-8')

        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        resp_json = eval(resp.read().decode('utf-8'))

        if "OK" == resp_json['status']:
            print("data requests successful!!")
        elif "ERROR" == resp_json['status']:    
            received_message=resp_json['msg']
            raise ValueError(received_message)   

    # request end of mission message
    message_structure = {
    "team_id": "userxx",
    "hash": "!@#$%^&*()",
    "end_of_mission": "true"
    }

    # json dump & encode utf-8
    tmp_message = json.dumps(message_structure).encode('utf-8')
    request_message = request.Request(api_url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST

    resp_json = eval(resp.read().decode('utf-8'))
    
    if "OK" == resp_json['status']:
        print("data requests successful!!")
    elif "ERROR" == resp_json['status']:    
        received_message=resp_json['msg']
        raise ValueError(received_message)     
    
if __name__ == "__main__":
    main()
