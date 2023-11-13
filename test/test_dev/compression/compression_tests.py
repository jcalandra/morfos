from algo_segmentation_mso import fun_segmentation
from data_mso import algo_cog
import compression
import compression_synthesis as com_syn
import time_manager
import parameters as prm

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT


def compute_mso_char(char):
    char_ex = ''
    for c in range(len(char)):
        char_ex += chr(ord(char[c]) - 96)
    data_length = len(char_ex)
    oracles = [-1, []]
    fun_segmentation(oracles, char_ex, data_length)
    mso = oracles[1]
    return mso


def compute_mso(path):
    oracles = [-1, []]
    algo_cog(path, oracles, HOP_LENGTH, NB_VALUES, TETA, INIT)
    mso = oracles[1]
    return mso


def test_compression(mso):
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


def test_compression_encodage(mso):
    lvl_max = len(mso) - 1
    start_time = time_manager.time()
    for j in range(10000):
        compression.nb_materials = [-1 for i in range(lvl_max + 1)]
        compression.encoded_char = []
        t_end = len(mso[lvl_max][0].data)
        compression.encode(lvl_max, mso, fd_str=[], t_start=1, t_end=t_end)
    print("time =", time_manager.time() - start_time)


def test_compression_decodage(mso):
    lvl_max = len(mso) - 1

    compression.nb_materials = [-1 for i in range(lvl_max + 1)]
    compression.encoded_char = []
    t_end = len(mso[lvl_max][0].data)
    compression.encode(lvl_max, mso, fd_str=[], t_start=1, t_end=t_end)
    tmp = compression.encoded_char

    start_time = time_manager.time()
    for j in range(10000):
        compression.encoded_char = tmp
        compression.dictionary = [[] for i in range(lvl_max + 1)]
        compression.formal_diagrams = [[] for i in range(lvl_max + 1)]
        compression.decode(lvl_max)
    print("time =", time_manager.time() - start_time)


def test_compression_repeat(mso):
    lvl_max = len(mso) - 1

    start_time = time_manager.time()
    for j in range(10000):
        compression.nb_materials = [-1 for i in range(lvl_max + 1)]
        compression.encoded_char = []
        t_end = len(mso[lvl_max][0].data)
        compression.encode(lvl_max, mso, fd_str=[], t_start=1, t_end=t_end)

        compression.dictionary = [[] for i in range(lvl_max + 1)]
        compression.formal_diagrams = [[] for i in range(lvl_max + 1)]
        compression.decode(lvl_max)
    print("time =", time_manager.time() - start_time)


def main():
    debussy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 1, 2, 3, 4, 9, 20, 21,
               20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 28, 29, 32, 33, 34, 35, 1, 2, 3, 4, 5, 6, 36, 37, 9, 38,
               39, 9, 39, 40, 1, 39, 40, 41, 42]
    geisslerlied = 'cognitive_algorithm_and_its_musical_applications/data/Geisslerlied/Geisslerlied.wav'
    mozart = 'cognitive_algorithm_and_its_musical_applications/data/Mozart/MozartK545_rondo.wav'
    multi_scale_oracle = compute_mso(geisslerlied)

    for level in range(len(multi_scale_oracle)):
        print(len(multi_scale_oracle[level][0].data))

    test_compression(multi_scale_oracle)
    test_compression_repeat(multi_scale_oracle)
    test_compression_encodage(multi_scale_oracle)
    test_compression_decodage(multi_scale_oracle)
    com_syn.full_synthesis(multi_scale_oracle, geisslerlied)
