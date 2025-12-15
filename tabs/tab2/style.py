from streamlit_agraph import Config

FASE_COLORS = {}

NODE_COLORS = {
    "fase": "#2563EB",      
    "produk": "#22C55E"     
}

GRAPH_THEME = {
    "background": "#020617",
    "edge_color": "#94a3b8",
    "highlight": "#38bdf8",
    "font_color": "#E5E7EB"
}

GRAPH_CONFIG = Config(
    width="100%",
    height=550,
    directed=True,
    physics=True,
    hierarchical=False,

    nodeHighlightBehavior=True,
    highlightColor=GRAPH_THEME["highlight"],

    node={
        "shape": "dot",
        "borderWidth": 2,
        "font": {
            "size": 14,
            "color": GRAPH_THEME["font_color"]
        }
    },

    edge={
        "smooth": True,
        "color": GRAPH_THEME["edge_color"]
    }
)
