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
OUT = ROOT / "output" / "pdf" / "Great_Waters_Gazette_2026-09-28.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "featured-photo.webp"
CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:Gladiolus_dalenii_flower_Ooty_Jul25_A7CR_06187-224_zsp.jpg"
WEATHER = [
    ("Today", "Sunny (2%)", "85 / 55"),
    ("Tue 29", "Sunny (5%)", "88 / 60"),
    ("Wed 30", "Mostly sunny (8%)", "90 / 64"),
    ("Thu 01", "Sunny (8%)", "90 / 68"),
    ("Fri 02", "Partly cloudy (24%)", "90 / 72"),
]
STORIES = [
    ("AI Story of the Day", "Bill Gates called unmonitored AI irresponsible and urged legal safeguards against catastrophic misuse.", "https://www.aljazeera.com/news/2026/9/27/bill-gates-says-ai-without-regulation-is-completely-irresponsible"),
    ("Microsoft 365 Copilot", "Copilot now lets users edit scheduled prompts; retime recurring work instead of rebuilding it.", "https://www.microsoft.com/en-us/microsoft-365/roadmap?filters=&searchterms=531912"),
    ("ChatGPT", "ChatGPT Live now works with plugins; start by asking Voice to use one, then approve actions on screen.", "https://help.openai.com/en/articles/20001274-chatgpt-voice"),
    ("Tesla Manufacturing & Expansion", "A California trial opened over claims that Tesla allowed pervasive racial abuse at its Fremont factory.", "https://www.theguardian.com/technology/2026/sep/21/black-employees-accuse-tesla-fostering-discrimination"),
    ("Lighting Industry — Story One", "Acuity heads into Thursday's results with lighting sales softness and a new segment president in place.", "https://inside.lighting/news/26-09/5-things-know-september-26"),
    ("Lighting Industry — Story Two", "ArchLIGHT drew 90-plus brands and will join Dallas Lighting Week in June 2027.", "https://edisonreport.com/2026/09/24/archlight-summit-celebrates-successful-2026-event-sets-stage-for-2027/"),
    ("3D Printing News", "Bambu Lab patented a housing-actuated dual-hotend switch that removes a motor from the printhead.", "https://www.fabbaloo.com/news/tuozhu-patent-uses-printer-housing-to-switch-hotends"),
    ("Porsche 997 & 911", "No worthwhile unused standard 997 road-car item passed the verified three-month access and recency checks.", ""),
    ("AI-Powered Solopreneur Business", "Offer a $750 AI-safeguard audit to small firms; validate demand with three owner interviews.", "https://www.aljazeera.com/news/2026/9/27/bill-gates-says-ai-without-regulation-is-completely-irresponsible"),
    ("Anna Maria Island News", "Bradenton Beach commissioners are weighing a 13-page media and municipal social-media policy.", "https://www.islander.org/2026/09/bb-commission-weighs-proposed-communications-policy/"),
    ("Lake Oconee News", "Lake Oconee Bistro hosts a Different Eras trivia night in Eatonton from 6 to 7 tonight.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events/trivia-night-at-lake-oconee-bistro0928"),
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
    c.setTitle("Great Waters Gazette — Monday, September 28, 2026"); c.setAuthor("Great Waters Gazette")
    width, height = letter
    c.setFillColor(CREAM); c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold", 28); c.drawCentredString(width / 2, 752, "Great Waters Gazette")
    c.setFont("DVSans", 11); c.drawCentredString(width / 2, 731, "Monday, September 28, 2026")
    left, right, top = 40, 572, 704
    weather_width, gap = 195, 16; photo_x = left + weather_width + gap; photo_width = right - photo_x
    c.setFont("DVSansBold", 13); c.drawString(left, top, "ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left, top - 6, left + weather_width, top - 6)
    y = top - 25
    for day, condition, temps in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold", 8.1); c.drawString(left, y, day)
        c.setFont("DVSans", 6.8); c.drawString(left + 47, y, condition); c.drawRightString(left + weather_width, y, temps); y -= 16
    c.setFillColor(LINK); c.setFont("DVSans", 7.3)
    weather_label = "Weather Channel — 6:04 AM EDT"; c.drawString(left, y - 1, weather_label)
    c.linkURL(WEATHER_URL, (left, y - 3, left + stringWidth(weather_label, "DVSans", 7.3), y + 8), relative=0)
    cover(c, PHOTO, photo_x, 570, photo_width, 134); c.linkURL(PHOTO_URL, (photo_x, 570, right, 704), relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans", 6.8); c.drawString(photo_x, 559, "Yesterday's Picture: Parrot gladiolus flower in rain, Ooty, India.")
    c.setFillColor(LINK); credit = "© Timothy A. Gonsalves / CC BY-SA 4.0 (cropped)"; c.drawString(photo_x, 549, credit)
    c.linkURL(PHOTO_URL, (photo_x, 547, photo_x + stringWidth(credit, "DVSans", 6.8), 558), relative=0)
    c.setFillColor(NAVY); c.roundRect(left, 509, right - left, 31, 4, stroke=1, fill=0)
    c.setFont("DVSansBold", 9); c.drawString(left + 8, 528, "Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique", 7.4)
    practice = "Let history shrink today's drama: choose one useful act, perform it humbly, and release the applause."
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
