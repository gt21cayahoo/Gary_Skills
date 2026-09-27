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
OUT = ROOT / "output" / "pdf" / "Great_Waters_Gazette_2026-09-27.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "featured-photo.jpg"
CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL = "https://weather.com/us/georgia/city/eatonton/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:002_Jabiru_feeding_its_babies_in_their_nest_in_Encontro_das_%C3%81guas_State_Park_Photo_by_Giles_Laurent.jpg"
WEATHER = [
    ("Today", "Sunny (2%)", "85 / 54"),
    ("Mon 28", "Sunny (5%)", "86 / 55"),
    ("Tue 29", "Sunny (6%)", "89 / 60"),
    ("Wed 30", "Sunny (8%)", "91 / 64"),
    ("Thu 01", "Mostly sunny (13%)", "91 / 69"),
]
STORIES = [
    ("AI Story of the Day", "Anthropic committed $11.6 billion to Akamai for seven years of distributed CPU cloud capacity.", "https://www.akamai.com/newsroom/press-release/akamai-announces-11-6-billion-multi-year-agreement-with-anthropic-to-support-growing-demand"),
    ("Microsoft 365 Copilot", "New Copilot adds Home, Code and Autopilot; use Home to resume recent work without rebuilding context.", "https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/"),
    ("ChatGPT", "Security history now lists sign-ins and authentication changes; review it under Settings > Security and login.", "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
    ("Tesla Manufacturing & Expansion", "Tesla opened its Sparks factory for high-volume Semi production, targeting 50,000 trucks yearly.", "https://electrek.co/2026/09/25/tesla-semi-volume-production-launch-nevada-factory/"),
    ("Lighting Industry — Story One", "Massachusetts, New York and Washington now recognize DLC LUNA as an outdoor-lighting compliance path.", "https://edisonreport.com/2026/09/24/states-are-choosing-luna-heres-why-that-matters/"),
    ("Lighting Industry — Story Two", "Precise LED pairs 1.5-inch downlights with remote drivers and custom curved linear fixtures.", "https://edisonreport.com/2026/09/24/precise-leds-birgit-collins-on-1-5-downlights-the-new-wave-fixture-and-a-career-built-on-custom-lighting/"),
    ("3D Printing News", "Phrozen's Revo MAX combines a 14-inch 16K panel, dual heating and a 2-liter vat for large resin jobs.", "https://www.3dnatives.com/en/phrozen-sonic-mighty-revo-16k-max-22092026/"),
    ("Porsche 997 & 911", "No worthwhile unused standard 997 road-car item passed the verified three-month access and recency checks.", ""),
    ("AI-Powered Solopreneur Business", "Sell a $1,500 Copilot FinOps setup to 10–50-person firms; validate it with two IT-manager calls.", "https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/"),
    ("Anna Maria Island News", "Manatee County detectives identified the victim in a September 18 drowning near Passage Key.", "https://www.islander.org/2026/09/passage-key-drowning-victim-indentified/"),
    ("Lake Oconee News", "Table at the Lake hosts a PlumpJack dinner with four Napa producers tonight from 5:30 to 9:30.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events/plumpjack-collection-wine-dinner0927"),
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

def linked_line(c, x, y, text, url, maxw):
    label = "  Read source" if url else ""
    size = 7.3
    while size > 6.0 and stringWidth(text + label, "DVSans", size) > maxw:
        size -= 0.1
    c.setFont("DVSans", size); c.setFillColor(TEXT); c.drawString(x, y, text)
    if url:
        lx = x + stringWidth(text, "DVSans", size)
        c.setFillColor(LINK); c.drawString(lx, y, label)
        c.linkURL(url, (lx, y - 2, lx + stringWidth(label, "DVSans", size), y + size), relative=0)

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True); ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    width, height = letter
    c.setTitle("Great Waters Gazette — Sunday, September 27, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold", 28); c.drawCentredString(width / 2, 752, "Great Waters Gazette")
    c.setFont("DVSans", 11); c.drawCentredString(width / 2, 731, "Sunday, September 27, 2026")
    left, right, top = 40, 572, 704
    weather_width, gap = 195, 16; photo_x = left + weather_width + gap; photo_width = right - photo_x
    c.setFont("DVSansBold", 13); c.drawString(left, top, "ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left, top - 6, left + weather_width, top - 6)
    y = top - 25
    for day, condition, temps in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold", 8.1); c.drawString(left, y, day)
        c.setFont("DVSans", 6.8); c.drawString(left + 47, y, condition); c.drawRightString(left + weather_width, y, temps); y -= 16
    c.setFillColor(LINK); c.setFont("DVSans", 7.3)
    weather_label = "Weather Channel — 6:02 AM EDT"; c.drawString(left, y - 1, weather_label)
    c.linkURL(WEATHER_URL, (left, y - 3, left + stringWidth(weather_label, "DVSans", 7.3), y + 8), relative=0)
    cover(c, PHOTO, photo_x, 570, photo_width, 134); c.linkURL(PHOTO_URL, (photo_x, 570, right, 704), relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans", 6.8); c.drawString(photo_x, 559, "Yesterday's Picture: Jabiru feeding its chicks in Mato Grosso, Brazil.")
    c.setFillColor(LINK); credit = "© Giles Laurent / CC BY-SA 4.0 (cropped)"; c.drawString(photo_x, 549, credit)
    c.linkURL(PHOTO_URL, (photo_x, 547, photo_x + stringWidth(credit, "DVSans", 6.8), 558), relative=0)
    c.setFillColor(NAVY); c.roundRect(left, 509, right - left, 31, 4, stroke=1, fill=0)
    c.setFont("DVSansBold", 9); c.drawString(left + 8, 528, "Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique", 7.4)
    practice = "Measure the day by steadiness, not comfort: accept one loss, then do the next right thing."
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
