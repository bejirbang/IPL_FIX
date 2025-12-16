import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from functools import lru_cache

# ============================================================
# 1️⃣ LOAD ENV + CREATE ENGINE (OPTIMIZED)
# ============================================================

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)

load_env()

@lru_cache(maxsize=1)
def get_engine():
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    return create_engine(f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}")

engine = get_engine()

# ============================================================
# 2️⃣ LOAD FUNGSI INDIKATOR
# ============================================================
from fitur_program.indikator_pendapatan.pendapatan_function import get_pendapatan_data
from fitur_program.indikator_penggunaan.penggunaan import get_penggunaan_data
from fitur_program.indikator_tiket.tiket_machine import get_tiket_data
from fitur_program.indikator_csi.CSI_function import get_csi_data


# ============================================================
# 3️⃣ HELPER: READ SQL (CACHED)
# ============================================================
@lru_cache(maxsize=16)
def cached_query(sql: str):
    return pd.read_sql(sql, engine)


# ============================================================
# 4️⃣ FASE PRODUK
# ============================================================
FASE_RULES = {
    "Perencanaan & Konseptual":  ("Belum Ada", "Belum Ada", "Belum Ada", "Belum Ada"),
    "Rilis (Go Live)":            ("Rendah", "Rendah", "Rendah", "Rendah"),
    "Pertumbuhan":                ("Tinggi", "Tinggi", "Rendah", "Tinggi"),
    "Evolusi":                    ("Sedang", "Rendah", "Tinggi", "Sedang"),
    "Penutupan":                  ("Rendah", "Rendah", "Tinggi", "Rendah"),
}

def tentukan_fase_vectorized(df):
    df = df.copy()
    df["fase_produk"] = "Tidak Terklasifikasi"

    for fase, (rev, png, kel, csi) in FASE_RULES.items():
        mask = (
            (df["indikator_pendapatan"] == rev) &
            (df["indikator_penggunaan"].fillna(png) == png) &
            (df["indikator_tiket"] == kel) &
            (df["indikator_csi"] == csi)
        )
        df.loc[mask, "fase_produk"] = fase

    return df


# ============================================================
# 5️⃣ REKOMENDASI (OPTIMIZED)
# ============================================================
def rekomendasi_dan_campaign(fase, keluhan):
    if pd.isna(fase):
        return ("Tidak ada fase", "Tidak ada campaign")

    f = str(fase).lower()
    k = str(keluhan).lower() if isinstance(keluhan, str) else ""

    # SAME RULES EXACTLY
    # (tidak disingkat agar sama seperti aslinya)

    if "perencanaan & konseptual" in f:
        if any(w in k for w in ["akun", "regist", "portal"]):
            return ("Validasi kebutuhan autentikasi & sistem pendaftaran; Lakukan uji UX dan keamanan login.",
                    "Campaign edukatif tentang keamanan & manfaat produk; Publikasi artikel awareness.")
        elif any(w in k for w in ["pembelian", "kuota"]):
            return ("Susun business case terkait monetisasi; Validasi kebutuhan pelanggan.",
                    "Publikasi teaser tentang value produk; Edukasi fitur utama.")
        return ("Validasi kebutuhan & feasibility produk digital; Susun MVP.",
                "Riset audiens & campaign edukatif.")

    if "rilis (go live)" in f:
        if any(w in k for w in ["signing", "certificate"]):
            return ("Perkuat modul signing & validasi sertifikat.",
                    "Launch campaign dengan demo signing.")
        elif any(w in k for w in ["portal", "akun"]):
            return ("Pastikan kestabilan login & portal.",
                    "Campaign onboarding pengguna.")
        return ("Kelola feedback pasca rilis.",
                "Launch campaign besar.")

    if "pertumbuhan" in f:
        if any(w in k for w in ["kuota", "pembelian"]):
            return ("Optimalkan manajemen kuota & pembayaran.",
                    "Referral + loyalty program.")
        if any(w in k for w in ["portal", "akun"]):
            return ("Tingkatkan performa login & dashboard.",
                    "Campaign retensi pengguna.")
        return ("Ekspansi fitur & optimasi infrastruktur.",
                "Referral, loyalty, success story.")

    if "evolusi" in f:
        if any(w in k for w in ["signing", "certificate"]):
            return ("Evaluasi fitur signing; redesign UI/UX.",
                    "Webinar demo fitur baru.")
        if any(w in k for w in ["portal", "akun"]):
            return ("Rebranding portal & integrasi feedback.",
                    "Demo fitur baru via webinar.")
        return ("Evaluasi fitur eksisting & inovasi.",
                "Melibatkan pengguna dalam pengembangan selanjutnya.")

    if "penutupan" in f:
        if any(w in k for w in ["akun", "portal"]):
            return ("Migrasi pengguna & dokumentasi pembelajaran.",
                    "Komunikasi penghentian layanan secara empatik.")
        return ("Rancang sunset policy & migrasi.",
                "Komunikasi penghentian layanan secara positif.")

    return ("Menyesuaikan indikator.", "Menyesuaikan indikator.")


# ============================================================
# 6️⃣ GENERATE ALL DATA —  *MAIN FUNCTION*
# ============================================================
def generate_all_nodes_and_rekomendasi():

    df_rev  = get_pendapatan_data(engine)
    df_use  = get_penggunaan_data(engine)
    df_tik  = get_tiket_data(engine)
    df_csi  = get_csi_data(engine)

    df_all = df_rev.merge(df_use, on="produk_hierarki", how="outer") \
                   .merge(df_tik, on="produk_hierarki", how="outer") \
                   .merge(df_csi, on="produk_hierarki", how="outer")

    df_all = tentukan_fase_vectorized(df_all)

    df_all["alasan_tidak_terklasifikasi"] = np.where(
        df_all["fase_produk"] == "Tidak Terklasifikasi",
        "Pendapatan: " + df_all["indikator_pendapatan"].astype(str) +
        ", Penggunaan: " + df_all["indikator_penggunaan"].astype(str) +
        ", Keluhan: " + df_all["indikator_tiket"].astype(str) +
        ", CSI: " + df_all["indikator_csi"].astype(str),
        np.nan
    )

    df_fase_node = df_all[["produk_hierarki", "fase_produk", "alasan_tidak_terklasifikasi"]].copy()
    df_fase_node["faseId"] = ["F" + str(i+1) for i in range(len(df_fase_node))]
    df_fase_node = df_fase_node[["faseId", "produk_hierarki", "fase_produk", "alasan_tidak_terklasifikasi"]]

    df_keluhan = cached_query(
        "SELECT produk_hierarki, klasifikasi_keluhan FROM ds_ipl.tiket_keluhan"
    )

    df_rekom = df_all.merge(df_keluhan, on="produk_hierarki", how="left")

    df_rekom = df_rekom.groupby(
        ["produk_hierarki", "fase_produk"], as_index=False
    ).agg({
        "klasifikasi_keluhan": lambda x: ", ".join(sorted(set([str(i) for i in x if pd.notna(i)])))
    })

    indicator_cols = ["indikator_pendapatan", "indikator_penggunaan", "indikator_tiket", "indikator_csi"]
    df_rekom = df_rekom.merge(df_all[["produk_hierarki"] + indicator_cols], on="produk_hierarki", how="left")

    hasil = df_rekom.apply(
        lambda r: rekomendasi_dan_campaign(r["fase_produk"], r["klasifikasi_keluhan"]),
        axis=1, result_type="expand"
    )
    hasil.columns = ["rekomendasi_aksi", "fokus_campaign"]
    df_rekom = pd.concat([df_rekom, hasil], axis=1)

    df_rekom["rekomId"] = ["R" + str(i+1) for i in range(len(df_rekom))]

    return df_all, df_fase_node, df_rekom


# ============================================================
# 7️⃣ **DATA UNTUK TAB VISUALISASI** (Pendapatan, Penggunaan, PO, Keluhan)
# ============================================================

@lru_cache(maxsize=8)
def load_pendapatan():
    return cached_query("SELECT * FROM ds_ipl.pendapatan")

@lru_cache(maxsize=8)
def load_penggunaan():
    return cached_query("SELECT * FROM ds_ipl.penggunaan")

@lru_cache(maxsize=8)
def load_po_settlement():
    return cached_query("SELECT * FROM ds_ipl.po_settlement")

@lru_cache(maxsize=8)
def load_keluhan():
    return cached_query("SELECT * FROM ds_ipl.tiket_keluhan")
