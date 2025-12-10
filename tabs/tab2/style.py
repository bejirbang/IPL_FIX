# Warna fase
FASE_COLORS = {
    "Perencanaan & Konseptual": "#48cae4",
    "Rilis (Go Live)": "#00b4d8",
    "Pertumbuhan": "#0096c7",
    "Evolusi": "#0077b6",
    "Penutupan": "#023e8a",
    "Tidak Terklasifikasi": "#F50F1A",
}

from streamlit_agraph import Config

GRAPH_CONFIG = Config(
    width="100%",
    height=550,
    directed=True,
    physics=True,
    hierarchical=False,
)
