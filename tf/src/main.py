import os
import json
import numpy as np
import tensorflow as tf
from urllib import request
from dataloader import MNIST_inference

def main():
    # load environment variable
    url = os.environ['REST_URL']
    data_path = os.environ['DATA_PATH']
    headers = os.environ['API_HEADER']

    # define dataloader
    inference_loader = MNIST_inference(file_path = data_path)

    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    model.evaluate(inference_loader)
    result = model.predict(inference_loader)

    # model result request
    answer = [int(np.argmax(sample)) for sample in result]
    answer_dict = {'answer' : answer}
    data = json.dumps(answer_dict).encode('utf8')

    # request result to API
    req =  request.Request(url, data=data, headers=headers)
    resp = request.urlopen(req)
    print(resp.read().decode('utf8'))

if __name__ == "__main__":
    main()