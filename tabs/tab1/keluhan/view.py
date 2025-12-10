import streamlit as st

def render_filter(df):
    st.markdown("## Filter Keluhan")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        tahun = st.selectbox(
            "Tahun Keluhan",
            sorted(df["tahun"].dropna().unique())
        )

    with col2:
        bulan = st.selectbox(
            "Bulan Keluhan",
            df[["bulan_num", "bulan"]].drop_duplicates().sort_values("bulan_num")["bulan"].tolist()
        )

    with col3:
        produk = st.selectbox(
            "Produk Keluhan",
            sorted(df["produk_hierarki"].dropna().unique())
        )

    return tahun, bulan, produk
