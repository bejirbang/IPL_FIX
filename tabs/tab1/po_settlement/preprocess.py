import pandas as pd

def preprocess_po(df):
    if "tanggal" in df.columns:
        df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
        df["tahun"] = df["tanggal"].dt.year
        df["bulan"] = df["tanggal"].dt.month
        df["bulan_nama"] = df["tanggal"].dt.month_name()
    return df
