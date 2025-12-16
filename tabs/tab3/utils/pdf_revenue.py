from io import BytesIO
from reportlab.lib.pagesizes import A2
from reportlab.platypus import SimpleDocTemplate, Table, LongTable, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_revenue(df_summary, total_rev, df_phase):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A2, rightMargin=20, leftMargin=20)
    styles = getSampleStyleSheet()

    elems = []
    elems.append(Paragraph("Ringkasan Revenue", styles["Title"]))
    elems.append(Spacer(1, 8))

    # --- SUMMARY REVENUE ---
    data = [["Produk", "Total Revenue"]]
    for _, r in df_summary.iterrows():
        data.append([r["produk_hierarki"], f"Rp {r['nilai_tagihan']:,.0f}"])
    data.append(["TOTAL", f"Rp {total_rev:,.0f}"])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.25,colors.grey),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ]))

    elems += [table, Spacer(1, 12)]

    # --- TABLE PHASE PRODUK ---
    elems.append(Paragraph("Rekomendasi Aksi dan Fokus Campaign", styles["Heading2"]))

    # URUTKAN KOLOM SESUAI HARUSNYA
    kolom = [
        "produk_hierarki","fase_produk","klasifikasi_keluhan",
        "indikator_pendapatan","indikator_penggunaan","indikator_tiket",
        "indikator_csi","rekomendasi_aksi","fokus_campaign"
    ]

    dfp = df_phase[kolom].fillna("")

    phdata = [kolom] + dfp.values.tolist()

    ptable = LongTable(phdata, repeatRows=1)
    ptable.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.25,colors.grey)
    ]))

    elems.append(ptable)

    doc.build(elems)
    return buffer.getvalue()
