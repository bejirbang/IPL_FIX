import pandas as pd
import numpy as np

def get_csi_data(engine):
    df_csi = pd.read_sql("""
        SELECT produk_hierarki, skor_csi
        FROM ds_ipl.csi_produk
    """, engine)

    df_csi_agg = df_csi.groupby('produk_hierarki', as_index=False)['skor_csi'].sum()
    df_csi_agg.rename(columns={'skor_csi': 'total_skor_csi'}, inplace=True)

    conditions = [
        (df_csi_agg['total_skor_csi'] == 0),
        (df_csi_agg['total_skor_csi'] > 0) & (df_csi_agg['total_skor_csi'] <= 70),
        (df_csi_agg['total_skor_csi'] > 70) & (df_csi_agg['total_skor_csi'] <= 80),
        (df_csi_agg['total_skor_csi'] > 80)
    ]

    choices = ['Belum Ada', 'Rendah', 'Sedang', 'Tinggi']

    df_csi_agg['indikator_csi'] = np.select(conditions, choices, default=None)
    df_csi_agg.insert(0, 'csiId', ['C' + str(i+1) for i in range(len(df_csi_agg))])

    return df_csi_agg
