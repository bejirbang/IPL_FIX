# ============================
# STYLE SETTINGS
# ============================

# --- Color Mapping untuk Fase ---
FASE_COLORS = {
    "Perencanaan & Konseptual": "#48cae4",
    "Rilis (Go Live)": "#00b4d8",
    "Pertumbuhan": "#0096c7",
    "Evolusi": "#0077b6",
    "Penutupan": "#023e8a",
    "Tidak Terklasifikasi": "#F50F1A",
}

# --- Default Node Style ---
NODE_STYLE_FASE = {
    "size": 50,
    "shape": "box",
    "borderWidth": 3,
    "font": {"size": 18, "color": "#000", "bold": True},
}

NODE_STYLE_PRODUK = {
    "size": 28,
    "shape": "ellipse",
    "borderWidth": 1,
    "font": {"size": 14, "bold": False},
}

# --- Edge Style ---
EDGE_STYLE = {
    "width": 2,
    "color": "#0077b6",
    "arrows": "to",
    "smooth": True
}

# --- Vis.js Config ---
from streamlit_agraph import Config

GRAPH_CONFIG = Config(
    width="100%",
    height=550,
    directed=True,
    physics=True,
    hierarchical=False,
)
