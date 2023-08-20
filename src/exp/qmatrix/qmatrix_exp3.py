import main_mso
import parameters


def main():
    for song in range(1,101):
        if song < 10:
            number = '0' + str(song)
        else:
            number = str(song)
        path = "C:/Users/jmoca/OneDrive/Documents/Travail/These/Programmation/" \
               "cognitive_algorithm_and_its_musical_applications/data/qmatrix/Qmatrix_song"+ str(song) + ".npy"
        result_path = parameters.project_root + '/results/qmatrix/exp2/rwcpop/Pop ' + number + '/'
        main_mso.main(path, result_path)

# main()
