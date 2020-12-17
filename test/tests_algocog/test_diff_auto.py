import test_diff as td


def main():
    name = "Geisslerlied"
    hop_length = 256
    nb_mfcc = 50
    teta = 0.6
    tempo = 120

    tab_fav_teta = []
    best_teta = teta
    best_hop = hop_length
    best_total = 1

    fichier = open("../results/validations/auto/comparaison" + name + "/data.txt", "w")
    while hop_length < 5000:
        print("HOP_LENGTH = ", hop_length)
        fav_teta = teta
        fav_total = 1
        teta = 0.60
        while teta < 1:
            fichier.write("[INFO] HOP_LENGTH = " + str(hop_length) + " TETA = " + str(teta) + "\n")
            print("TETA = ", teta)
            ns_lines, inf_lines, sup_lines, diff, nb_mat = td.test_diff(name, hop_length, nb_mfcc, teta, tempo)
            # total = diff
            total = 0.05*ns_lines/nb_mat + 0.25*inf_lines/nb_mat + 0.25*sup_lines/nb_mat + 0.45*diff
            if total < fav_total:
                fav_teta = teta
                fav_total = total
            teta = teta + 0.05
            fichier.write("non significant lines = " + str(ns_lines) + "\nmissing lines = " + str(inf_lines) +
                          "\nsupplementary lines = " + str(sup_lines) + "\ndifference = " + str(diff) +
                          "\n===> total = " + str(total) + "\n")

        if fav_total < best_total:
            best_teta = fav_teta
            best_hop = hop_length
            best_total = fav_total

        fav_params = [hop_length, fav_teta]
        tab_fav_teta.append(fav_params)
        hop_length = hop_length*2
        fichier.write("[RESULTS] OPTIMUM PARAMETERS [hop_length, teta]= " + str(fav_params) + "\n")
        fichier.write("\n")

    best_params = [best_hop, best_teta]
    fichier.write("BEST PARAMETERS [hop_length, teta]= " + str(best_params))
    fichier.close()
    return tab_fav_teta, best_params


main()
