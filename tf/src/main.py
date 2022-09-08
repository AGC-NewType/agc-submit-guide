import os
import json
import requests
import numpy as np
import tensorflow as tf
from dataloader import MNIST

def main():
    url = os.environ['REST_URL']
    
    data_path = os.environ['DATA_PATH']
    inference_loader = MNIST(file_path = data_path)

    # model load & predict
    model = tf.keras.models.load_model("./my_model")
    model.evaluate(inference_loader)
    result = model.predict(inference_loader)

    # model result request
    answer = [int(np.argmax(sample)) for sample in result]
    answer_dict = {'answer' : answer}
    data = json.dumps(answer_dict)
    response = requests.post(url, data=data)
    print("response: ", response)
    print("response.text: ", response.text)

if __name__ == "__main__":
    main()