import numpy as np
import scipy.io.wavfile as wave

# In this file are found fonctions to reecreate the audio from an oracle


# ================================================ SYNTHESIS ===========================================================
def synthesis_data(ms_oracle, level, nb_hop, hop_size):
    """ Create an audio tab from the oracle 'oracle_t'. """
    new_y = np.array([])
    print(len(ms_oracle.audio))
    for i in range(1, nb_hop):
        latent = ms_oracle.levels[level].oracle.latent[int(ms_oracle.levels[level].oracle.data[i])]
        sound = ms_oracle.audio[latent[1]*hop_size:(latent[1] + 1)*hop_size]
        new_y = np.concatenate((new_y, sound))
    return new_y


def synthesis_wav(new_y, sr, name):
    """ Write an tab corresponding to audio in a .wav file."""
    wave.write(name, sr, new_y)


def synthesis(ms_oracle, level, nb_hop, hop_size):
    """ Create an audio tab from the oracle 'oracle_t' and write the audio in a .wav file called 'name'."""
    new_y = synthesis_data(ms_oracle, level, nb_hop, hop_size)
    synthesis_wav(new_y, ms_oracle.rate, ms_oracle.name + "synthesis.wav")
