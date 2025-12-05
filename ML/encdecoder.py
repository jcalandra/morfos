import tensorflow as tf
from tensorflow.keras import layers, models

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

# -------------------------
# Exemple d'entraînement
# -------------------------
# X_train : tableau numpy de spectrogrammes de forme (N, 128, 128, 1)
# autoencoder.fit(X_train, X_train, epochs=50, batch_size=32)

embeddings = encoder.predict(X_new)