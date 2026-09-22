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
OUT = ROOT / "output" / "pdf" / "Great_Waters_Gazette_2026-09-22.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "featured-photo.png"
CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:The_Blue_Marble,_AS17-148-22727.png"
WEATHER = [
    ("Today", "PM thunderstorms (43%)", "90 / 70"),
    ("Wed 23", "Cloudy (24%)", "80 / 62"),
    ("Thu 24", "Cloudy (24%)", "73 / 57"),
    ("Fri 25", "Mostly sunny (5%)", "79 / 54"),
    ("Sat 26", "Mostly sunny (4%)", "83 / 54"),
]
STORIES = [
    ("AI Story of the Day", "Alibaba unveiled its Zhenwu V900 AI chip and plans a 5–10-trillion-parameter model.", "https://apnews.com/article/b29908e516faff9f5a82b201ba954aab"),
    ("Microsoft 365 Copilot", "Copilot unifies work and personal use while keeping account data separate; verify the active account first.", "https://copilot.com/"),
    ("ChatGPT", "ChatGPT Work creates and edits finished documents; ask for the artifact plus a source-and-layout check.", "https://chatgpt.com/overview/"),
    ("Tesla Manufacturing & Expansion", "A California trial opened over alleged discrimination at Tesla's Fremont assembly plant.", "https://www.reuters.com/legal/government/tesla-faces-major-trial-alleged-bias-against-black-workers-after-years-lawsuits-2026-09-21/"),
    ("Lighting Industry — Story One", "DLFNY extended Beacon Awards entries and sponsorships for New York lighting design.", "https://edisonreport.com/2026/09/17/dlfny-announces-final-call-for-3rd-annual-beacon-awards-submissions-and-sponsors/"),
    ("Lighting Industry — Story Two", "No second worthwhile, non-repeated lighting story met the seven-day publication cutoff.", ""),
    ("3D Printing News", "XYZO launched a hybrid platform combining DLP, FDM or pellets with machining and inspection.", "https://www.tctmagazine.com/xyzo-launches-hybrid-manufacturing-system-that-can-integrate-dlp-fdm-or-pellet-extrusion/"),
    ("Porsche 997 & 911", "No worthwhile unused standard 997 road-car item remains in the verified three-month queue.", ""),
    ("AI-Powered Solopreneur Business", "Sell a $1,500 AI-copyright readiness audit to Australian creative agencies; validate with two buyers.", "https://www.reuters.com/legal/litigation/anthropic-openai-call-australia-relax-ban-training-ai-models-2026-09-22/"),
    ("Anna Maria Island News", "Turtle Watch reported continuing hatchling disorientations with about six weeks left in nesting season.", "https://www.islander.org/2026/09/nesting-notes-disorientations-continue/"),
    ("Lake Oconee News", "The Concert Truck brings a free mobile live-music program to Lakeside Church at 7 tonight.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events/opas-pop-up-series-the-concert-truck-returns0922"),
]


def cover(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), x - (sw - w) / 2, y - (sh - h) / 2, sw, sh)
    c.restoreState()


def linked_line(c, x, y, text, url, maxw):
    label = "  Read source" if url else ""
    size = 7.3
    while size > 6.1 and stringWidth(text + label, "DVSans", size) > maxw:
        size -= 0.1
    c.setFont("DVSans", size)
    c.setFillColor(TEXT)
    c.drawString(x, y, text)
    if url:
        lx = x + stringWidth(text, "DVSans", size)
        c.setFillColor(LINK)
        c.drawString(lx, y, label)
        c.linkURL(url, (lx, y - 2, lx + stringWidth(label, "DVSans", size), y + size), relative=0)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    width, height = letter
    c.setTitle("Great Waters Gazette — Tuesday, September 22, 2026")
    c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont("DVSansBold", 28)
    c.drawCentredString(width / 2, 752, "Great Waters Gazette")
    c.setFont("DVSans", 11)
    c.drawCentredString(width / 2, 731, "Tuesday, September 22, 2026")

    left, right, top = 40, 572, 704
    weather_width, gap = 195, 16
    photo_x = left + weather_width + gap
    photo_width = right - photo_x
    c.setFont("DVSansBold", 13)
    c.drawString(left, top, "ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY)
    c.line(left, top - 6, left + weather_width, top - 6)
    y = top - 25
    for day, condition, temps in WEATHER:
        c.setFillColor(TEXT)
        c.setFont("DVSansBold", 8.1)
        c.drawString(left, y, day)
        c.setFont("DVSans", 6.8)
        c.drawString(left + 47, y, condition)
        c.drawRightString(left + weather_width, y, temps)
        y -= 16
    c.setFillColor(LINK)
    c.setFont("DVSans", 7.3)
    weather_label = "Weather Channel — 6:17 AM EDT"
    c.drawString(left, y - 1, weather_label)
    c.linkURL(WEATHER_URL, (left, y - 3, left + stringWidth(weather_label, "DVSans", 7.3), y + 8), relative=0)

    cover(c, PHOTO, photo_x, 570, photo_width, 134)
    c.linkURL(PHOTO_URL, (photo_x, 570, right, 704), relative=0)
    c.setFillColor(TEXT)
    c.setFont("DVSans", 6.8)
    c.drawString(photo_x, 559, "Yesterday's Picture: The Blue Marble from Apollo 17.")
    c.setFillColor(LINK)
    credit = "Harrison Schmitt / NASA / Public domain (cropped)"
    c.drawString(photo_x, 549, credit)
    c.linkURL(PHOTO_URL, (photo_x, 547, photo_x + stringWidth(credit, "DVSans", 6.8), 558), relative=0)

    c.setFillColor(NAVY)
    c.roundRect(left, 509, right - left, 31, 4, stroke=1, fill=0)
    c.setFont("DVSansBold", 9)
    c.drawString(left + 8, 528, "Today's Stoic Practice")
    c.setFillColor(TEXT)
    c.setFont("DVSansOblique", 7.4)
    practice = "Choose one duty, do it without complaint, then let the result belong to the day."
    c.drawString(left + 8, 516, practice)
    c.setFillColor(LINK)
    c.drawRightString(right - 8, 516, "Daily Stoic")
    c.linkURL("https://dailystoic.com/podcast/", (right - 66, 514, right - 8, 524), relative=0)

    y = 486
    for heading, summary, url in STORIES:
        c.setFillColor(TEXT)
        c.setFont("DVSansBold", 9.5)
        c.drawString(left, y, heading)
        c.setStrokeColor(NAVY)
        c.line(left, y - 3, right, y - 3)
        linked_line(c, left + 3, y - 16, summary, url, right - left - 3)
        y -= 40

    c.setFillColor(NAVY)
    c.setFont("DVSansOblique", 7)
    c.drawCentredString(width / 2, 25, "A concise morning digest — sources linked in every section")
    c.showPage()
    c.save()
    shutil.copyfile(OUT, ARCHIVE)
    print(OUT)


if __name__ == "__main__":
    build()
