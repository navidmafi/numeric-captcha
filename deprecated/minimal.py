import numpy as np
import tensorflow as tf
import datasets
print(datasets.version.Version)
ds = datasets.load_dataset("project-sloth/captcha-images").with_format("tensorflow")


to_gray = lambda sample: {'image': np.expand_dims(sample['image'].convert("L"), axis=-1)}
# ds_gray = ds.map(to_gray)