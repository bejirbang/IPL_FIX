query_revenue = """
SELECT 
    id, tgl_transaksi, produk_hierarki, nama_produk,
    nama_pelanggan, qty_pesanan, nilai_tagihan, created_at
FROM pendapatan_produk;
"""