import altair as alt

def chart_total_per_produk(df):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("nilai_tagihan:Q", title="Total Pendapatan (Rp)"),
            y=alt.Y("produk_hierarki:N", sort='-x'),
            color=alt.Color("produk_hierarki:N", legend=None),
            tooltip=["produk_hierarki", "nilai_tagihan"], #PERSENTASE GA BISA DIMUNCULIN ("persentase")
        )
    )
    return chart


def chart_trend(df_trend):
    return (
        alt.Chart(df_trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("tgl_transaksi:T", title="Bulan"),
            y=alt.Y("nilai_tagihan:Q", title="Pendapatan"),
            color="produk_hierarki:N",
        )
    )


def chart_top_customer(df_top5):
    return (
        alt.Chart(df_top5)
        .mark_bar()
        .encode(
            x="sum(nilai_tagihan):Q",
            y=alt.Y("nama_pelanggan:N", sort='-x'),
            color="produk_hierarki:N",
        )
    )
