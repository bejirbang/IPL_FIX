import pandas as pd
import calendar

def preprocess_stamping(df):
    if "tanggal" in df.columns:
        df["tanggal"] = pd.to_datetime(df["tanggal"], errors="coerce")
        df["tahun"] = df["tanggal"].dt.year
        df["bulan_num"] = df["tanggal"].dt.month
        df["bulan"] = df["bulan_num"].apply(lambda x: calendar.month_name[x])
    return df
