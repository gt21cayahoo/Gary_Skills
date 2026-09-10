from pathlib import Path
import shutil

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "output" / "pdf" / "Great_Waters_Gazette_2026-09-10.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "assets" / "2026-09-09-picture-of-the-day.jpg"

CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:189_Red-and-green_macaw_couple_flying_in_Chapada_dos_Guimar%C3%A3es_National_Park_Photo_by_Giles_Laurent.jpg"
STOIC_URL = "https://dailystoic.com/podcast/"

WEATHER = [
    ("Today", "AM clouds / PM sun (10%)", "93 / 73"),
    ("Fri 11", "PM thunderstorms (54%)", "91 / 72"),
    ("Sat 12", "Partly cloudy (24%)", "89 / 72"),
    ("Sun 13", "Partly cloudy (24%)", "92 / 71"),
    ("Mon 14", "Mostly sunny (15%)", "95 / 72"),
]

STORIES = [
    ("AI Story of the Day", "ENISA is testing Anthropic's Mythos 5 and OpenAI's GPT-6 Astra.", "https://www.reuters.com/technology/eus-cybersecurity-agency-granted-access-mythos-5-ai-model-commission-says-2026-09-10/"),
    ("Microsoft 365 Copilot", "Copilot Notebooks can use Outlook emails as sources; tip: add key decision threads before drafting.", "https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
    ("ChatGPT", "Voice can use GPT-5.6 or GPT-6 Astra; tip: raise reasoning for complex dictated work.", "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
    ("Tesla Manufacturing & Expansion", "Tesla began limited Cybercab rides in Austin as NHTSA evaluates the steering-wheel-free rollout.", "https://www.reuters.com/technology/us-auto-safety-regulator-says-evaluating-teslas-cybercab-rollout-2026-09-04/"),
    ("Lighting Industry - Top Two", "", ""),
    ("3D Printing News", "Continuous Composites won a Navy SBIR to embed electrical functions in printed UAV structures.", "https://3dprint.com/331981/continuous-composites-gets-phase-ii-sbir-for-embedding-electronics-in-uavs/"),
    ("Porsche 997 & 911", "A new 997.1 owner gets practical guidance on oil-level readings, wheel-bolt torque and rear trim.", "https://rennlist.com/forums/997-forum/1517934-997-1-new-owner-questions.html"),
    ("AI-Powered Solopreneur Business", "Offer contractors a $750/week voice-note-to-job-brief service; validate with three owner-operators.", "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
    ("Anna Maria Island News", "Gulf Islands Ferry added a Coquina Bayside stop, opening another car-free route to Coquina Beach.", "https://www.islander.org/2026/09/gulf-islands-ferry-opens-coquina-bayside-stop/"),
    ("Lake Oconee News", "Neighbors Helping Neighbors holds a 4 p.m. Lakeside Church town hall on local family-support projects.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events/town-hall-meeting-september0910"),
]


def draw_image_cover(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    sw, sh = iw * scale, ih * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), x - (sw - w) / 2, y - (sh - h) / 2, sw, sh, mask="auto")
    c.restoreState()


def link_text(c, x, y, label, url, font="Times-Roman", size=9.4):
    c.setFont(font, size)
    c.setFillColor(LINK)
    c.drawString(x, y, label)
    width = stringWidth(label, font, size)
    c.linkURL(url, (x, y - 2, x + width, y + size), relative=0)


def fitted_story_line(c, x, y, text, url, max_width, label="Read more", start_size=8.8, min_size=7.2):
    sep = " - "
    size = start_size
    while size > min_size:
        total = stringWidth(text + sep, "Times-Roman", size) + stringWidth(label, "Times-Roman", size)
        if total <= max_width:
            break
        size -= 0.1
    c.setFont("Times-Roman", size)
    c.setFillColor(TEXT)
    c.drawString(x, y, text + sep)
    link_x = x + stringWidth(text + sep, "Times-Roman", size)
    link_text(c, link_x, y, label, url, size=size)


def build(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    c.setTitle("Great Waters Gazette - Thursday, September 10, 2026")
    c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    c.setFillColor(TEXT)
    c.setFont("Times-Bold", 28)
    c.drawCentredString(width / 2, 750, "Great Waters Gazette")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, 730, "Thursday, September 10, 2026")

    left, right = 42, 570
    top = 704
    col_gap = 16
    available = right - left - col_gap
    weather_w = available * 0.37
    photo_w = available - weather_w
    photo_x = left + weather_w + col_gap

    c.setFont("Times-Bold", 13.5)
    c.drawString(left, top, "ZIP 31024 - 5-Day Forecast")
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.8)
    c.line(left, top - 6, left + weather_w, top - 6)

    y = top - 25
    for day, summary, temps in WEATHER:
        c.setFillColor(TEXT)
        c.setFont("Times-Bold", 8.7)
        c.drawString(left, y, day)
        c.setFont("Times-Roman", 7.5)
        c.drawString(left + 49, y, summary)
        c.drawRightString(left + weather_w, y, temps)
        y -= 16
    link_text(c, left, y - 1, "Weather Channel - 9:46 AM EDT", WEATHER_URL, size=8.2)

    photo_h = 132
    draw_image_cover(c, PHOTO, photo_x, top - photo_h + 2, photo_w, photo_h)
    c.linkURL(PHOTO_URL, (photo_x, top - photo_h + 2, photo_x + photo_w, top + 2), relative=0)
    caption = Paragraph(
        '<b>Yesterday\'s Picture:</b> Red-and-green macaws in flight at Chapada dos Guimaraes National Park. '
        '<font color="#0B5EA8">Giles Laurent / Wikimedia Commons / CC BY-SA 4.0</font>',
        ParagraphStyle("caption", fontName="Times-Roman", fontSize=7.5, leading=9, textColor=TEXT),
    )
    caption.wrapOn(c, photo_w, 32)
    caption.drawOn(c, photo_x, top - photo_h - 22)
    c.linkURL(PHOTO_URL, (photo_x, top - photo_h - 23, photo_x + photo_w, top - photo_h + 1), relative=0)

    c.setStrokeColor(NAVY)
    c.setFillColor(NAVY)
    c.roundRect(left, 512, right - left, 38, 4, stroke=1, fill=0)
    c.setFont("Times-Bold", 9.8)
    c.drawString(left + 9, 536, "Today's Stoic Practice")
    stoic = Paragraph(
        'Choose the next useful action, then give it your full attention before judging the day. '
        '- <link href="https://dailystoic.com/podcast/" color="#0B5EA8"><u>Daily Stoic</u></link>',
        ParagraphStyle("stoic", fontName="Times-Italic", fontSize=8.2, leading=9.4, textColor=TEXT),
    )
    stoic.wrapOn(c, right - left - 18, 20)
    stoic.drawOn(c, left + 9, 517)

    # Preserve a clear visual pause between the Stoic practice and the news.
    y = 487
    for heading, story, url in STORIES:
        c.setFillColor(TEXT)
        c.setFont("Times-Bold", 11.1)
        c.drawString(left, y, heading)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.2)
        c.line(left, y - 4, right, y - 4)
        if heading == "Lighting Industry - Top Two":
            fitted_story_line(c, left + 4, y - 17, "Loxone is positioning lighting as a building-system layer beside HVAC, shading, energy and security.", "https://www.lightnowblog.com/2026/09/loxone-positions-lighting-as-a-building-system-layer/", right - left - 4, label="Read more")
            fitted_story_line(c, left + 4, y - 31, "Flock camera controversy is pulling streetlights into the national surveillance debate.", "https://www.lightnowblog.com/2026/09/flock-controversy-comes-to-streetlights/", right - left - 4, label="Read more")
            y -= 57
        else:
            fitted_story_line(c, left + 4, y - 18, story, url, right - left - 4)
            y -= 44

    c.setFillColor(NAVY)
    c.setFont("Times-Italic", 7.2)
    c.drawCentredString(width / 2, 28, "A concise morning digest - sources linked in every section")
    c.showPage()
    c.save()


if __name__ == "__main__":
    build(OUT)
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT, ARCHIVE)
    print(OUT)
