from streamlit_agraph import Node, Edge
from .style import NODE_COLORS


def build_graph_nodes_edges(df_rekom, fase_colors=None):
    nodes = []
    edges = []

    created_nodes = set()

    fase_list = df_rekom["fase_produk"].dropna().unique()

    for fase in fase_list:
        node_id = f"fase_{fase}"
        created_nodes.add(node_id)

        nodes.append(Node(
            id=node_id,
            label=f"\n{fase}",
            size=25,
            borderWidth=2,
            font={
                "size": 13,
                "color": "#ffffff"
            },
            color={
                "background": NODE_COLORS["fase"],
                "border": "#ffffff"
            }
        ))

    for _, r in df_rekom.iterrows():
        produk_id = r["produk_hierarki"]
        fase = r["fase_produk"]

        if produk_id not in created_nodes:
            created_nodes.add(produk_id)

            nodes.append(Node(
                id=produk_id,
                label=produk_id,
                size=25,
                borderWidth=2,
                font={
                    "size": 13,
                    "color": "#ffffff"
                },
                color={
                    "background": NODE_COLORS["produk"],
                    "border": "#ffffff"
                }
            ))

        edges.append(Edge(
            source=f"fase_{fase}",
            target=produk_id,
            label="HAS_PRODUCT",
            smooth=True
        ))

    return nodes, edges
