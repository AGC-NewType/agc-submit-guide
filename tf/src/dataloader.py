import math
import numpy as np 
from glob import glob
import tensorflow as tf
from tensorflow.keras.utils import Sequence

class MNIST(Sequence):
    def __init__(self, file_path, batch_size=10, shuffle=False):
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.file_path = glob(file_path+ "/**/**.png")
        
    def __len__(self):
        return math.ceil(len(self.file_path)//self.batch_size)
    
    def decode(self,file):
        img = img = tf.io.read_file(file)
        img = tf.io.decode_image(img, channels=1, dtype=tf.dtypes.float32)
        img = np.resize(img, (28,28))
        return img

    def __getitem__(self, idx):
        file_batch = self.file_path[idx*self.batch_size:(idx+1)*self.batch_size]
        batch_img = [self.decode(img) for img in file_batch]
        return np.array(batch_img) 

if __name__ == '__main__':
    dir = "C:/Users/bomeb/jh/agc-submit-guide/mnist_inference"
    testloader = MNIST(file_path = dir)
    for img in testloader:
        print(img)
        