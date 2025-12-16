import pandas as pd
import streamlit as st
from .query import query_revenue
from ..utils.excel_export import to_excel_bytes
from ..utils.pdf_revenue import generate_pdf_revenue

def render_revenue(engine, df_phase):
    st.subheader("Revenue (pendapatan_produk)")

    df = pd.read_sql(query_revenue, engine)

    df["nilai_tagihan"] = pd.to_numeric(df["nilai_tagihan"], errors="coerce").fillna(0)

    # FILTER
    produk_opts = sorted(df["produk_hierarki"].dropna().unique().tolist())
    pel_opts = sorted(df["nama_pelanggan"].dropna().unique().tolist())

    c1, c2 = st.columns(2)
    with c1:
        produk = st.selectbox("Filter Produk", ["(Semua)"] + produk_opts)
    with c2:
        pelanggan = st.selectbox("Filter Pelanggan", ["(Semua)"] + pel_opts)

    df_disp = df.copy()
    if produk != "(Semua)":
        df_disp = df_disp[df_disp["produk_hierarki"] == produk]
    if pelanggan != "(Semua)":
        df_disp = df_disp[df_disp["nama_pelanggan"] == pelanggan]

    st.dataframe(df_disp, use_container_width=True)

    # SUMMARY
    df_sum = (
        df.groupby("produk_hierarki", as_index=False)["nilai_tagihan"]
        .sum()
        .sort_values("nilai_tagihan", ascending=False)
    )

    st.markdown("### Ringkasan Total Revenue per Produk")
    st.dataframe(df_sum, use_container_width=True)

    # Download Excel
    st.download_button(
        "Download Full Data (Excel)",
        data=to_excel_bytes(df_disp),
        file_name="revenue.xlsx",
    )

    # Download PDF
    pdf = generate_pdf_revenue(df_sum, df_sum["nilai_tagihan"].sum(), df_phase)
    st.download_button("Download Summary (PDF)", data=pdf, file_name="revenue.pdf")
