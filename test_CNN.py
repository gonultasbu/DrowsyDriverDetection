from keras.models import load_model
import numpy as np
import cv2
import os

model = load_model('DDD_model.h5')

im = cv2.imread("bmg.jpg")
im = np.dot(np.array(im, dtype='float32'), [[0.2989], [0.5870], [0.1140]]) / 255
im = np.expand_dims(im, axis=0)
im = im.reshape((im.shape[0], im.shape[3]) + im.shape[1:3])
print (model.predict(im, batch_size=32, verbose=0, steps=None))
