import sys
from pathlib import Path

file = Path(__file__).resolve()
project_root = str(file.parents[1])
src_path = project_root
sys.path.append(src_path)
import paths

import module_parameters.parameters as prm
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import librosa
from scipy.spatial.distance import euclidean

#================================================================================================================================================
# classification model
#================================================================================================================================================
def param_to_latent_space(n_mels=128, latent_dim=128):
    sr = prm.SR #16000
    frame_duration = 1.0   # duration of the concatenated frames in the lower level
    input_shape = (n_mels, 128, 1)
    change_threshold = 1-prm.d_threshold
    return input_shape, latent_dim, change_threshold, sr, frame_duration


def build_classification_model(input_shape, latent_dim, change_threshold):
    # -------------------------
    # Encoder
    # -------------------------
    encoder_input = layers.Input(shape=input_shape)

    x = layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=(2,2))(encoder_input)
    x = layers.Conv2D(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Conv2D(128, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Flatten()(x)
    latent = layers.Dense(latent_dim, name='latent_vector')(x)

    encoder = models.Model(encoder_input, latent, name='encoder')
    encoder.summary()

    # -------------------------
    # Decoder
    # -------------------------
    decoder_input = layers.Input(shape=(latent_dim,))
    x = layers.Dense((16*16*128), activation='relu')(decoder_input)
    x = layers.Reshape((16,16,128))(x)
    x = layers.Conv2DTranspose(128, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Conv2DTranspose(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Conv2DTranspose(32, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    decoder_output = layers.Conv2D(1, (3,3), activation='sigmoid', padding='same')(x)

    decoder = models.Model(decoder_input, decoder_output, name='decoder')
    decoder.summary()

    # -------------------------
    # Autoencoder
    # -------------------------
    autoencoder_input = encoder_input
    encoded = encoder(autoencoder_input)
    decoded = decoder(encoded)

    autoencoder = models.Model(autoencoder_input, decoded, name='autoencoder')
    autoencoder.compile(optimizer='adam', loss='mse')

    autoencoder.summary()
    return autoencoder, encoder, decoder
#================================================================================================================================================
# segmentation model
#================================================================================================================================================

# -------------------------
# Paramètres
# -------------------------
def build_segmentation_model(input_shape, latent_dim):
    # -------------------------
    # Auto-encodeur CNN simple
    # -------------------------
    encoder_input = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=(2,2))(encoder_input)
    x = layers.Conv2D(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Flatten()(x)
    latent = layers.Dense(latent_dim, name='latent_vector')(x)
    encoder = models.Model(encoder_input, latent)
    return encoder

def build_models():
    input_shape, latent_dim, change_threshold, sr, frame_duration  = param_to_latent_space(128, 128)
    autoencoder, encoder, decoder = build_classification_model(input_shape, latent_dim, change_threshold)
    egmentation_encoder = build_segmentation_model(input_shape, latent_dim)
    return autoencoder, encoder, decoder, segmentation_encoder, sr, frame_duration

build_models()

