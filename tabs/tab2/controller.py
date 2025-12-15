import streamlit as st
from backend import generate_all_nodes_and_rekomendasi
from streamlit_agraph import agraph

from .style import FASE_COLORS, GRAPH_CONFIG
from .graph_builder import build_graph_nodes_edges


def render_tab2(engine):

    st.header("Product Lifecycle Analysis")

    try:
        with st.spinner("🔄 Mengambil dan memproses data..."):
            df_all, df_fase_node, df_rekom = generate_all_nodes_and_rekomendasi()

        st.success("Data berhasil diproses!")

        nodes, edges = build_graph_nodes_edges(df_rekom, FASE_COLORS)

        graph_expander = st.expander("Product Lifecycle Graph", expanded=True)

        with graph_expander:

            col_left, col_graph, col_info = st.columns([1.2, 4, 1.2])

            with col_left:
                with st.expander("ℹ️ Catatan Fase Produk", expanded=False):
                    st.markdown("""
                    **Sistem Product Lifecycle ini memiliki 6 fase utama:**

                    1. **Perencanaan & Konseptual**  
                    2. **Rilis (Go Live)**  
                    3. **Pertumbuhan**  
                    4. **Evolusi**  
                    5. **Penutupan**  
                    6. **Tidak Terklasifikasi**

                    Warna node dibedakan berdasarkan **jenis entitas**:
                    - 🔵 **Fase Produk**
                    - 🟢 **Produk**
                    """)

            with col_graph:
                selected = agraph(
                    nodes=nodes,
                    edges=edges,
                    config=GRAPH_CONFIG
                )

            with col_info:
                with st.expander("OVERVIEW", expanded=True):
                    
                    fase_nodes = [
                        n for n in nodes
                        if str(n.id).startswith("fase_")
                    ]
                    produk_nodes = [
                        n for n in nodes
                        if not str(n.id).startswith("fase_")
                    ]

                    # Relationship types
                    rel_types = {}
                    for e in edges:
                        rel_types[e.label] = rel_types.get(e.label, 0) + 1
                    
                    st.markdown("**Node Summary**")
                    st.info(f"Fase : {len(fase_nodes)}")
                    st.success(f"Produk : {len(produk_nodes)}")

                    # spacer
                    st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

                    st.write(f"**Total Nodes** : {len(nodes)}")

                    st.divider()

                    st.markdown("**Relationships**")
                    for rel, total in rel_types.items():
                        st.write(f"- `{rel}` : {total}")

        # ============================================
        # DETAIL PRODUK
        # ============================================
        if selected:
            st.subheader("📄 Detail Produk")

            row = df_rekom[df_rekom["produk_hierarki"] == selected].head(1)

            if not row.empty:
                r = row.iloc[0]

                st.markdown(f"### **{r['produk_hierarki']}**")
                st.markdown(f"**Fase Produk:** {r['fase_produk']}")
                st.markdown(f"**Keluhan:** {r['klasifikasi_keluhan']}")

                if str(r["fase_produk"]).lower() == "tidak terklasifikasi":
                    st.warning(
                        f"- Pendapatan: {r['indikator_pendapatan']}\n"
                        f"- Penggunaan: {r['indikator_penggunaan']}\n"
                        f"- Keluhan: {r['indikator_tiket']}\n"
                        f"- CSI: {r['indikator_csi']}"
                    )

                st.markdown(f"**Rekomendasi Aksi:** {r['rekomendasi_aksi']}")
                st.markdown(f"**Fokus Campaign:** {r['fokus_campaign']}")

        with st.expander("📋 Data Tabel"):
            st.dataframe(df_rekom)

    except Exception as e:
        st.error(f"Gagal memuat tab 2: {e}")
