import datasets
import numpy as np
datasets.disable_caching()

ds = datasets.load_dataset("project-sloth/captcha-images")


# to_grayscale_pillow = lambda x : {'image' :np.expand_dims(np.array(x['image'].convert("L")).astype(np.uint8), axis=2).astype(np.uint8)}


ds.map(to_grayscale_pillow, num_proc=10) # type: ignore

ds.save_to_disk("captcha-gs") # type: ignore
