import streamlit as st
from datetime import datetime
import pandas as pd
from io import BytesIO

from .utils.excel_export import to_excel_bytes
from backend import generate_all_nodes_and_rekomendasi


from .revenue.controller import render_revenue
from .keluhan.controller import render_keluhan
from .stamping.controller import render_stamping


def show_tab3(engine):
    st.header("Reporting & Monitoring")

    # -----------------------------
    # LOAD REKOM (fase produk)
    # -----------------------------
    if "df_phase" not in st.session_state:
        with st.spinner("🔄 Menghasilkan rekomendasi..."):

            df_all, df_phase, df_rekom = generate_all_nodes_and_rekomendasi()

            st.session_state.df_all = df_all
            st.session_state.df_phase = df_phase
            st.session_state.df_rekom = df_rekom

        st.success("Rekomendasi berhasil digenerate!")

    # Setelah pasti tersedia
    df_phase = st.session_state.df_phase
    df_rekom = st.session_state.df_rekom
    df_all   = st.session_state.df_all

    # -----------------------------
    # PILIHAN REPORT
    # -----------------------------
    pilihan = st.radio(
        "Pilih Jenis Data:",
        ["Revenue", "Keluhan", "Stamping"],
        horizontal=True
    )

    # -----------------------------
    # RENDER SESUAI PILIHAN
    # -----------------------------
    if pilihan == "Revenue":
        render_revenue(engine, df_rekom)

    elif pilihan == "Keluhan":
        render_keluhan(engine, df_rekom)

    elif pilihan == "Stamping":
        render_stamping(engine, df_rekom)

