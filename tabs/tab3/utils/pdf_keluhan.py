from io import BytesIO
from reportlab.lib.pagesizes import A2
from reportlab.platypus import SimpleDocTemplate, Table, LongTable, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_keluhan(top5, df_phase):

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A2, rightMargin=20, leftMargin=20)
    styles = getSampleStyleSheet()

    elems = []
    elems.append(Paragraph("Top 5 Tipe Keluhan per Produk", styles["Title"]))
    elems.append(Spacer(1, 8))

    # ========================
    # TOP 5 KELUHAN TABLE
    # ========================
    data = [["Produk", "Tipe Keluhan", "Jumlah Tiket"]]

    for _, row in top5.iterrows():
        data.append([
            row["produk_hierarki"],
            row["tipe_keluhan"],
            row["qty_tiket"]
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elems.append(table)
    elems.append(Spacer(1, 12))

    # ========================
    # Rekomendasi & Campaign
    # ========================
    elems.append(Paragraph("Rekomendasi Aksi dan Fokus Campaign", styles["Heading2"]))

    # Kolom HARUS sesuai pdf_revenue
    kolom = [
        "produk_hierarki", "fase_produk", "klasifikasi_keluhan",
        "indikator_pendapatan", "indikator_penggunaan", "indikator_tiket",
        "indikator_csi", "rekomendasi_aksi", "fokus_campaign"
    ]

    dfp = df_phase[kolom].fillna("")

    phdata = [kolom] + dfp.values.tolist()

    ptable = LongTable(phdata, repeatRows=1)
    ptable.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    elems.append(ptable)

    doc.build(elems)
    pdf_val = buffer.getvalue()
    buffer.close()
    return pdf_val
