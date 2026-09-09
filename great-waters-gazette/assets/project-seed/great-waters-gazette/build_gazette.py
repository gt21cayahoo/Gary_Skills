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
OUT = ROOT.parent / "output" / "pdf" / "Great_Waters_Gazette_2026-09-09.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "assets" / "2026-09-08-picture-of-the-day.jpg"

CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:Sunset_over_Trommekilen_from_Norrkila_6.jpg"
STOIC_URL = "https://dailystoic.com/podcast/"

WEATHER = [
    ("Wed 09", "Partly cloudy (1%)", "91 / 72"),
    ("Thu 10", "Partly cloudy (23%)", "91 / 73"),
    ("Fri 11", "Scattered storms (58%)", "90 / 72"),
    ("Sat 12", "Scattered storms (44%)", "88 / 72"),
    ("Sun 13", "Partly cloudy (24%)", "91 / 71"),
]

STORIES = [
    ("AI Story of the Day", "AI labs are asking governments and rivals for shared restraints as capabilities accelerate.", "https://www.axios.com/2026/09/09/openai-artificial-general-intelligence-safety"),
    ("Microsoft 365 Copilot", "Copilot can ground answers in authorized private Viva Engage posts; tip: ask for expert consensus.", "https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
    ("ChatGPT", "ChatGPT Images 2.5 improves editing and speed; tip: sketch a layout before generating the image.", "https://openai.com/index/introducing-chatgpt-images-2-5/"),
    ("Tesla Manufacturing & Expansion", "Samsung's Taylor 2nm fab is reportedly booked by Tesla AI5 and AI6 chip orders.", "https://www.trendforce.com/news/2026/09/09/news-samsung-taylor-fab-reportedly-fully-booked-for-2nm-before-operations-begin-fab-2-preparations-accelerate/"),
    ("Lighting Industry - Top Two", "", ""),
    ("3D Printing News", "California's AB 2047 printer-control bill passed the legislature and awaits the governor.", "https://www.fabbaloo.com/news/california-ab-2047-3d-printer-bill-passes-legislature-awaits-governors-decision"),
    ("Porsche 997 & 911", "Owners compare a 997.1 Carrera 4 and Carrera S on traction, steering feel and buying risk.", "https://www.reddit.com/r/porsche911/comments/1vw7eqp/9971_carrera_4_vs_carrera_s/"),
    ("AI-Powered Solopreneur Business", "Opportunity: sell same-day catalog-image refreshes to small retailers with Images 2.5.", "https://openai.com/index/introducing-chatgpt-images-2-5/"),
    ("Anna Maria Island News", "About 150 residents joined Anna Maria's town hall on the city's evolving parking study.", "https://amisun.com/anna-maria-hosts-parking-study-meeting/"),
    ("Lake Oconee News", "A Fiber Arts Gathering brings local makers together in Madison today.", "https://lakeoconeelife.com/lake-oconee-calendar-of-events"),
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
    c.setTitle("Great Waters Gazette - Wednesday, September 9, 2026")
    c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    c.setFillColor(TEXT)
    c.setFont("Times-Bold", 28)
    c.drawCentredString(width / 2, 750, "Great Waters Gazette")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, 730, "Wednesday, September 9, 2026")

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
    link_text(c, left, y - 1, "Weather Channel - 11:16 AM EDT", WEATHER_URL, size=8.2)

    photo_h = 132
    draw_image_cover(c, PHOTO, photo_x, top - photo_h + 2, photo_w, photo_h)
    c.linkURL(PHOTO_URL, (photo_x, top - photo_h + 2, photo_x + photo_w, top + 2), relative=0)
    caption = Paragraph(
        '<b>Yesterday\'s Picture:</b> Sunset over Trommekilen and Brofjorden in Lysekil, Sweden. '
        '<font color="#0B5EA8">W.carter / Wikimedia Commons / CC0</font>',
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
        'Meet the next duty without rehearsing its difficulty; attention belongs to the action in front of you. '
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
            fitted_story_line(c, left + 4, y - 17, "PTAB invalidated every challenged claim in Feit Electric's white-filament LED patent.", "https://edisonreport.com/2026/09/08/ptab-finds-all-challenged-claims-in-feit-electric-led-patent-unpatentable/", right - left - 4, label="Read more")
            fitted_story_line(c, left + 4, y - 31, "Orion won a second multimillion-dollar hyperscaler order for data-center LED lighting.", "https://edisonreport.com/2026/09/08/orion-secures-second-multimillion-dollar-data-center-order-from-global-hyperscaler/", right - left - 4, label="Read more")
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
