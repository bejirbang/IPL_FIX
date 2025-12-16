import streamlit as st
from .query import load_keluhan
from .preprocess import preprocess_keluhan, filter_keluhan
from .charts import chart_klasifikasi, chart_tren, chart_top_tipe
from .view import render_filter


def render_keluhan(engine):
    # Load
    df = load_keluhan(engine)

    # Preprocess
    df, time_col = preprocess_keluhan(df)

    # Filter UI
    tahun, bulan, produk = render_filter(df)
    df_filtered = filter_keluhan(df, tahun, bulan, produk)

    # Total tiket
    total_keluhan = (
        df_filtered["qty_tiket"].sum()
        if "qty_tiket" in df_filtered.columns
        else len(df_filtered)
    )

    st.metric("Total Tiket", total_keluhan)

    # --- BAR: Klasifikasi Keluhan
    st.subheader("Total Tiket per Klasifikasi Keluhan")

    if "klasifikasi_keluhan" in df_filtered.columns:
        klas_df = (
            df_filtered.groupby("klasifikasi_keluhan", as_index=False)["qty_tiket"]
            .sum()
            .sort_values("qty_tiket", ascending=False)
        )

        klas_df["persentase"] = (
            klas_df["qty_tiket"] / klas_df["qty_tiket"].sum() * 100
        ).round(2)

        st.altair_chart(chart_klasifikasi(klas_df), use_container_width=True)

    # --- LINE: Tren Keluhan
    st.subheader("Tren Keluhan Bulanan (Per Klasifikasi)")

    if "klasifikasi_keluhan" in df.columns:
        df_tren = (
            df.groupby([df[time_col].dt.to_period("M"), "klasifikasi_keluhan"])["qty_tiket"]
            .sum()
            .reset_index()
        )

        df_tren[time_col] = df_tren[time_col].astype(str)

        st.altair_chart(chart_tren(df_tren, time_col), use_container_width=True)

    # --- TOP 5 TIPE KELUHAN
    st.subheader("Top 5 Tipe Keluhan per Produk")

    required_cols = {"produk_hierarki", "tipe_keluhan", "qty_tiket"}

    if required_cols.issubset(df.columns):
        df_top = (
            df[df["produk_hierarki"] == produk]
            .groupby("tipe_keluhan", as_index=False)["qty_tiket"]
            .sum()
            .sort_values("qty_tiket", ascending=False)
            .head(5)
        )
        df_top["persentase"] = (
            df_top["qty_tiket"] / df_top["qty_tiket"].sum() * 100
        ).round(2)

        st.altair_chart(chart_top_tipe(df_top), use_container_width=True)
