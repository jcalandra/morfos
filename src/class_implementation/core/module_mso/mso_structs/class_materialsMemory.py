class Materials:
    def __init__(self):
        self.history = []
        self.sim_matrix = SimMatrix()

    def update_history(self, rep, concat_obj):
        self.history.append([rep, concat_obj])

    def update(self, rep, concat_obj, sim_tab):
        self.update_history(rep, concat_obj)
        self.sim_matrix.update(rep.char, sim_tab)


class SimMatrix:
    def __init__(self):
        self.labels = ""
        self.values = []

    def init(self, label, vec):
        self.labels = label
        self.values = [vec]

    def update(self, new_char, sim_tab):
        self.labels += new_char
        self.values.append(sim_tab.copy())
        for i in range(len(self.values - 1)):
            self.values.append(self.values[len(self.values[1]) - 1][i])