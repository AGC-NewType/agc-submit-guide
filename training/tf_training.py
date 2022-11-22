import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets
from tensorflow.keras.utils import to_categorical
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

mnist = datasets.mnist
(train_x, train_y), (test_x, test_y) = mnist.load_data()

model = tf.keras.Sequential()

model.add(tf.keras.layers.Flatten(input_shape=(28,28)))
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dense(10,activation='softmax'))

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
model.summary()

hist = model.fit(train_x, train_y, epochs=30, validation_split=0.3)
model.evaluate(test_x, test_y)

model.save('./my_model/mnist.h5')
model.save_weights('./my_model/epoch_001')