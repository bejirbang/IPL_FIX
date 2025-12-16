import streamlit as st
from .charts import chart_po_per_tipe, chart_trend_po, chart_top_perusahaan

def render_po_view(df, df_filtered, df_trend, df_top):
    
    st.subheader("Total PO per Tipe")
    st.altair_chart(chart_po_per_tipe(df_filtered), use_container_width=True)

    st.subheader("Tren Total PO per Bulan")
    st.altair_chart(chart_trend_po(df_trend), use_container_width=True)

    st.subheader("Klasifikasi Perusahaan Menurut Tipe PO")
    st.altair_chart(chart_top_perusahaan(df_top), use_container_width=True)
