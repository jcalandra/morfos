import numpy as np
import scipy.io.wavfile as wave


def synthesis_data(oracle_t, nb_hop, data, hop_size):
    new_y = np.array([])
    for i in range(1, nb_hop):
        latent = oracle_t.latent[int(oracle_t.data[i])]
        sound = data[latent[0]*hop_size:(latent[0] + 1)*hop_size]
        new_y = np.concatenate((new_y, sound))
    return new_y


def synthesis_wav(new_y, sr, name):
    wave.write(name, sr, new_y)


def synthesis(oracle_t, nb_hop, data, hop_size, sr, name):
    new_y = synthesis_data(oracle_t, nb_hop, data, hop_size)
    synthesis_wav(new_y, sr, name)
