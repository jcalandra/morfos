import numpy as np
import librosa
import tensorflow as tf
import 
from tensorflow.keras import layers, models
from scipy.spatial.distance import cdist

# -------------------------
# Paramètres
# -------------------------
sr = 16000             # fréquence d'échantillonnage
frame_duration = 0.250   # 1 seconde par trame
n_mels = 64            # nombre de bins Mel
latent_dim = 64
distance_threshold = 0.05  # seuil pour créer un nouveau cluster

# -------------------------
# Auto-encodeur simple
# -------------------------
input_shape = (n_mels, 64, 1)
encoder_input = layers.Input(shape=input_shape)

x = layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=(2,2))(encoder_input)
x = layers.Conv2D(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
x = layers.Conv2D(128, (3,3), activation='relu', padding='same', strides=(2,2))(x)
x = layers.Flatten()(x)
latent = layers.Dense(latent_dim, name='latent_vector')(x)

encoder = models.Model(encoder_input, latent, name='encoder')

decoder_input = layers.Input(shape=(latent_dim,))
x = layers.Dense((8*8*128), activation='relu')(decoder_input)
x = layers.Reshape((8,8,128))(x)
x = layers.Conv2DTranspose(128, (3,3), activation='relu', padding='same', strides=(2,2))(x)
x = layers.Conv2DTranspose(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
x = layers.Conv2DTranspose(32, (3,3), activation='relu', padding='same', strides=(2,2))(x)
decoder_output = layers.Conv2D(1, (3,3), activation='sigmoid', padding='same')(x)

decoder = models.Model(decoder_input, decoder_output, name='decoder')

autoencoder_input = encoder_input
encoded = encoder(autoencoder_input)
decoded = decoder(encoded)
autoencoder = models.Model(autoencoder_input, decoded)
autoencoder.compile(optimizer='adam', loss='mse')

# -------------------------
# Fonction pour extraire mel spectrogramme
# -------------------------
def extract_mel_spectrogram(audio, sr=16000, n_mels=64, n_fft=1024, hop_length=256):
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    log_S = librosa.power_to_db(S, ref=np.max)
    log_S = log_S / 80.0 + 1.0  # normalisation [0,1]
    if log_S.shape[1] < 64:
        log_S = np.pad(log_S, ((0,0),(0,64-log_S.shape[1])), mode='constant')
    else:
        log_S = log_S[:, :64]
    return log_S[..., np.newaxis]  # shape = (n_mels, 64, 1)

# -------------------------
# Initialisation du clustering incrémental
# -------------------------
clusters = []   # liste de clusters, chaque cluster = dict avec 'centroid' et 'members'
all_labels = [] # label assigné à chaque trame

# -------------------------
# Traitement audio fichier (ou flux micro)
# -------------------------
audio, sr = librosa.load("ML/sonate-au-clair-de-lune-allegretto.wav", sr=sr)
frame_length = int(sr * frame_duration)

for start in range(0, len(audio), frame_length):
    frame = audio[start:start+frame_length]
    if len(frame) < frame_length:
        frame = np.pad(frame, (0, frame_length-len(frame)), mode='constant')
    
    mel = extract_mel_spectrogram(frame)
    mel = np.expand_dims(mel, axis=0)
    
    latent_vec = encoder.predict(mel)[0]  # shape=(latent_dim,)
    
    # Si aucun cluster existant → créer le premier
    if len(clusters) == 0:
        clusters.append({'centroid': latent_vec, 'members': [latent_vec]})
        all_labels.append(0)
        continue
    
    # Calculer distance à tous les centroïdes
    centroids = np.array([c['centroid'] for c in clusters])
    distances = cdist([latent_vec], centroids, metric='euclidean')[0]
    
    min_idx = np.argmin(distances)
    if distances[min_idx] < distance_threshold:
        # Ajouter au cluster existant
        clusters[min_idx]['members'].append(latent_vec)
        # Mettre à jour le centroïde
        clusters[min_idx]['centroid'] = np.mean(clusters[min_idx]['members'], axis=0)
        all_labels.append(min_idx)
    else:
        # Créer un nouveau cluster
        new_idx = len(clusters)
        clusters.append({'centroid': latent_vec, 'members': [latent_vec]})
        all_labels.append(new_idx)

# -------------------------
# Résultat final
# -------------------------
print("Nombre de clusters détectés :", len(clusters))
print("Labels assignés par trame :", all_labels)
