import pandas as pd

def load_pendapatan(engine):
    return pd.read_sql("SELECT * FROM ds_ipl.pendapatan_produk;", engine)
