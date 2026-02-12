"""Generate the legal digest PDF in the required format."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

from .crawler import LegalNewsItem


def build_pdf(items: list[LegalNewsItem], output_dir: str) -> Path:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    file_path = output / f"legal_digest_{datetime.now().strftime('%Y%m%d')}.pdf"

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        topMargin=2 * mm,
        bottomMargin=2 * mm,
        leftMargin=4 * mm,
        rightMargin=4 * mm,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="DigestBody",
            parent=styles["Normal"],
            fontName="Times-Roman",
            fontSize=12,
            leading=18,
            alignment=TA_JUSTIFY,
            textColor=colors.black,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DigestHeading",
            parent=styles["Heading3"],
            fontName="Times-Bold",
            fontSize=12,
            leading=18,
            textColor=colors.black,
        )
    )

    story = [Paragraph("Daily Legal Digest", styles["DigestHeading"]), Spacer(1, 8)]

    for item in items:
        heading = (
            f"<b><a href='{item.article_url}' color='blue'>{item.title}</a></b>"
            f" | <a href='{item.judgment_pdf_url}' color='blue'>Judgment/Order PDF</a>"
        )
        story.append(Paragraph(heading, styles["DigestHeading"]))
        story.append(Paragraph(f"Court: {item.court}", styles["DigestBody"]))
        story.append(Paragraph(f"Bench: {item.bench}", styles["DigestBody"]))
        judge_line = ", ".join(item.judges) if item.judges else "Not clearly named in source"
        story.append(Paragraph(f"Judges: {judge_line}", styles["DigestBody"]))

        bullets = [ListItem(Paragraph(point, styles["DigestBody"])) for point in item.summary_points]
        story.append(ListFlowable(bullets, bulletType="bullet", leftIndent=12))

        acts = ", ".join(item.act_tags)
        story.append(Paragraph(f"<i>Act(s): {acts}</i>", styles["DigestBody"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    return file_path
