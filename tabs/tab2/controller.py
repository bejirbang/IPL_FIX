import streamlit as st
from backend import generate_all_nodes_and_rekomendasi
from streamlit_agraph import agraph
import streamlit_nested_layout

from .style import FASE_COLORS, GRAPH_CONFIG
from .graph_builder import build_graph_nodes_edges


def render_tab2(engine):

    st.header("Product Lifecycle Analysis")

    try:
        with st.spinner("🔄 Mengambil dan memproses data..."):
            df_all, df_fase_node, df_rekom = generate_all_nodes_and_rekomendasi()

        st.success("Data berhasil diproses!")

   
        nodes, edges = build_graph_nodes_edges(df_rekom, FASE_COLORS)

       
        graph_expander = st.expander("📌 Product Lifecycle Graph", expanded=True)

        with graph_expander:

            col_left, col_right = st.columns([1, 3])

            with col_left.expander("ℹ️ Catatan Fase Produk", expanded=False):
                st.markdown("""
                **Sistem Product Lifecycle ini memiliki 6 fase utama:**

                1. **Perencaan & Konseptual - Produk Baru Dirancang** 
                2. **Rilis (Go Live) - Produk Belum Stabil** 
                3. **Pertumbuhan - Produk Sukses di Pasar** 
                4. **Evolusi - Produk Mulai Jenuh di Pasar** 
                5. **Penutupan - Produk Sudah Tidak Efisien Dipertahankan**
                6. **Tidak Terklasifikasi - Data Tidak Mencukupi**            

                Setiap node pada grafik diberi **warna sesuai fasenya**.
                """)

            selected = agraph(nodes=nodes, edges=edges, config=GRAPH_CONFIG)

        # ============================================
        # DETAIL PRODUK
        # ============================================
        if selected:
            st.subheader("📄 Detail Produk")

            row = df_rekom[df_rekom["produk_hierarki"] == selected].head(1)

            if not row.empty:
                r = row.iloc[0]

                st.markdown(f"### **{r['produk_hierarki']}**")
                st.markdown(f"**Fase Produk:** {r['fase_produk']}   ")
                st.markdown(f"**Keluhan:** {r['klasifikasi_keluhan']}")

                if str(r["fase_produk"]).lower() == "tidak terklasifikasi":
                    st.warning(
                        f"Produk tidak terklasifikasi karena indikator berikut:\n\n"
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
