from pathlib import Path
import shutil

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "output" / "pdf" / "Great_Waters_Gazette_2026-09-11.pdf"
ARCHIVE = ROOT / "archive" / OUT.name
PHOTO = ROOT / "assets" / "2026-09-10-picture-of-the-day.jpg"

CREAM = HexColor("#FBF7E9")
NAVY = HexColor("#173A5E")
LINK = HexColor("#0B5EA8")
TEXT = HexColor("#151515")

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:Lake_Geneva_from_Chillon_Castle.jpg"

WEATHER = [
    ("Today", "PM thunderstorms (63%)", "91 / 71"),
    ("Sat 12", "PM thunderstorms (47%)", "86 / 71"),
    ("Sun 13", "Partly cloudy (24%)", "93 / 71"),
    ("Mon 14", "Partly cloudy (15%)", "96 / 72"),
    ("Tue 15", "Mostly sunny (15%)", "92 / 67"),
]

STORIES = [
    ("AI Story of the Day", "Sam Altman told staff OpenAI is open to slowing AI development as safety concerns rise.", "https://www.reuters.com/business/altman-tells-staff-openai-is-open-slowing-ai-development-bloomberg-news-reports-2026-09-11/"),
    ("Microsoft 365 Copilot", "Excel's =COPILOT preview retires Sept. 14; tip: move text tasks to the paid Copilot side pane.", "https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/microsoft-is-ditching-the-copilot-function-in-excel-before-it-even-launches"),
    ("ChatGPT", "ChatGPT for Financial Services adds licensed data and firm templates; tip: require cited source trails.", "https://www.reuters.com/business/openai-launches-chatgpt-financial-services-industry-2026-09-10/"),
    ("Tesla Manufacturing & Expansion", "Cybercab's hidden touch joystick may support end-of-line checks and depot repositioning.", "https://www.caranddriver.com/news/a73667574/tesla-cybercab-joystick-screen-controls/"),
    ("Lighting Industry - Top Two", "", ""),
    ("3D Printing News", "Stratasys will bring production tooling, fixtures and end-use workflows to IMTS 2026.", "https://investors.stratasys.com/news-events/press-releases/detail/992/stratasys-brings-production-proven-additive-manufacturing"),
    ("Porsche 997 & 911", "No worthwhile unused standard 997 road-car item remains in the verified three-month queue.", ""),
    ("AI-Powered Solopreneur Business", "Offer merchants a $1,000 AI payment-reconciliation setup; validate with three Shopify operators.", "https://www.expresscomputer.in/news/78-of-indian-businesses-would-switch-payment-gateways-for-ai-capabilities-zoho-survey/138608/"),
    ("Anna Maria Island News", "Anna Maria City Pier remediation is wrapping up, leaving one final construction phase before reopening.", "https://www.islander.org/2026/09/amcp-remediation-work-wraps-up/"),
    ("Lake Oconee News", "Eatonton hosts a 25th-anniversary 9/11 remembrance this morning at Veterans Wall of Honor Park.", "https://www.facebook.com/putnamcountyga/posts/1359728646334136/"),
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
    if not url:
        size = start_size
        while size > min_size and stringWidth(text, "Times-Roman", size) > max_width:
            size -= 0.1
        c.setFont("Times-Roman", size)
        c.setFillColor(TEXT)
        c.drawString(x, y, text)
        return
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
    c.setTitle("Great Waters Gazette - Friday, September 11, 2026")
    c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    c.setFillColor(TEXT)
    c.setFont("Times-Bold", 28)
    c.drawCentredString(width / 2, 750, "Great Waters Gazette")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, 730, "Friday, September 11, 2026")

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
    link_text(c, left, y - 1, "Weather Channel - 9:00 AM EDT", WEATHER_URL, size=8.2)

    photo_h = 132
    draw_image_cover(c, PHOTO, photo_x, top - photo_h + 2, photo_w, photo_h)
    c.linkURL(PHOTO_URL, (photo_x, top - photo_h + 2, photo_x + photo_w, top + 2), relative=0)
    caption = Paragraph(
        '<b>Yesterday\'s Picture:</b> Lake Geneva from Chillon Castle at sunset. '
        '<font color="#0B5EA8">Dmitry A. Mottl / Wikimedia Commons / CC BY-SA 4.0 (cropped)</font>',
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
        'Do not postpone the duty in front of you; steady action is remembrance made useful. '
        '- <link href="https://dailystoic.com/podcast/" color="#0B5EA8"><u>Daily Stoic</u></link>',
        ParagraphStyle("stoic", fontName="Times-Italic", fontSize=8.2, leading=9.4, textColor=TEXT),
    )
    stoic.wrapOn(c, right - left - 18, 20)
    stoic.drawOn(c, left + 9, 517)

    y = 487
    for heading, story, url in STORIES:
        c.setFillColor(TEXT)
        c.setFont("Times-Bold", 11.1)
        c.drawString(left, y, heading)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.2)
        c.line(left, y - 4, right, y - 4)
        if heading == "Lighting Industry - Top Two":
            fitted_story_line(c, left + 4, y - 17, "CEDIA signals a shift toward commissioned systems and integrator-led lighting delivery.", "https://electricaltrends.com/2026/09/07/what-cedia-already-knows-about-systems-delivery/", right - left - 4)
            fitted_story_line(c, left + 4, y - 31, "Zumtobel and Impact Acoustic are combining lighting, acoustics and interior-system design.", "https://edisonreport.com/2026/09/09/zumtobel-and-impact-acoustic-partner-to-improve-quality-of-life-in-enclosed-space/", right - left - 4)
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
