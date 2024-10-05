import tensorflow as tf
import pandas as pd
from tensorflow.keras.layers import TextVectorization

model_path = 'toxicity3e.h5'
model = tf.keras.models.load_model(model_path)

df = pd.read_csv('train.csv')

MAX_FEATURES = 200000
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=1800,
                               output_mode='int')
