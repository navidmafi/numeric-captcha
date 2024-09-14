import keras
import tensorflow as tf

class PerImageStandardizationLayer(keras.layers.Layer):
    def call(self, inputs):
        return tf.image.per_image_standardization(inputs)