import streamlit as st
from .query import load_stamping
from .preprocess import preprocess_stamping
from .view import render_stamping_view

def render_stamping(engine):

    # Load
    df = load_stamping(engine)
    df = preprocess_stamping(df)

    # FILTER UI
    st.markdown("## Filter Data Stamping")

    tahun = st.selectbox("Tahun", sorted(df["tahun"].dropna().unique()))
    bulan = st.selectbox("Bulan", sorted(df["bulan"].dropna().unique()))

    df_filtered = df[(df["tahun"] == tahun) & (df["bulan"] == bulan)]

    # Trend chart (ambil semua data)
    df_trend = (
        df.groupby([df["tanggal"].dt.to_period("M"), "produk_hierarki"])["qty"]
        .sum()
        .reset_index()
    )
    df_trend["tanggal"] = df_trend["tanggal"].astype(str)

    # Render
    render_stamping_view(df, df_filtered, df_trend)
