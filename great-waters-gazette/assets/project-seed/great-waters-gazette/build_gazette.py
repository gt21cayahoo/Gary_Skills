from pathlib import Path
import shutil
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "pdf" / "Great_Waters_Gazette_2026-09-29.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "featured-photo.jpg"
CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:Cisterna_Bas%C3%ADlica,_Estambul,_Turqu%C3%ADa,_2024-09-28,_DD_58-60_HDR.jpg"
WEATHER = [
    ("Today", "Sunny (2%)", "87 / 59"),
    ("Wed 30", "Sunny (7%)", "90 / 65"),
    ("Thu 01", "Mostly sunny (11%)", "90 / 69"),
    ("Fri 02", "Partly cloudy (20%)", "90 / 71"),
    ("Sat 03", "Thunderstorms (66%)", "87 / 71"),
]
STORIES = [
    ("AI Story of the Day", "OpenAI shelved its planned GPT-6.1 Astra release after internal tests raised safety and oversight concerns.", "https://www.reuters.com/business/openai-shelves-new-ai-model-after-internal-safety-tests-wsj-reports-2026-09-28/"),
    ("Microsoft 365 Copilot", "Copilot in Excel now links to changed sheets, ranges and charts; use those links to audit edits in context.", "https://learn.microsoft.com/en-us/copilot/microsoft-365/release-notes"),
    ("ChatGPT", "ChatGPT for Word drafts and revises in a sidebar; select text and specify exactly what must stay unchanged.", "https://help.openai.com/en/articles/20001526-chatgpt-for-word"),
    ("Tesla Manufacturing & Expansion", "Giga Nevada marked its six-millionth drive unit as Tesla ramps Semi and Cybercab production.", "https://www.teslabriefing.com/en/articles/product-giga-nevada-6-millionth-drive-unit-2026-09-27"),
    ("Lighting Industry — Story One", "Luminis launched Hollowcore Element, a circular luminous-ring family with a distinctive open interior core.", "https://www.lightdirectory.com/news-Luminis-Launches-Hollowcore-Element-Luminaire-Family.htm"),
    ("Lighting Industry — Story Two", "A $3.6 million NIH-backed trial will test tunable, sensor-led lighting for dementia care in 10 nursing homes.", "https://edisonreport.com/2026/09/28/nih-grant-supports-smart-lighting-research-for-dementia-care/"),
    ("3D Printing News", "AI found six workable settings for NASA's GRCop-42 alloy in 40 trials, including a first 500-watt print.", "https://www.3dnatives.com/en/grcop-42-28092026/"),
    ("Porsche 997 & 911", "A five-year 997.2 Targa 4S ownership review explains why its road-car blend keeps winning long-term loyalty.", "https://www.youtube.com/watch?v=yTkcDDtwvCM"),
    ("AI-Powered Solopreneur Business", "Sell a $1,200 ChatGPT-for-Word proposal sprint to boutique consultancies; validate with three paid-pilot pitches.", "https://help.openai.com/en/articles/20001526-chatgpt-for-word"),
    ("Anna Maria Island News", "Employee complaints resurfaced as Amber LaRowe prepares to become Anna Maria's first city administrator.", "https://amisun.com/employee-complaints-resurface-in-anna-maria/"),
    ("Lake Oconee News", "Truth in Art opens at Steffen Thomas Museum at 4 PM today and runs through Saturday.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events/truth-in-art0929"),
]

def cover(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.saveState()
    clip = c.beginPath(); clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), x - (sw - w) / 2, y - (sh - h) / 2, sw, sh)
    c.restoreState()

def linked_line(c, x, y, body, url, maxw):
    label = "  Read source" if url else ""
    size = 7.3
    while size > 5.8 and stringWidth(body + label, "DVSans", size) > maxw:
        size -= 0.1
    c.setFont("DVSans", size); c.setFillColor(TEXT); c.drawString(x, y, body)
    if url:
        lx = x + stringWidth(body, "DVSans", size)
        c.setFillColor(LINK); c.drawString(lx, y, label)
        c.linkURL(url, (lx, y - 2, lx + stringWidth(label, "DVSans", size), y + size), relative=0)

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True); ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Great Waters Gazette — Tuesday, September 29, 2026"); c.setAuthor("Great Waters Gazette")
    width, height = letter
    c.setFillColor(CREAM); c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold", 28); c.drawCentredString(width / 2, 752, "Great Waters Gazette")
    c.setFont("DVSans", 11); c.drawCentredString(width / 2, 731, "Tuesday, September 29, 2026")
    left, right, top = 40, 572, 704
    weather_width, gap = 195, 16; photo_x = left + weather_width + gap; photo_width = right - photo_x
    c.setFont("DVSansBold", 13); c.drawString(left, top, "ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left, top - 6, left + weather_width, top - 6)
    y = top - 25
    for day, condition, temps in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold", 8.1); c.drawString(left, y, day)
        c.setFont("DVSans", 6.8); c.drawString(left + 47, y, condition); c.drawRightString(left + weather_width, y, temps); y -= 16
    c.setFillColor(LINK); c.setFont("DVSans", 7.3)
    weather_label = "Weather Channel — 5:56 AM EDT"; c.drawString(left, y - 1, weather_label)
    c.linkURL(WEATHER_URL, (left, y - 3, left + stringWidth(weather_label, "DVSans", 7.3), y + 8), relative=0)
    cover(c, PHOTO, photo_x, 570, photo_width, 134); c.linkURL(PHOTO_URL, (photo_x, 570, right, 704), relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans", 6.8); c.drawString(photo_x, 559, "Yesterday's Picture: Basilica Cistern, Istanbul, Turkey.")
    c.setFillColor(LINK); credit = "Diego Delso, delso.photo / CC BY-SA 4.0 (cropped)"; c.drawString(photo_x, 549, credit)
    c.linkURL(PHOTO_URL, (photo_x, 547, photo_x + stringWidth(credit, "DVSans", 6.8), 558), relative=0)
    c.setFillColor(NAVY); c.roundRect(left, 509, right - left, 31, 4, stroke=1, fill=0)
    c.setFont("DVSansBold", 9); c.drawString(left + 8, 528, "Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique", 7.4)
    practice = "Before chasing more today, name the one small need that truly matters—and meet only that."
    c.drawString(left + 8, 516, practice); c.setFillColor(LINK); c.drawRightString(right - 8, 516, "Daily Stoic")
    c.linkURL("https://dailystoic.com/podcast/", (right - 66, 514, right - 8, 524), relative=0)
    y = 486
    for heading, summary, url in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold", 9.5); c.drawString(left, y, heading)
        c.setStrokeColor(NAVY); c.line(left, y - 3, right, y - 3)
        linked_line(c, left + 3, y - 16, summary, url, right - left - 3); y -= 40
    c.setFillColor(NAVY); c.setFont("DVSansOblique", 7)
    c.drawCentredString(width / 2, 25, "A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); shutil.copyfile(OUT, ARCHIVE); print(OUT)

if __name__ == "__main__":
    build()
