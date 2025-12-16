import pandas as pd
import streamlit as st
from .query import query_keluhan
from ..utils.excel_export import to_excel_bytes
from ..utils.pdf_keluhan import generate_pdf_keluhan

def render_keluhan(engine, df_phase):
    st.subheader("Keluhan (tiket_keluhan)")

    df = pd.read_sql(query_keluhan, engine)

    produk_opts = sorted(df["produk_hierarki"].unique())
    klas_opts = sorted(df["klasifikasi_keluhan"].unique())

    c1, c2 = st.columns(2)
    with c1:
        produk = st.selectbox("Filter Produk", ["(Semua)"] + produk_opts)
    with c2:
        klas = st.selectbox("Filter Klasifikasi", ["(Semua)"] + klas_opts)

    df_disp = df.copy()
    if produk != "(Semua)":
        df_disp = df_disp[df_disp["produk_hierarki"] == produk]
    if klas != "(Semua)":
        df_disp = df_disp[df_disp["klasifikasi_keluhan"] == klas]

    st.dataframe(df_disp, use_container_width=True)

    # Top 5
    top5 = (
        df.groupby(["produk_hierarki", "tipe_keluhan"], as_index=False)["qty_tiket"]
        .sum()
        .sort_values(["produk_hierarki", "qty_tiket"], ascending=[True, False])
        .groupby("produk_hierarki")
        .head(5)
    )

    st.markdown("### Top 5 Tipe Keluhan per Produk")
    st.dataframe(top5, use_container_width=True)

    # Export
    st.download_button(
        "Download Full Data (Excel)",
        data=to_excel_bytes(df_disp),
        file_name="keluhan.xlsx",
    )

    pdf = generate_pdf_keluhan(top5, df_phase)
    st.download_button("Download Summary (PDF)", data=pdf, file_name="keluhan.pdf")
