import pandas as pd

def detect_datetime_column(df):
    for col in ["tgl_keluhan", "tgl_tiket", "created_at"]:
        if col in df.columns:
            return col
    return None


def preprocess_keluhan(df):
    time_col = detect_datetime_column(df)

    if time_col:
        df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
        df["tahun"] = df[time_col].dt.year
        df["bulan_num"] = df[time_col].dt.month
        df["bulan"] = df[time_col].dt.month_name()

    return df, time_col


def filter_keluhan(df, tahun, bulan, produk):
    return df[
        (df["tahun"] == tahun) &
        (df["bulan"] == bulan) &
        (df["produk_hierarki"] == produk)
    ]
