import os
import json
from pickletools import unicodestring8
import numpy as np
import tensorflow as tf
from urllib import request
from dataloader import MNIST_inference

def main():
    # load environment variable
    url = os.environ['REST_URL']
    data_path = '/home/agc2022/data'
    
    # define dataloader
    inference_loader = MNIST_inference(file_path = data_path)

    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    for batch,data in enumerate(inference_loader):
        
        # get inference result 
        output = model(data)
        
        # extract label from inference output
        batch_label = [int(np.argmax(sample)) for sample in output]
        batch_answer = {'answer': batch_label}
        
        # apply unicode to str json data
        data = json.dumps(batch_answer).encode('unicode-escape')
        # request ready
        req =  request.Request(url, data=data)
        
        # POST to API server
        resp = request.urlopen(req)
        
        # check POST result
        status = resp.read().decode('utf8')
        if "OK" in status:
            print("batch : "+str(batch+1)+"'s result requests successful!!")

if __name__ == "__main__":
    main()