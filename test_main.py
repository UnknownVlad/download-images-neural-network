import os

import numpy as np
import tensorflow as tf
from keras import Model
from keras.src.utils import load_img, img_to_array
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.python import keras
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import load_img, img_to_array


# Установка режима динамического выделения памяти на GPU
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


# Функция для загрузки и предобработки изображений
def load_images_from_dir(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img = load_img(os.path.join(directory, filename), target_size=(256, 256))
            img_array = img_to_array(img) / 255.0  # Нормализация значений пикселей
            images.append(img_array)
    return np.array(images)


# Функция для построения модели автокодировщика
def autoencoder_model(input_shape=(256, 256, 3)):
    inputs = Input(shape=input_shape)
    x = Conv2D(64, 3, activation='relu', padding='same')(inputs)
    x = MaxPooling2D(2, padding='same')(x)
    x = Conv2D(32, 3, activation='relu', padding='same')(x)
    encoded = MaxPooling2D(2, padding='same')(x)

    x = Conv2D(32, 3, activation='relu', padding='same')(encoded)
    x = UpSampling2D(2)(x)
    x = Conv2D(64, 3, activation='relu', padding='same')(x)
    x = UpSampling2D(2)(x)
    decoded = Conv2D(3, 3, activation='sigmoid', padding='same')(x)

    autoencoder = Model(inputs, decoded)
    return autoencoder


# Пути к директориям с изображениями
train_dir_with_watermark = 'image_fragments'
train_dir_original = 'image_fragments_watermark'

# Загрузка изображений
train_images_with_watermark = load_images_from_dir(train_dir_with_watermark)
train_images_original = load_images_from_dir(train_dir_original)

# Построение и компиляция модели
autoencoder = autoencoder_model()
autoencoder.compile(optimizer=Adam(), loss='mse')

# Обучение модели
autoencoder.fit(train_images_with_watermark, train_images_original, epochs=10, batch_size=32, validation_split=0.2)

# Сохранение модели
autoencoder.save('autoencoder_model.h5')