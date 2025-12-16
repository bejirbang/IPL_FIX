import pandas as pd
import numpy as np

def get_tiket_data(engine):
    df_tiket = pd.read_sql("""
        SELECT produk_hierarki, qty_tiket
        FROM ds_ipl.tiket_keluhan
    """, engine)

    df_tiket_agg = df_tiket.groupby('produk_hierarki', as_index=False)['qty_tiket'].sum()
    df_tiket_agg.rename(columns={'qty_tiket': 'total_qty_tiket'}, inplace=True)

    conditions = [
        (df_tiket_agg['total_qty_tiket'] == 0),
        (df_tiket_agg['total_qty_tiket'] > 0) & (df_tiket_agg['total_qty_tiket'] <= 100),
        (df_tiket_agg['total_qty_tiket'] > 100) & (df_tiket_agg['total_qty_tiket'] <= 500),
        (df_tiket_agg['total_qty_tiket'] > 500)
    ]

    choices = ['Belum Ada', 'Rendah', 'Sedang', 'Tinggi']

    df_tiket_agg['indikator_tiket'] = np.select(conditions, choices, default=None)
    df_tiket_agg.insert(0, 'tiketId', ['T' + str(i+1) for i in range(len(df_tiket_agg))])

    return df_tiket_agg
