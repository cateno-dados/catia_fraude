"""Reusable python-docx helpers for specification documents.

Import this module from a custom spec script:

    import sys
    sys.path.insert(0, r"<skill_dir>/lib")
    from spec_helpers import (
        Doc, AZUL, CINZA, BRANCO,
        add_heading, add_para, add_bullets, add_table, add_callout, add_image,
        cover, version_table, summary,
    )

Style choices kept minimal and neutral so the output looks clean in any
corporate context (blue headings, gray subtitles, light blue table headers,
zebra rows). Override colors and font by editing the constants below.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor

AZUL = RGBColor(0x1F, 0x4E, 0x79)
CINZA = RGBColor(0x44, 0x44, 0x44)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)


def Doc():
    """Return a new Document with sane defaults (Calibri 11, 2 cm margins)."""
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.2)
        section.right_margin = Cm(2.2)
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    return doc


def shade(cell, color_hex: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def add_heading(doc, text: str, level: int = 1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = AZUL
    return h


def add_para(doc, text: str, bold: bool = False, italic: bool = False, size: int = 11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    return p


def add_bullets(doc, items: Iterable[str]) -> None:
    for it in items:
        doc.add_paragraph(it, style="List Bullet")


def add_table(
    doc,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    widths_cm: Sequence[float] | None = None,
    header_color: str = "1F4E79",
    zebra: bool = True,
):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(h)
        run.bold = True
        run.font.color.rgb = BRANCO
        run.font.size = Pt(10)
        shade(hdr[i], header_color)
        hdr[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for r_idx, row in enumerate(rows):
        cells = table.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(str(v))
            run.font.size = Pt(10)
            if zebra and r_idx % 2 == 1:
                shade(cells[i], "F2F2F2")
    if widths_cm:
        for row in table.rows:
            for i, w in enumerate(widths_cm):
                row.cells[i].width = Cm(w)
    return table


def add_callout(doc, title: str, body: str, fill: str = "DDF0DD", border: str = "548235") -> None:
    t = doc.add_table(rows=1, cols=1)
    cell = t.rows[0].cells[0]
    cell.text = ""
    shade(cell, fill)
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "14")
        el.set(qn("w:color"), border)
        tc_borders.append(el)
    tc_pr.append(tc_borders)
    p1 = cell.paragraphs[0]
    r1 = p1.add_run(title)
    r1.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = RGBColor(0x54, 0x82, 0x35)
    p2 = cell.add_paragraph()
    r2 = p2.add_run(body)
    r2.font.size = Pt(11)
    doc.add_paragraph()


def add_image(doc, path: str | Path, width_cm: float, caption: str | None = None) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(caption)
        r.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = CINZA


def cover(doc, title: str, subtitle: str = "", subtitle2: str = "", subtitle3: str = "") -> None:
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap.add_run("\n\n\n" + title)
    r.bold = True
    r.font.size = Pt(28)
    r.font.color.rgb = AZUL
    if subtitle:
        sub = doc.add_paragraph()
        sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rs = sub.add_run(subtitle)
        rs.bold = True
        rs.font.size = Pt(20)
        rs.font.color.rgb = CINZA
    if subtitle2:
        sub2 = doc.add_paragraph()
        sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rs2 = sub2.add_run(subtitle2)
        rs2.font.size = Pt(14)
        rs2.font.color.rgb = CINZA
    if subtitle3:
        sub3 = doc.add_paragraph()
        sub3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rs3 = sub3.add_run(subtitle3)
        rs3.italic = True
        rs3.font.size = Pt(13)
        rs3.font.color.rgb = CINZA


def metadata_block(doc, rows: Sequence[tuple[str, str]]) -> None:
    """Two-column metadata table used right after the cover."""
    doc.add_paragraph("\n\n\n\n")
    meta = doc.add_table(rows=len(rows), cols=2)
    meta.style = "Light List Accent 1"
    for i, (k, v) in enumerate(rows):
        c1, c2 = meta.rows[i].cells
        c1.text = ""
        c2.text = ""
        rk = c1.paragraphs[0].add_run(k)
        rk.bold = True
        rk.font.size = Pt(11)
        c2.paragraphs[0].add_run(v).font.size = Pt(11)
        c1.width = Cm(3.5)
        c2.width = Cm(12.5)


def version_table(doc, rows: Sequence[tuple[str, str, str, str]]) -> None:
    """Version, Date, Author, Notes table."""
    add_heading(doc, "Controle de versão", level=1)
    add_table(
        doc,
        ["Versão", "Data", "Autor", "Alterações"],
        rows,
        widths_cm=[2.0, 2.2, 3.0, 8.8],
    )


def summary(doc, items: Sequence[str]) -> None:
    add_heading(doc, "Sumário", level=1)
    for item in items:
        doc.add_paragraph(item)
    doc.add_page_break()
