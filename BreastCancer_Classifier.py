import cv2
import numpy as np
from keras.models import load_model
from PIL import ImageGrab,ImageOps,Image

# Load the model
model = load_model('.\Dataset\keras_model.h5')
labels = open('.\Dataset\labels.txt', 'r').readlines()
def classifiy(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (750, 480))   
    img = cv2.resize(img,(224,224),interpolation=cv2.INTER_AREA)
    img = np.asarray(img,dtype=np.float32).reshape(1,224,224,3) 
    img=(img/127.5)-1
    prediction = model.predict(img)
    index =np.argmax(prediction)
    class_name = labels[index]
    print("classname",class_name)
    return class_name
    # Print what the highest value probabilitie label
    # print(labels[np.argmax(probabilities)])
    # Listen to the keyboard for presses.
# 27 is the ASCII for the esc key on your keyboard.

