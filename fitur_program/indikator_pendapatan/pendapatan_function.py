import pandas as pd
import numpy as np

def get_pendapatan_data(engine):

    # --- Load data dari DB
    df_pendapatan = pd.read_sql("""
        SELECT produk_hierarki, nama_produk, nilai_tagihan
        FROM ds_ipl.pendapatan_produk
    """, engine)

    # --- Agregasi total nilai_tagihan per produk (sesuai versi awal)
    df_revenue_node = (
        df_pendapatan
        .groupby(['produk_hierarki', 'nama_produk'], as_index=False)
        .agg(total_nilai_tagihan=('nilai_tagihan', 'sum'))
    )

    # --- Tambahkan ID unik
    df_revenue_node.insert(
        0,
        'revenueId',
        ['R' + str(i + 1) for i in range(len(df_revenue_node))]
    )

    # --- Tentukan indikator pendapatan
    df_revenue_node['indikator_pendapatan'] = np.select(
        [
            (df_revenue_node['total_nilai_tagihan'] == 0),
            (df_revenue_node['total_nilai_tagihan'] > 0) & 
            (df_revenue_node['total_nilai_tagihan'] <= 50_000_000),

            (df_revenue_node['total_nilai_tagihan'] > 50_000_000) & 
            (df_revenue_node['total_nilai_tagihan'] <= 300_000_000),

            (df_revenue_node['total_nilai_tagihan'] > 300_000_000)
        ],
        ['Belum Ada', 'Rendah', 'Sedang', 'Tinggi'],
        default=None
    )

    return df_revenue_node
