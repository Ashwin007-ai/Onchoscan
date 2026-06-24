"""
batch_report_generator.py - Updated to use dynamic AI recommendation paragraph.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os, datetime, uuid

def _draw_page_header(canv, doc):
    canv.saveState()
    W, H = letter
    cy = H - 0.45 * inch
    canv.setFillColor(colors.HexColor("#050d15"))
    canv.circle(0.55*inch, cy, 0.22*inch, fill=1, stroke=0)
    canv.setStrokeColor(colors.HexColor("#4fffb0"))
    canv.setLineWidth(1.5)
    canv.circle(0.55*inch, cy, 0.22*inch, fill=0, stroke=1)
    canv.setLineWidth(1.2)
    canv.setStrokeColor(colors.HexColor("#4fffb0"))
    p = canv.beginPath()
    p.moveTo(0.36*inch, cy)
    p.curveTo(0.42*inch, cy+0.09*inch, 0.48*inch, cy-0.09*inch, 0.55*inch, cy)
    p.curveTo(0.62*inch, cy+0.09*inch, 0.68*inch, cy-0.09*inch, 0.74*inch, cy)
    canv.drawPath(p, stroke=1, fill=0)
    canv.setFont("Helvetica-Bold", 11)
    canv.setFillColor(colors.HexColor("#0d1b2a"))
    canv.drawString(0.84*inch, cy-0.04*inch, "OnchoScan")
    canv.setFont("Helvetica", 8)
    canv.setFillColor(colors.HexColor("#5c6b7d"))
    canv.drawRightString(W-0.5*inch, cy-0.04*inch,
                         datetime.datetime.now().strftime("%Y-%m-%d") + "  ·  Batch Report")
    canv.setStrokeColor(colors.HexColor("#1a73e8"))
    canv.setLineWidth(1.0)
    canv.line(0.5*inch, H-0.68*inch, W-0.5*inch, H-0.68*inch)
    canv.setFont("Helvetica", 7)
    canv.setFillColor(colors.HexColor("#5c6b7d"))
    canv.drawCentredString(W/2, 0.4*inch, f"Page {doc.page}")
    canv.restoreState()

def _risk_color(risk_level):
    return {"High Risk":"#c0392b","Medium Risk":"#e67e22","Low Risk":"#27ae60"}.get(risk_level,"#2d3748")

def generate_batch_pdf_report(results, cancer_type):
    os.makedirs("reports", exist_ok=True)
    batch_id  = uuid.uuid4().hex[:8].upper()
    file_path = f"reports/batch_report_{batch_id}.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=letter,
        topMargin=1.0*inch, bottomMargin=0.75*inch,
        leftMargin=0.65*inch, rightMargin=0.65*inch)

    title_s   = ParagraphStyle("BT", fontName="Helvetica-Bold", fontSize=17,
                    textColor=colors.HexColor("#0d1b2a"), alignment=TA_CENTER, spaceAfter=3)
    sub_s     = ParagraphStyle("BS", fontName="Helvetica", fontSize=10,
                    textColor=colors.HexColor("#5c6b7d"), alignment=TA_CENTER, spaceAfter=14)
    head_s    = ParagraphStyle("BH", fontName="Helvetica-Bold", fontSize=12,
                    textColor=colors.HexColor("#0d1b2a"), spaceBefore=14, spaceAfter=6)
    sec_s     = ParagraphStyle("BSec", fontName="Helvetica-Bold", fontSize=13,
                    textColor=colors.HexColor("#1a73e8"), spaceBefore=20, spaceAfter=8)
    body_s    = ParagraphStyle("BB", fontName="Helvetica", fontSize=9.5,
                    textColor=colors.HexColor("#2d3748"), leading=15)
    ai_rec_s  = ParagraphStyle("BAI", fontName="Helvetica", fontSize=9.5,
                    textColor=colors.HexColor("#1a2332"), leading=16)

    story = []
    story.append(Spacer(1, 4))
    story.append(Paragraph("Batch Cancer Screening Report", title_s))
    story.append(Paragraph(f"AI-Assisted Screening · ResNet-18 + Grad-CAM · {len(results)} Scans", sub_s))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1a73e8"), spaceAfter=12))

    high   = sum(1 for r in results if r.get("risk_level")=="High Risk")
    medium = sum(1 for r in results if r.get("risk_level")=="Medium Risk")
    low    = sum(1 for r in results if r.get("risk_level")=="Low Risk")

    meta_rows = [
        ["Generated:",   datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")],
        ["Batch ID:",    batch_id],
        ["Cancer Type:", cancer_type.title()],
        ["Total Scans:", str(len(results))],
        ["High Risk:",   str(high)],
        ["Medium Risk:", str(medium)],
        ["Low Risk:",    str(low)],
    ]
    mt = Table(meta_rows, colWidths=[1.5*inch, 5.0*inch])
    mt.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),9.5),("TEXTCOLOR",(0,0),(-1,-1),colors.HexColor("#2d3748")),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[colors.HexColor("#f8fafc"),colors.white]),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),8),
        ("TEXTCOLOR",(1,4),(1,4),colors.HexColor("#c0392b")),
        ("TEXTCOLOR",(1,5),(1,5),colors.HexColor("#e67e22")),
        ("TEXTCOLOR",(1,6),(1,6),colors.HexColor("#27ae60")),
        ("FONTNAME",(1,4),(1,6),"Helvetica-Bold"),
    ]))
    story.append(mt)
    story.append(Spacer(1, 18))

    story.append(Paragraph("Scan Summary", head_s))
    sum_data = [["#","Filename","Patient","Prediction","Confidence","Risk Level"]]
    for i, r in enumerate(results, 1):
        if r.get("error"):
            sum_data.append([str(i), r.get("filename","?"), "–", "ERROR", "–", "–"])
        else:
            fname = r.get("filename", f"Image {i}")
            if len(fname)>28: fname=fname[:25]+"…"
            patient = r.get("patient_name","–") or "–"
            if len(patient)>14: patient=patient[:13]+"…"
            sum_data.append([str(i),fname,patient,r.get("prediction","–").title(),
                             f"{r.get('confidence',0)}%",r.get("risk_level","–")])
    col_w = [0.3*inch,1.7*inch,1.1*inch,1.1*inch,0.9*inch,1.1*inch]
    st = Table(sum_data, colWidths=col_w)
    sc = [
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0d1b2a")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),
        ("FONTSIZE",(0,0),(-1,-1),8.5),("ALIGN",(0,0),(-1,-1),"CENTER"),("ALIGN",(1,0),(1,-1),"LEFT"),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cbd5e0")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f8fafc"),colors.white]),
    ]
    for i, r in enumerate(results, 1):
        rc = _risk_color(r.get("risk_level",""))
        sc.append(("TEXTCOLOR",(5,i),(5,i),colors.HexColor(rc)))
        sc.append(("FONTNAME",(5,i),(5,i),"Helvetica-Bold"))
    st.setStyle(TableStyle(sc))
    story.append(st)

    for i, r in enumerate(results, 1):
        story.append(PageBreak())
        fname = r.get("filename", f"Image {i}")
        story.append(Paragraph(f"Scan {i} — {fname}", sec_s))
        story.append(HRFlowable(width="100%",thickness=0.8,color=colors.HexColor("#cbd5e0"),spaceAfter=8))

        if r.get("error"):
            story.append(Paragraph(f"<b>Error:</b> {r['error']}", body_s))
            continue

        rc = _risk_color(r.get("risk_level",""))
        pd = [["Prediction","Confidence","Risk Score","Risk Level"],
              [r.get("prediction","–").title(), f"{r.get('confidence',0)}%",
               f"{r.get('risk_score',0)} / 100", r.get("risk_level","–")]]
        pt = Table(pd, colWidths=[1.7*inch,1.4*inch,1.4*inch,1.7*inch])
        pt.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0d1b2a")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("FONTSIZE",(0,0),(-1,-1),9.5),("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#eef2ff")]),
            ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
            ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cbd5e0")),
            ("TEXTCOLOR",(3,1),(3,1),colors.HexColor(rc)),("FONTNAME",(3,1),(3,1),"Helvetica-Bold"),
        ]))
        story.append(pt)
        story.append(Spacer(1,10))

        probs = r.get("class_probabilities",{})
        if probs:
            story.append(Paragraph("Class Probabilities", head_s))
            prob_rows = [["Class","Probability"]] + [
                [cls.title(), f"{pct}%"] for cls,pct in sorted(probs.items(), key=lambda x:-x[1])]
            pbt = Table(prob_rows, colWidths=[3*inch,3.5*inch])
            pbt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1a73e8")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTNAME",(0,1),(-1,-1),"Helvetica"),
                ("FONTSIZE",(0,0),(-1,-1),9),("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f7ff"),colors.white]),
                ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#cbd5e0")),
            ]))
            story.append(pbt)
            story.append(Spacer(1,10))

        story.append(Paragraph("Diagnostic Summary", head_s))
        clean = (r.get("diagnostic_text","").replace("<strong>","").replace("</strong>",""))
        story.append(Paragraph(clean, body_s))

        # ── AI Recommendation (dynamic, unique per scan) ───────────────────
        recommendation = r.get("recommendation","")
        if recommendation:
            story.append(Paragraph("AI-Generated Clinical Recommendation", head_s))
            rp = Paragraph(recommendation.replace("\n", "<br/>"), ai_rec_s)
            rt = Table([[rp]], colWidths=[doc.width])
            rt.setStyle(TableStyle([
                ("BOX",(0,0),(-1,-1),1.2,colors.HexColor("#1a73e8")),
                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f0f7ff")),
                ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
                ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
            ]))
            story.append(rt)
            story.append(Paragraph(
                "<i>Generated by LLaMA 3 (Groq AI) · Based on ResNet-18 prediction patterns</i>",
                ParagraphStyle("BL",fontName="Helvetica-Oblique",fontSize=7.5,
                               textColor=colors.HexColor("#718096"),spaceAfter=4)))

        story.append(Spacer(1,12))

        orig = r.get("original","")
        heat = r.get("heatmap","")
        if orig and os.path.exists(orig) and heat and os.path.exists(heat):
            story.append(Paragraph("Explainable AI Visualization (Grad-CAM)", head_s))
            lt = Table([["Original Image","Grad-CAM Heatmap"]], colWidths=[3.0*inch,3.0*inch])
            lt.setStyle(TableStyle([
                ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),("TEXTCOLOR",(0,0),(-1,-1),colors.HexColor("#5c6b7d")),
                ("BOTTOMPADDING",(0,0),(-1,-1),5),
            ]))
            it = Table([[RLImage(orig,width=2.6*inch,height=2.6*inch),
                         RLImage(heat,width=2.6*inch,height=2.6*inch)]], colWidths=[3.0*inch,3.0*inch])
            it.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
            story.append(KeepTogether([lt,it]))
        elif heat and os.path.exists(heat):
            story.append(Paragraph("Grad-CAM Heatmap", head_s))
            story.append(RLImage(heat,width=2.8*inch,height=2.8*inch))

    story.append(Spacer(1,20))
    story.append(HRFlowable(width="100%",thickness=0.8,color=colors.HexColor("#cbd5e0"),spaceAfter=8))
    story.append(Paragraph(
        "Disclaimer: This batch report is generated by an AI-assisted screening tool and is NOT a "
        "substitute for professional medical diagnosis. Always consult a qualified healthcare professional.",
        ParagraphStyle("D",fontName="Helvetica-Oblique",fontSize=7.5,
                       textColor=colors.HexColor("#718096"),leading=12)))

    doc.build(story, onFirstPage=_draw_page_header, onLaterPages=_draw_page_header)
    return file_path
