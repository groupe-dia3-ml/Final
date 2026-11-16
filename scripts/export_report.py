"""Export the final Markdown report as a paginated PDF with embedded figures."""

import re
from html import escape
from pathlib import Path

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/FINAL_REPORT.md"
OUTPUT = ROOT / "output/pdf/FINAL_REPORT.pdf"
INK = colors.HexColor("#18334a")
MUTED = colors.HexColor("#596978")
FONT_DIR = Path(reportlab.__file__).parent / "fonts"


def setup_styles():
    for name, filename in [
        ("Vera", "Vera.ttf"),
        ("VeraBold", "VeraBd.ttf"),
        ("VeraItalic", "VeraIt.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(name, FONT_DIR / filename))
    pdfmetrics.registerFontFamily(
        "Vera",
        normal="Vera",
        bold="VeraBold",
        italic="VeraItalic",
        boldItalic="VeraBold",
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "Body",
            fontName="Vera",
            fontSize=9.5,
            leading=14.5,
            spaceAfter=8,
            textColor=INK,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            "ReportTitle",
            parent=styles["Body"],
            fontName="VeraBold",
            fontSize=23,
            leading=29,
            spaceAfter=16,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "Section",
            parent=styles["Body"],
            fontName="VeraBold",
            fontSize=14,
            leading=19,
            spaceBefore=13,
            spaceAfter=8,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle("Subsection", parent=styles["Section"], fontSize=11, leading=16)
    )
    styles.add(
        ParagraphStyle(
            "Cell", parent=styles["Body"], fontSize=7.5, leading=10.5, spaceAfter=0
        )
    )
    styles.add(
        ParagraphStyle(
            "CellHead",
            parent=styles["Cell"],
            fontName="VeraBold",
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            "Caption", parent=styles["Body"], fontSize=9, leading=13, textColor=MUTED
        )
    )
    styles.add(
        ParagraphStyle(
            "CodeBlock",
            parent=styles["Body"],
            fontName="Courier",
            fontSize=8.1,
            leading=12,
            backColor=colors.HexColor("#f0f4f7"),
            borderPadding=8,
        )
    )
    return styles


def inline(text):
    text = text.translate(str.maketrans({"−": "-", "–": "-", "—": "-", "‑": "-"}))
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r'<font color="#245478">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    def link(match):
        label, target = match.groups()
        if target.startswith("https://"):
            return f'<link href="{target}" color="#245478"><u>{label}</u></link>'
        return label

    return re.sub(r"\[([^]]+)\]\(([^)]+)\)", link, text)


def footer(canvas, doc):
    width, height = canvas._pagesize
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cbd5de"))
    canvas.line(42, 36, width - 42, 36)
    canvas.setFont("Vera", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(42, 23, "ESILV A4 DIA3 | Diabetes status and noise robustness")
    canvas.drawRightString(width - 42, 23, str(doc.page))
    if doc.page > 1:
        canvas.setFont("Vera", 7)
        canvas.drawString(
            42, height - 25, "Machine Learning final project | Experimental results"
        )
    canvas.restoreState()


def table_flow(lines, styles, width):
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines
    ]
    rows = [
        row
        for row in rows
        if not all(re.fullmatch(r":?-+:?", cell.replace(" ", "")) for cell in row)
    ]
    columns = len(rows[0])
    first = width * (0.29 if columns >= 5 else 0.33)
    widths = [first] + [(width - first) / (columns - 1)] * (columns - 1)
    cells = [
        [
            Paragraph(inline(cell), styles["CellHead" if index == 0 else "Cell"])
            for cell in row
        ]
        for index, row in enumerate(rows)
    ]
    table = Table(
        cells,
        colWidths=widths,
        repeatRows=1,
        hAlign="LEFT",
        spaceBefore=7,
        spaceAfter=12,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.HexColor("#f0f4f7"), colors.white],
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#cbd5de")),
            ]
        )
    )
    return table


def build():
    styles = setup_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        title="Diabetes status classification and controlled noise robustness",
        author="Louis Le Forestier and Team - ESILV A4 DIA3",
        leftMargin=42,
        rightMargin=42,
        topMargin=45,
        bottomMargin=49,
    )
    portrait = Frame(
        42,
        49,
        A4[0] - 84,
        A4[1] - 94,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    wide_size = landscape(A4)
    wide = Frame(
        42,
        49,
        wide_size[0] - 84,
        wide_size[1] - 94,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="portrait", frames=portrait, pagesize=A4, onPage=footer),
            PageTemplate(id="figure", frames=wide, pagesize=wide_size, onPage=footer),
        ]
    )
    lines = SOURCE.read_text().splitlines()
    story = []
    index = 0
    figure_number = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            code = []
            while index < len(lines) and not lines[index].startswith("```"):
                code.append(lines[index])
                index += 1
            story.append(Preformatted("\n".join(code), styles["CodeBlock"]))
            story.append(Spacer(1, 10))
        elif line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(table_flow(table_lines, styles, A4[0] - 84))
            continue
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[([^]]+)\]\(([^)]+)\)", line)
            if match is None:
                raise ValueError(f"Invalid image reference: {line}")
            caption, relative = match.groups()
            figure_number += 1
            story.extend(
                [
                    NextPageTemplate("figure"),
                    PageBreak(),
                    Paragraph(
                        f"Figure {figure_number}. {inline(caption)}", styles["Section"]
                    ),
                    Spacer(1, 12),
                ]
            )
            image = Image(str(SOURCE.parent / relative))
            scale = min(
                (wide_size[0] - 84) / image.imageWidth,
                (wide_size[1] - 195) / image.imageHeight,
            )
            image.drawWidth = image.imageWidth * scale
            image.drawHeight = image.imageHeight * scale
            image.hAlign = "CENTER"
            story.extend(
                [
                    image,
                    Spacer(1, 15),
                    Paragraph(
                        "Source: saved experiment outputs from the accompanying repositories. "
                        "Definitions, numerical results and uncertainty limits are given in the adjacent report sections.",
                        styles["Caption"],
                    ),
                    NextPageTemplate("portrait"),
                    PageBreak(),
                ]
            )
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            style = (
                "ReportTitle"
                if level == 1
                else "Section"
                if level == 2
                else "Subsection"
            )
            story.append(Paragraph(inline(line[level:].strip()), styles[style]))
        else:
            paragraph = [line]
            index += 1
            while (
                index < len(lines)
                and lines[index].strip()
                and not lines[index].startswith(("#", "|", "![", "```"))
                and not re.match(r"^\d+\. ", lines[index])
            ):
                paragraph.append(lines[index].strip())
                index += 1
            story.append(Paragraph(inline(" ".join(paragraph)), styles["Body"]))
            continue
        index += 1
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
