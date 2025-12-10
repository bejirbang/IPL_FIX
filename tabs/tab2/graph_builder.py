from streamlit_agraph import Node, Edge
from .style import (
    FASE_COLORS,
    NODE_STYLE_FASE,
    NODE_STYLE_PRODUK,
    EDGE_STYLE,
)

def build_graph_nodes_edges(df_rekom):

    nodes = []
    edges = []

    # Pastikan fase unik
    fase_list = df_rekom["fase_produk"].dropna().unique()

    # --- Node Fase ---
    for fase in fase_list:
        nodes.append(Node(
            id=f"fase_{fase}",
            label=fase,
            color={
                "background": FASE_COLORS.get(fase, "#ddd"),
                "border": "#000",
                "highlight": {"background": "#ffe066", "border": "#000"}
            },
            title=f"Fase Produk: {fase}",
            **NODE_STYLE_FASE
        ))

    # --- Node Produk + Edge ---
    for _, r in df_rekom.iterrows():
        nodes.append(Node(
            id=r["produk_hierarki"],
            label=r["produk_hierarki"],
            color={
                "background": FASE_COLORS.get(r["fase_produk"], "#90e0ef"),
                "highlight": {
                    "background": "#48cae4",
                    "border": "#0077b6"
                }
            },
            title=f"Produk: {r['produk_hierarki']}\nFase: {r['fase_produk']}",
            **NODE_STYLE_PRODUK
        ))

        edges.append(Edge(
            source=f"fase_{r['fase_produk']}",
            target=r["produk_hierarki"],
            **EDGE_STYLE
        ))

    return nodes, edges
