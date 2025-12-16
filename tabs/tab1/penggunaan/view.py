import streamlit as st
import pandas as pd
from .charts import chart_stamping_per_produk, chart_stamping_trend

def render_stamping_view(df, df_filtered, df_trend):

    st.metric("Total Stamping", df_filtered["qty"].sum())

    st.subheader("Total Stamping per Produk")
    stamping_per_produk = (
        df_filtered.groupby("produk_hierarki", as_index=False)["qty"]
        .sum()
        .sort_values("qty", ascending=False)
    )
    stamping_per_produk["persentase"] = (
        stamping_per_produk["qty"] / stamping_per_produk["qty"].sum() * 100
    ).round(2)

    st.altair_chart(chart_stamping_per_produk(stamping_per_produk), use_container_width=True)

    st.subheader("Tren Stamping Bulanan")
    st.altair_chart(chart_stamping_trend(df_trend), use_container_width=True)
