import tensorflow as tf
import numpy as np
import datasets

# to_grayscale_tf = lambda x:{'image' : tf.expand_dims(tf.image.rgb_to_grayscale(tf.cast(x['image'], dtype=tf.uint8)), axis=-1)}

to_grayscale_pillow_np = lambda x:{'image' : np.expand_dims(np.asarray(x['image'].convert("L"), dtype=np.uint8), axis=-1)}


train_ds = datasets.load_dataset("project-sloth/captcha-images", split='train')

# train_dsp = train_ds.with_format("tf").map(to_grayscale_tf)

train_dsp = train_ds.map(to_grayscale_pillow_np)


print(train_dsp[0]['image'].shape) # Expecting (50,200,1)

