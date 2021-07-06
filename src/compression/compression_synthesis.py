import numpy as np
import parameters as prm
import scipy.io.wavfile as wave
import compression
from signal_mso import algo_cog
import data_computing as dc

hop_size = prm.HOP_LENGTH
sr = prm.SR


def compute_mso(path):
    oracles = [-1, []]
    algo_cog(path, oracles, hop_size, prm.NB_VALUES, prm.TETA, prm.INIT)
    mso = oracles[1]
    return mso


def compute_data(path):
    data, rate, data_size, data_length = dc.get_data(path)
    nb_points = prm.NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    return data


def re_synthesis(mso, formal_diagrams, name, data):
    wave.write(name + "_verification.wav", sr, data)
    final_name = name + '_compression_synthesis.wav'
    print(final_name)
    new_y = np.array([])
    for i in range(1, len(formal_diagrams[0])):
        latent = mso[0][0].latent[formal_diagrams[0][i]]
        sound = data[latent[1]*hop_size:(latent[1] + 1)*hop_size]
        new_y = np.concatenate((new_y, sound))
    wave.write(final_name, sr, new_y)


def levelup_synthesis(mso, formal_diagrams, name, data):
    wave.write(name + "_verification.wav", sr, data)
    for j in len(mso):
        final_name = name + str(j) + '_compression_synthesis.wav'
        new_y = np.array([])
        for i in range(1, len(formal_diagrams[0])):
            latent = mso[j][0].latent[formal_diagrams[0][i]]
            sound = data[latent[1] * hop_size:(latent[1] + 1) * hop_size]
            new_y = np.concatenate((new_y, sound))
        wave.write(final_name, sr, new_y)


def full_synthesis(mso, path):
    lvl_max = len(mso) - 1
    compression.nb_materials = [-1 for i in range(lvl_max + 1)]
    compression.encoded_char = []
    t_end = len(mso[lvl_max][0].data)

    compression.encode(lvl_max, mso, fd_str=[], t_start=1, t_end=t_end)
    print(compression.encoded_char)

    compression.dictionary = [[] for i in range(lvl_max + 1)]
    compression.formal_diagrams = [[] for i in range(lvl_max + 1)]
    compression.decode(lvl_max)
    print(compression.dictionary)
    print(compression.formal_diagrams)

    data = compute_data(path)
    name = path.split('.')[0]
    re_synthesis(mso, compression.formal_diagrams, name, data)


def main():
    path = 'cognitive_algorithm_and_its_musical_applications/data/Geisslerlied/Geisslerlied.wav'
    # path = 'cognitive_algorithm_and_its_musical_applications/data/Mozart/MozartK545_rondo.wav'
    mso = compute_mso(path)
    full_synthesis(mso, path)
