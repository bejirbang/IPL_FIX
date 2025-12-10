import streamlit as st
from .query import load_pendapatan
from .preprocess import preprocess_pendapatan, filter_pendapatan
from .charts import chart_total_per_produk, chart_trend, chart_top_customer
from .view import view_filter, view_metric

def render_pendapatan(engine):

    df = load_pendapatan(engine)
    df = preprocess_pendapatan(df)

    tahun, bulan = view_filter(df)
    df_filtered = filter_pendapatan(df, tahun, bulan)

    total = df_filtered["nilai_tagihan"].sum()
    view_metric(total)

    # Chart 1
    st.subheader("Total Pendapatan per Produk")
    df_group = df_filtered.groupby("produk_hierarki", as_index=False)["nilai_tagihan"].sum()
    st.altair_chart(chart_total_per_produk(df_group), use_container_width=True)

    # Chart 2
    st.subheader("Trend Pendapatan")
    df_trend = df.groupby([df["tgl_transaksi"].dt.to_period("M"), "produk_hierarki"])["nilai_tagihan"].sum().reset_index()
    df_trend["tgl_transaksi"] = df_trend["tgl_transaksi"].astype(str)
    st.altair_chart(chart_trend(df_trend), use_container_width=True)

    # Chart 3
    st.subheader("Top 5 Customer")
    df_top = df_filtered.groupby(["nama_pelanggan", "produk_hierarki"], as_index=False)["nilai_tagihan"].sum()
    top5 = df_top.groupby("nama_pelanggan")["nilai_tagihan"].sum().nlargest(5).index
    df_top5 = df_top[df_top["nama_pelanggan"].isin(top5)]
    st.altair_chart(chart_top_customer(df_top5), use_container_width=True)
