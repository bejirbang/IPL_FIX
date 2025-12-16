import altair as alt

def chart_stamping_per_produk(df):
    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("qty:Q", title="Total Stamping"),
            y=alt.Y("produk_hierarki:N", sort="-x"),
            color=alt.Color("produk_hierarki:N", legend=None),
            tooltip=["produk_hierarki", "qty", "persentase"],
        )
    )

    text = (
        alt.Chart(df)
        .mark_text(align="left", baseline="middle", dx=3, color="white")
        .encode(
            x="qty:Q",
            y="produk_hierarki:N",
            text=alt.Text("persentase:Q", format=".2f"),
        )
    )

    return bar + text


def chart_stamping_trend(df):
    return (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("tanggal:T", title="Bulan"),
            y=alt.Y("qty:Q", title="Jumlah Stamping"),
            color="produk_hierarki:N",
            tooltip=["tanggal", "produk_hierarki", "qty"]
        )
    )
