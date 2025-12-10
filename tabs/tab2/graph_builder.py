from streamlit_agraph import Node, Edge

def build_graph_nodes_edges(df_rekom, fase_colors):
    nodes = []
    edges = []

    # --- Node Fase ---
    fase_list = df_rekom["fase_produk"].dropna().unique()
    for fase in fase_list:
        nodes.append(Node(
            id=f"fase_{fase}",
            label=fase,
            color=fase_colors.get(fase, "#ddd"),
            size=40
        ))

    # --- Node Produk + Edge Fase → Produk ---
    for _, r in df_rekom.iterrows():
        nodes.append(Node(
            id=r["produk_hierarki"],
            label=r["produk_hierarki"],
            color=fase_colors.get(r["fase_produk"], "#90e0ef"),
            size=25
        ))

        edges.append(Edge(
            source=f"fase_{r['fase_produk']}",
            target=r["produk_hierarki"]
        ))

    return nodes, edges
