import altair as alt

def chart_klasifikasi(klas_df):
    bar = (
        alt.Chart(klas_df)
        .mark_bar()
        .encode(
            x=alt.X("qty_tiket:Q", title="Jumlah Keluhan"),
            y=alt.Y("klasifikasi_keluhan:N", sort="-x", title="Klasifikasi Keluhan"),
            color=alt.Color("klasifikasi_keluhan:N", legend=None),
            tooltip=["klasifikasi_keluhan", "qty_tiket", "persentase"]
        )
    )

    text = (
        alt.Chart(klas_df)
        .mark_text(align="left", dx=5)
        .encode(
            x="qty_tiket:Q",
            y="klasifikasi_keluhan:N",
            text="persentase:Q"
        )
    )
    return bar + text

def chart_tren(df_tren, time_col):
    return (
        alt.Chart(df_tren)
        .mark_line(point=True)
        .encode(
            x=alt.X(f"{time_col}:T", title="Bulan"),
            y=alt.Y("qty_tiket:Q", title="Jumlah Keluhan"),
            color=alt.Color("klasifikasi_keluhan:N", title="Klasifikasi"),
            tooltip=[time_col, "klasifikasi_keluhan", "qty_tiket"]
        )
        .properties(height=350)
    )

def chart_top_tipe(df_top):
    bar = (
        alt.Chart(df_top)
        .mark_bar()
        .encode(
            x=alt.X("qty_tiket:Q", title="Jumlah Keluhan"),
            y=alt.Y("tipe_keluhan:N", sort="-x", title="Tipe Keluhan"),
            color=alt.Color("tipe_keluhan:N", legend=None),
            tooltip=["tipe_keluhan", "qty_tiket", "persentase"]
        )
    )

    text = (
        alt.Chart(df_top)
        .mark_text(align="left", baseline="middle", dx=3, color="white")
        .encode(
            x="qty_tiket:Q",
            y="tipe_keluhan:N",
            text=alt.Text("persentase:Q", format=".2f")
        )
    )

    return bar + text
