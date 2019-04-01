# Import Dependencies
import matplotlib.pyplot as plt
#%matplotlib inline

import os
import numpy as np
import tensorflow as tf

import keras
from keras.preprocessing import image
from keras.applications.vgg19 import (
    VGG19, 
    preprocess_input, 
    decode_predictions
)

from keras import backend as K


# Refactor above steps into reusable function
def predict(image_path):
    """Use VGG19 to label image"""
    # Load the VGG19 model
    # https://keras.io/applications/#VGG19
    model = VGG19(include_top=True, weights='imagenet')

    # Define default image size for VGG19
    image_size = (224, 224)
    img = image.load_img(image_path, target_size=image_size)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    prediction = model.predict(x)
    predictions = decode_predictions(prediction, top=1)[0]
    predicted = predictions[0][1]
    print('Predicted:', predicted)
    predicted_clean = predicted.replace('_',' ')
    #https://github.com/RasaHQ/rasa_nlu/issues/3102
    K.clear_session()
    if (predicted_clean == 'Siamese cat'):
        predicted_clean = 'Siamese'
    return predicted_clean

# image_path = os.path.join("Images","NotDog.jpg")
# predict(image_path)

