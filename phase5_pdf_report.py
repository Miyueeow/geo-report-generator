"""
Phase 5: PDF Report Generation
Combines the map (as a static image), key stats, and AI narrative
into one polished PDF report.
"""

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib import colors

# ---- CONFIG ----
DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"
ANALYSIS_FILE = "analysis_results.json"
NARRATIVE_FILE = "narrative.txt"
MAP_IMAGE_FILE = "map_screenshot.png"  # see note below
REPORT_FILENAME = "geo_report.pdf"


def load_data():
    with open(os.path.join(DATA_FOLDER, ANALYSIS_FILE), "r") as f:
        analysis = json.load(f)
    with open(os.path.join(DATA_FOLDER, NARRATIVE_FILE), "r", encoding="utf-8") as f:
        narrative = f.read()
    return analysis, narrative


def build_pdf(analysis: dict, narrative: str):
    filepath = os.path.join(OUTPUT_FOLDER, REPORT_FILENAME)
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm,
                             leftMargin=2*cm, rightMargin=2*cm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle", parent=styles["Normal"], fontSize=12,
        textColor=colors.grey, alignment=TA_CENTER, spaceAfter=20
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["Normal"], fontSize=10.5, leading=16
    )

    elements = []

    # ---- Title ----
    elements.append(Paragraph("Geospatial Area Report", title_style))
    elements.append(Paragraph(analysis["region"], subtitle_style))

    # ---- Map image (optional, only if it exists) ----
    map_path = os.path.join(DATA_FOLDER, MAP_IMAGE_FILE)
    if os.path.exists(map_path):
        elements.append(Image(map_path, width=16*cm, height=10*cm))
        elements.append(Spacer(1, 12))
    else:
        elements.append(Paragraph(
            "<i>(Map screenshot not found — see note in script comments)</i>",
            body_style
        ))
        elements.append(Spacer(1, 12))

    # ---- Key Stats Table ----
    elements.append(Paragraph("Key Statistics", heading_style))

    stats_data = [
        ["Metric", "Value"],
        ["Area", f"{analysis['area_km2']} km²"],
        ["Total Points of Interest", str(analysis["total_pois"])],
        ["Distinct Categories", str(analysis["diversity"]["total_distinct_categories"])],
        ["Intersection Density", f"{analysis['walkability']['intersection_density_per_km2']} per km²"],
        ["Total Street Length", f"{analysis['walkability']['total_street_length_km']} km"],
        ["Street Density", f"{analysis['walkability']['street_density_km_per_km2']} km per km²"],
    ]

    table = Table(stats_data, colWidths=[8*cm, 8*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
    ]))
    elements.append(table)

    # ---- Top 5 Categories Table ----
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Top 5 Points of Interest Categories", heading_style))

    top5_data = [["Category", "Count"]] + [
        [item["category"], str(item["count"])]
        for item in analysis["diversity"]["top_5_categories"]
    ]
    top5_table = Table(top5_data, colWidths=[8*cm, 8*cm])
    top5_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
    ]))
    elements.append(top5_table)

    # ---- AI Narrative ----
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Analysis & Insights", heading_style))

    for paragraph in narrative.strip().split("\n"):
        if paragraph.strip():
            elements.append(Paragraph(paragraph.strip(), body_style))
            elements.append(Spacer(1, 8))

    # ---- Footer note ----
    elements.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        "FooterStyle", parent=styles["Normal"], fontSize=8,
        textColor=colors.grey, alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "Generated automatically using OpenStreetMap data and AI-assisted analysis.",
        footer_style
    ))

    doc.build(elements)
    print(f"PDF report saved to: {filepath}")


if __name__ == "__main__":
    print("Loading data...")
    analysis, narrative = load_data()

    print("Building PDF report...")
    build_pdf(analysis, narrative)