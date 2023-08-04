import oracle_mso
import formal_diagram_mso as fd_mso

# The function that initialize the Multi_Scale Oracle is defined in this file


# ============================================ MULTI-SCALED ORACLE =====================================================
def structure_init(flag, level, dim=1):
    """Initialize the Multi-Scale Oracle."""
    f_oracle = oracle_mso.create_oracle(flag, dim=dim)
    link = [0]
    history_next = []
    concat_obj = ''
    formal_diagram = []
    formal_diagram_graph = fd_mso.print_formal_diagram_init(level)
    matrix = ["", []]
    return f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix
