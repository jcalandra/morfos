from data_processing import blue_value


def clicks_per_song(data):
    clicks = [[] for i in range(len(data[0][3])//2)]
    for sujet in data:
        for c in range(len(sujet[3])):
            if c%2 == 0:
                couple = [sujet[3][c], sujet[3][c + 1]]
                clicks[c//2].append(couple)
    return clicks


def mean_click_sujet(data):
    mean_click = []
    for sujet in data:
        sujet_click = []
        for c in range(len(sujet[3])):
            if c%2 == 0:
                sum_n = 0
                sum_t = 0
                for i in range(len(sujet[3][c])):
                    if sujet[3][c][i] != blue_value:
                        sum_n += sujet[3][c][i]
                        sum_t += sujet[3][c + 1][i]
                sujet_click.append(sum_t/sum_n)
        mean_click.append(sujet_click)
    print(mean_click)
    return mean_click


def mean_click(mc_sujet):
    means = [0 for i in range(len(mc_sujet[0]))]
    for i in range(len(mc_sujet)):
        for k in range(len(mc_sujet[i])):
            means[k] = means[k] + mc_sujet[i][k]/len(mc_sujet)
    print(means)


def mean_nasatlx(data):
    return
