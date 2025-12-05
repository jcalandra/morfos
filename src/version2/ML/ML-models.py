import module_parameters.parameters as prm
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import librosa
from scipy.spatial.distance import euclidean

#================================================================================================================================================
# classification model
#================================================================================================================================================


def build_classification_autoencoder():
    # -------------------------
    # Paramètres
    # -------------------------
    input_shape = (128, 128, 1)  # Exemple : 128 mel bins x 128 frames
    latent_dim = 64              # Dimension du vecteur latent

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
def build_segmentation_autoencoder():
    sr = prm.SR #16000
    frame_duration = 1.0   # duration of the concatenated frames in the lower level
    n_mels = 64
    latent_dim = 64
    change_threshold = 1-prm.d_threshold  # seuil pour détecter un changement de segment

    # -------------------------
    # Auto-encodeur CNN simple
    # -------------------------
    input_shape = (n_mels, 64, 1)
    encoder_input = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=(2,2))(encoder_input)
    x = layers.Conv2D(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
    x = layers.Flatten()(x)
    latent = layers.Dense(latent_dim, name='latent_vector')(x)
    encoder = models.Model(encoder_input, latent)
    return encoder