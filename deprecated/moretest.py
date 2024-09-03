import tensorflow as tf
from datasets import load_dataset

dataset = load_dataset("project-sloth/captcha-images")

# Function to convert an RGB image to grayscale and reshape
def process_image(example):
    image = example['image']
    # Convert to grayscale
    grayscale_image = tf.image.rgb_to_grayscale(image)
    # Ensure the shape is (height, width, 1)
    grayscale_image = tf.reshape(grayscale_image, (grayscale_image.shape[0], grayscale_image.shape[1], 1))
    example['image'] = grayscale_image
    return example

# Apply the transformation to the dataset
processed_dataset = dataset.map(process_image, batched=False)

# Convert to TensorFlow dataset if needed
tf_dataset = processed_dataset.with_format("tensorflow")
print(tf_dataset[0]['image'])