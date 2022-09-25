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
    data_path = '/home/agc2022/data/'
    
    # define dataloader
    inference_loader = MNIST_inference(file_path = data_path)

    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    
    # define template json path
    template_path = '/home/agc2022/data/template.json'
    
    for batch,data in enumerate(inference_loader):
        # load answer template
        with open(template_path,"r") as answer_json:
            json_data = json.load(answer_json)
                
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]

        # define tmp_answer for append to json_data['answer_sheet']:list
        for num,label in enumerate(batch_label):
            tmp_answer = {"no":str(num+1), "answer" : str(label)}
            json_data['answer_sheet'].append(tmp_answer)

        
        # apply unicode to str json data
        data = json.dumps(json_data).encode('unicode-escape')
        # request ready
        req =  request.Request(api_url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        status = resp.read().decode('utf8')
        if "OK" in status:
            print("batch : "+str(batch+1)+"'s result requests successful!!")

    # request end of mission message
    message_structure = {
    "team_id": "convai",
    "secret": "3dlZhXRPPyt22tR9",
    "end_of_mission": "true"
    }

    # json dump & encode unicode
    tmp_message = json.dumps(message_structure).encode('unicode-escape')
    request_message = request.Request(url, data=tmp_message) 
    resp = request.urlopen(request_message) # POST
    
if __name__ == "__main__":
    main()