import oracle_mso
import formal_diagram_mso as fd_mso


# ============================================ MULTI-SCALED ORACLE =====================================================
def structure_init(flag, level):
    # TODO : faire une version objet
    f_oracle = oracle_mso.create_oracle(flag)
    link = [0]
    history_next = []
    concat_obj = ''
    formal_diagram = []
    formal_diagram_graph = fd_mso.print_formal_diagram_init(level)
    matrix = ["", []]
    return f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix