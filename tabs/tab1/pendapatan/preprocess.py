import calendar
import pandas as pd

def preprocess_pendapatan(df):
    df["tgl_transaksi"] = pd.to_datetime(df["tgl_transaksi"], errors="coerce")
    df["tahun"] = df["tgl_transaksi"].dt.year
    df["bulan_num"] = df["tgl_transaksi"].dt.month
    df["bulan"] = df["bulan_num"].apply(lambda x: calendar.month_name[x])
    return df


def filter_pendapatan(df, tahun, bulan):
    return df[(df["tahun"] == tahun) & (df["bulan"] == bulan)]
