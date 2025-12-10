import streamlit as st
from .query import load_po_settlement
from .preprocess import preprocess_po
from .view import render_po_view

def render_posettlement(engine):

    # Load data
    df = load_po_settlement(engine)
    df = preprocess_po(df)

    # Filter UI
    st.markdown("# Filter Data PO Settlement")
    col1, col2 = st.columns(2)

    with col1:
        tahun_list = sorted(df["tahun"].dropna().unique())
        tahun_selected = st.selectbox("Tahun PO", tahun_list, index=len(tahun_list)-1)

    with col2:
        bulan_list = (
            df[["bulan", "bulan_nama"]]
            .drop_duplicates()
            .sort_values("bulan")["bulan_nama"]
            .tolist()
        )
        bulan_selected = st.selectbox("Bulan PO", bulan_list)

    df_filtered = df[
        (df["tahun"] == tahun_selected) &
        (df["bulan_nama"] == bulan_selected)
    ]

    # Total PO per tipe
    df_tipe = (
        df_filtered.groupby("tipe", as_index=False)["total_po"]
        .sum()
        .sort_values("total_po", ascending=False)
    )
    df_tipe["persentase"] = (
        df_tipe["total_po"] / df_tipe["total_po"].sum() * 100
    ).round(2)

    # Trend chart
    df_trend = (
        df.groupby([df["tanggal"].dt.to_period("M"), "tipe"])["total_po"]
        .sum()
        .reset_index()
    )
    df_trend["tanggal"] = df_trend["tanggal"].astype(str)

    # Top perusahaan per tipe
    df_top = (
        df_filtered.groupby(["tipe", "nama_perusahaan"], as_index=False)["total_po"]
        .sum()
    )
    df_top = df_top.sort_values(["tipe", "total_po"], ascending=[True, False]) \
                   .groupby("tipe", group_keys=False).head(5)
    df_top["persentase"] = (
        df_top["total_po"] / df_top.groupby("tipe")["total_po"].transform("sum") * 100
    ).round(2)

    # Render final view
    render_po_view(df_tipe, df_tipe, df_trend, df_top)
