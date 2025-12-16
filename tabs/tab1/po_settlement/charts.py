import altair as alt

def chart_po_per_tipe(df):
    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="total_po:Q",
            y=alt.Y("tipe:N", sort="-x"),
            color=alt.Color("tipe:N", legend=None),
            tooltip=["tipe", "total_po", "persentase"],
        )
    )

    text = (
        alt.Chart(df)
        .mark_text(align="left", baseline="middle", dx=5, color="white")
        .encode(
            x="total_po:Q",
            y="tipe:N",
            text=alt.Text("persentase:Q", format=".2f"),
        )
    )

    return bar + text

def chart_trend_po(df):
    return (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("tanggal:T", title="Bulan"),
            y=alt.Y("total_po:Q", title="Total PO"),
            color=alt.Color("tipe:N", title="Tipe PO"),
            tooltip=["tanggal", "tipe", "total_po"],
        )
    )

def chart_top_perusahaan(df):
    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="total_po:Q",
            y=alt.Y("nama_perusahaan:N", sort="-x"),
            color=alt.Color("tipe:N"),
            tooltip=["tipe", "nama_perusahaan", "total_po", "persentase"]
        )
    )

    text = (
        alt.Chart(df)
        .mark_text(align="left", baseline="middle", dx=3, color="white")
        .encode(
            x="total_po:Q",
            y="nama_perusahaan:N",
            text=alt.Text("persentase:Q", format=".2f")
        )
    )

    return bar + text
