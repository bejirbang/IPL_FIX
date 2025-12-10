import pandas as pd
import numpy as np

def get_penggunaan_data(engine):
    df_penggunaan = pd.read_sql("""
        SELECT produk_hierarki, qty
        FROM ds_ipl.penggunaan
    """, engine)

    df_penggunaan_agg = df_penggunaan.groupby('produk_hierarki', as_index=False)['qty'].sum()
    df_penggunaan_agg.rename(columns={'qty': 'total_qty_penggunaan'}, inplace=True)

    conditions = [
        (df_penggunaan_agg['total_qty_penggunaan'] == 0),
        (df_penggunaan_agg['total_qty_penggunaan'] > 0) & (df_penggunaan_agg['total_qty_penggunaan'] <= 1000),
        (df_penggunaan_agg['total_qty_penggunaan'] > 1000) & (df_penggunaan_agg['total_qty_penggunaan'] <= 5000),
        (df_penggunaan_agg['total_qty_penggunaan'] > 5000)
    ]

    choices = ['Belum Ada', 'Rendah', 'Sedang', 'Tinggi']

    df_penggunaan_agg['indikator_penggunaan'] = np.select(conditions, choices, default=None)
    df_penggunaan_agg.insert(0, 'penggunaanId', ['P' + str(i+1) for i in range(len(df_penggunaan_agg))])

    return df_penggunaan_agg
