"""Build the one-page clinician orientation PDF using ReportLab.

Run from any directory with ``python tools/downloads/build_clinician_handout.py``.
The PDF is a general educational handout, not an individualized emergency plan.
Content and evidence decisions are documented in the Module 5 Audit 1 report.
The layout deliberately reserves three ruled lines for the patient's own notes.
"""
from pathlib import Path

import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

# Embed ReportLab's bundled fonts so printer/viewer substitution cannot distort spacing.
FONT_DIR = Path(reportlab.__file__).resolve().parent / "fonts"
for name, filename in (("Handout", "Vera.ttf"), ("Handout-Bold", "VeraBd.ttf"),
                       ("Handout-Italic", "VeraIt.ttf"), ("Handout-BoldItalic", "VeraBI.ttf")):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily("Handout", normal="Handout", bold="Handout-Bold",
                             italic="Handout-Italic", boldItalic="Handout-BoldItalic")

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/downloads/meeting-a-person-with-fnd-clinician-handout.pdf"
INK = colors.HexColor("#193b52")
GOLD = colors.HexColor("#bd8a2e")
BODY = ParagraphStyle("Body", fontName="Handout", fontSize=12, leading=15,
                      textColor=INK, alignment=TA_LEFT)
SMALL = ParagraphStyle("Source", parent=BODY, fontSize=9, leading=11.5)

# Numbers refer to the short clinical references printed on the same page.
SECTIONS = [
    ("Listen and make communication possible",
     "Speak directly to the person. They may hear and understand while unable to speak or respond. "
     "Ask what helps; offer time, writing or another communication method, and less light or noise "
     "where helpful. Invite supporter observations with permission. [1, 2]"),
    ("Recognise genuine, variable symptoms",
     "Functional neurological disorder (FND) causes real, involuntary symptoms affecting movement, "
     "sensation, speech, cognition or episodes of altered awareness. Diagnosis uses positive clinical "
     "features; normal tests alone are insufficient. Psychological stress is not required. "
     "Improved function in one setting can coexist with substantial everyday disability. [1]"),
    ("Assess this presentation on its own merits",
     "Compare today with the medically assessed pattern. FND can coexist with migraine, epilepsy "
     "and other illnesses: each deserves appropriate care. Assess changed symptoms, injury "
     "and physiological stability. Suspected stroke, severe breathing difficulty or ongoing "
     "unresponsiveness requires immediate emergency assessment. [1, 3]"),
    ("Use proportionate care for functional seizures",
     "Follow the individual plan for a familiar, confirmed functional event while reassessing "
     "unexpected changes. Protect from injury and use calm communication. Avoid restraint and painful "
     "attempts to stop an event. Benzodiazepines and antiseizure medicines require another clinical "
     "indication, such as coexisting epilepsy; they are not indicated for functional seizures alone. [2, 3]"),
    ("Leave a clear next step",
     "Explain the assessment and agree what happens next, who will follow up and when reassessment "
     "is needed. Ask about everyday function, safe mobility and the help actually available. "
     "Rehabilitation and practical accommodations can support participation alongside ongoing care. [1, 2]"),
]
REFERENCES = [
    '1. Bennett et al. <i>Clin Med</i> (2021). doi:10.7861/clinmed.2020-0987',
    '2. Tolchin et al. AAN functional-seizure guideline. <i>Neurology</i> (2026).<br/>doi:10.1212/WNL.0000000000214466',
    '3. Mcloughlin et al. Iatrogenic harm in FND. <i>Brain</i> (2025). doi:10.1093/brain/awae283',
]


def paragraph(canvas: Canvas, text: str, y: float, style: ParagraphStyle) -> float:
    """Draw wrapped text within the printable width and return its lower edge."""
    p = Paragraph(text, style)
    _, height = p.wrap(516, 792)
    p.drawOn(canvas, 48, y - height)
    return y - height


def main() -> None:
    """Create a deterministic single-page PDF and fail on content overflow."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = Canvas(str(OUTPUT), pagesize=letter, pageCompression=1, invariant=1)
    c.setTitle("Meeting a person with FND - clinician orientation")
    c.setAuthor("FND Education Project")
    c.setSubject("General clinical education; reviewed sources and patient notes")
    c.setFillColor(INK)
    c.setFont("Handout-Bold", 9)
    c.drawString(48, 752, "FND EDUCATION PROJECT")
    c.setFont("Handout-Bold", 21)
    c.drawString(48, 724, "Meeting a person with FND")
    c.setFont("Handout", 10)
    c.drawString(48, 706, "A one-page clinical orientation for an unfamiliar encounter")
    c.setStrokeColor(GOLD)
    c.line(48, 696, 564, 696)
    y = 678
    for heading, text in SECTIONS:
        c.setFont("Handout-Bold", 12)
        c.setFillColor(INK)
        c.drawString(48, y, heading)
        y = paragraph(c, text, y - 7, BODY) - 16
    y = paragraph(c, "<b>Clinical references</b>", y + 3, SMALL) - 3
    for reference in REFERENCES:
        y = paragraph(c, reference, y, SMALL)
    # A hard boundary prevents an unnoticed second page or overlap with notes.
    if y < 170:
        raise ValueError(f"Content reaches {y:.1f} pt; shorten text to preserve notes.")
    c.setFillColor(INK)
    c.setFont("Handout-Bold", 11.5)
    c.drawString(48, 151, "What I would like the clinician to know")
    c.setFont("Handout", 9)
    c.drawString(48, 137, "My symptoms, communication needs, other conditions or questions:")
    c.setStrokeColor(colors.HexColor("#aebcc5"))
    for baseline in (116, 95, 74):
        c.line(48, baseline, 564, baseline)
    c.setFont("Handout", 10)
    c.drawString(48, 51, "For more free FND education, visit https://fndeducationproject.org")
    c.linkURL("https://fndeducationproject.org", (48, 48, 564, 62), relative=0)
    c.setFont("Handout", 8)
    c.drawString(48, 29, "General education; individual assessment and care remain with the treating team. Updated 25 Oct 2026.")
    c.showPage()
    c.save()
    print(f"Built {OUTPUT.relative_to(ROOT)}; references end at {y:.1f} pt.")


if __name__ == "__main__":
    main()
