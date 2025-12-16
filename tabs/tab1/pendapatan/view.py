import streamlit as st

def view_filter(df):
    col1, col2 = st.columns(2)

    with col1:
        tahun = st.selectbox(
            "Tahun",
            sorted(df["tahun"].unique()),
            index=len(sorted(df["tahun"].unique())) - 1,
        )

    with col2:
        bulan = st.selectbox(
            "Bulan",
            df[["bulan_num", "bulan"]].drop_duplicates().sort_values("bulan_num")["bulan"]
        )

    return tahun, bulan


def view_metric(total):
    st.metric("Total Pendapatan", f"Rp {total:,.0f}")
