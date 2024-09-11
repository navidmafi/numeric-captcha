from matplotlib import pyplot as plt
import tensorflow as tf


def decode_img(img: tf.Tensor) -> tf.Tensor:
  return tf.io.decode_image(img,channels=1, dtype=tf.float32, expand_animations = False) # type: ignore

def preprocess_image(image:tf.Tensor) -> tf.Tensor:
  # tf.print(tf.shape(image))
  image = tf.image.resize(image, image_shape[:2])
  image = tf.image.per_image_standardization(image)
  return image

def label_to_one_hot_2d(label:tf.Tensor) -> tf.Tensor:
    digits = tf.strings.to_number(tf.strings.unicode_split(label, 'UTF-8'), out_type=tf.int32)
    one_hot_digits = tf.one_hot(digits, depth=10)
    return one_hot_digits


def preprocess_label(label : tf.Tensor) -> tf.Tensor:
  return label_to_one_hot_2d(label)


def get_shape(ds:tf.data.Dataset):
    for image, label in ds.unbatch().take(1): # type: ignore
        tf.print("image:")
        tf.print(tf.shape(image))
        tf.print(image.dtype)
        tf.print("label:")
        tf.print(tf.shape(label))
        tf.print(label.dtype)
        # print("Single label:", label.numpy())

def decode_one_hot(one_hot_label: tf.Tensor) ->  tf.Tensor:
    one_hot_reshaped = tf.reshape(one_hot_label, [code_length, charset_length])
    digits = tf.argmax(one_hot_reshaped, axis=-1)
    return tf.strings.reduce_join(tf.strings.as_string(digits), axis=0)
    

def decode_one_hot_2dim(one_hot_label : tf.Tensor) ->  tf.Tensor:
    one_hot_reshaped = tf.reshape(one_hot_label, [code_length, charset_length])
    return tf.argmax(one_hot_reshaped, axis=1)


def viz_ds(ds:tf.data.Dataset, count=6):
    plt.figure()
    ds= ds.unbatch().take(count)
    dsit = iter(ds)
    for i in range(count):
        image, label  = next(dsit)  # type: ignore
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(image.numpy().astype("uint8"),cmap="gray")
        if (len(label.numpy().shape) == 2):
             plt.title(decode_one_hot_2dim(label).numpy())
        else:
            plt.title(label.numpy())
            
        plt.tight_layout()
        plt.axis("off")