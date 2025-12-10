import streamlit as st

# Import controller dari masing-masing folder
from .pendapatan.controller import render_pendapatan
from .penggunaan.controller import render_stamping
from .po_settlement.controller import render_posettlement
from .keluhan.controller import render_keluhan

def show_tab1(engine):
    st.title("📊 Dashboard Visualisasi")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Pendapatan",
        "Stamping",
        "PO Settlement",
        "Keluhan"
    ])

    with tab1:
        render_pendapatan(engine)

    with tab2:
        render_stamping(engine)

    with tab3:
        render_posettlement(engine)

    with tab4:
        render_keluhan(engine)
