import silence_tensorflow.auto
import tensorflow as tf
gpuDevices = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(gpuDevices))
tf.config.experimental.set_memory_growth(gpuDevices[0], True)
tf.config.optimizer.set_experimental_options({'layout_optimizer': False})

import keras
import os, sys, random, glob, time, logging
from PIL import Image

import transformers
from IPython import display
import datasets
datasets.disable_caching()
import matplotlib.pyplot as plt
import numpy as np


ts = lambda tensor : keras.preprocessing.image.array_to_img(tensor)

def plot_n_samples(dataset, n ):
    plt.figure(figsize=(20, 4))
    for i in range(n):
        assert tf.is_tensor(dataset[i]), "This ain't a tensor"
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(ts(dataset[i].numpy()))
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()
    
    
def to_gray(dp):
    img_array = np.asarray(dp['image'].convert("L"))
    img_array = img_array[...,None].astype(dtype=int, copy=False)
    dp['image'] = img_array
    return dp
    
    
train_ds = datasets.load_dataset("project-sloth/captcha-images", split='train')


datasets.logging.set_verbosity_debug()

train_dsp = train_ds.map(to_gray,keep_in_memory=True, remove_columns = ["solution"], writer_batch_size=2)

print(train_dsp['image'][0].shape)