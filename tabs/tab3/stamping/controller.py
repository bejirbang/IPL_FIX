import pandas as pd
import streamlit as st
from .query import query_stamping
from ..utils.excel_export import to_excel_bytes
from ..utils.pdf_stamping import generate_pdf_stamping

def render_stamping(engine, df_phase):
    st.subheader("Stamping (penggunaan)")

    df = pd.read_sql(query_stamping, engine)

    produk_opts = sorted(df["produk_hierarki"].unique())
    produk = st.selectbox("Filter Produk", ["(Semua)"] + produk_opts)

    df_disp = df.copy()
    if produk != "(Semua)":
        df_disp = df_disp[df_disp["produk_hierarki"] == produk]

    st.dataframe(df_disp, use_container_width=True)

    df_sum = (
        df.groupby("produk_hierarki", as_index=False)["qty"]
        .sum()
        .sort_values("qty", ascending=False)
    )

    st.markdown("### Ringkasan Total Penggunaan per Produk")
    st.dataframe(df_sum, use_container_width=True)

    st.download_button(
        "Download Full Data (Excel)",
        data=to_excel_bytes(df_disp),
        file_name="stamping.xlsx",
    )

    pdf = generate_pdf_stamping(df_sum, df_phase)
    st.download_button("Download Summary (PDF)", data=pdf, file_name="stamping.pdf")
