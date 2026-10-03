from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "Great_Waters_Gazette_2026-10-03.pdf"
PHOTO = ROOT / "gene-autry.webp"

NAVY = HexColor("#17324D")
INK = HexColor("#20201D")
MUTED = HexColor("#6B665E")
CREAM = HexColor("#F7F1E5")
PAPER = HexColor("#FFFDF8")
GOLD = HexColor("#B78B47")
RULE = HexColor("#D5CAB8")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
pdfmetrics.registerFont(TTFont("Gazette", FONT))
pdfmetrics.registerFont(TTFont("GazetteBold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("GazetteItalic", FONT_ITALIC))

WEATHER_URL = "https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL = "https://commons.wikimedia.org/wiki/File:Gene_Autry,_NPG_94_39.jpg"

WEATHER = [
    ("TODAY", "Cloudy", "85 / 71", "21%"),
    ("SUN 04", "Rain", "75 / 68", "80%"),
    ("MON 05", "AM Showers", "79 / 61", "63%"),
    ("TUE 06", "Partly Cloudy", "79 / 57", "16%"),
    ("WED 07", "Partly Cloudy", "78 / 53", "10%"),
]

STORIES = [
    ("AI", "OCT 3", "OpenAI says its agent-hack review is scanning 50 petabytes at a cost above $500,000 a day.", "https://www.theguardian.com/technology/2026/oct/03/openai-review-hacks-australian-government-sites-costing-500000-a-day"),
    ("M365 COPILOT", "SEP 2026", "Microsoft halted its planned rollout of interactive Copilot agents in Teams meetings after further review.", "https://www.microsoft.com/en-us/microsoft-365/roadmap?featureid=383013"),
    ("CHATGPT", "CURRENT", "OpenAI Presence places managed workspace agents in ChatGPT or Slack for Business and Enterprise teams.", "https://help.openai.com/en/articles/20001405-openai-presence"),
    ("TESLA", "OCT 2", "Tesla delivered 486,532 vehicles in Q3, beating the 456,896 consensus as European demand recovered.", "https://www.reuters.com/business/autos-transportation/tesla-posts-stronger-than-expected-quarterly-deliveries-2026-10-02/"),
    ("LIGHTING 1", "OCT 2", "Acuity's Q4 sales rose 2.9% to $1.24B; Intelligent Spaces grew 16.6% while lighting sales slipped 0.4%.", "https://edisonreport.com/2026/10/02/acuity-q4-2026-earnings/"),
    ("LIGHTING 2", "SEP 29", "Lighting leaders are framing repairable fixtures and subscription lumens as the industry's next operating model.", "https://edisonreport.podbean.com/e/today-in-lighting-29-sep-2026-1790719473/"),
    ("3D PRINTING", "OCT 2", "Harbin researchers printed conductive cement supercapacitors that store charge while remaining structural.", "https://3dprinting.com/news/harbin-researchers-3d-print-cement-that-stores-electricity/"),
    ("PORSCHE 997", "3-MO CHECK", "No new, fully accessible standard 997.1/997.2 road-car item passed the access, recency and repeat gates.", None),
    ("SOLOPRENEUR", "PLAY", "Sell a $900 workspace-agent pilot: map one recurring task, deploy one agent, and validate with three clients.", "https://help.openai.com/en/articles/20001405-openai-presence"),
    ("ANNA MARIA", "OCT 1", "Anna Maria City Administrator Amber LaRowe resigned on her first effective day in the newly appointed role.", "https://amisun.com/city-administrator-amber-larowe-resigns/"),
    ("LAKE OCONEE", "OCT 9", "Banks & Shane play Harmony Crossing next Friday; gates open at 6 p.m. and music starts at 7 p.m.", "https://visitlakeoconee.com/event/banks-shane-live-at-the-lake/"),
]


def fit_text(c, text, font, max_size, min_size, width):
    size = max_size
    while size > min_size and c.stringWidth(text, font, size) > width:
        size -= 0.1
    return max(size, min_size)


def link_text(c, text, x, y, font, size, color, url=None):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)
    if url:
        w = c.stringWidth(text, font, size)
        c.linkURL(url, (x, y - 2, x + w, y + size + 1), relative=0)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    W, H = letter
    c.setTitle("Great Waters Gazette — October 3, 2026")
    c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # Masthead
    c.setFillColor(NAVY)
    c.rect(0, H - 88, W, 88, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(34, H - 24, 544, 1.4, stroke=0, fill=1)
    c.setFont("GazetteBold", 24)
    c.setFillColor(PAPER)
    c.drawCentredString(W / 2, H - 54, "GREAT WATERS GAZETTE")
    c.setFont("Gazette", 8.2)
    c.setFillColor(HexColor("#E8DCC8"))
    c.drawCentredString(W / 2, H - 72, "SATURDAY, OCTOBER 3, 2026  •  EATONTON, GEORGIA")

    # Weather and licensed photo band
    c.setFillColor(PAPER)
    c.roundRect(34, 572, 544, 118, 7, stroke=0, fill=1)
    c.setStrokeColor(RULE)
    c.roundRect(34, 572, 544, 118, 7, stroke=1, fill=0)
    c.setFont("GazetteBold", 9.2)
    c.setFillColor(NAVY)
    c.drawString(48, 672, "FIVE-DAY OUTLOOK")
    link_text(c, "THE WEATHER CHANNEL", 295, 672, "GazetteBold", 6.4, GOLD, WEATHER_URL)
    c.setFont("Gazette", 5.9)
    c.setFillColor(MUTED)
    c.drawString(48, 661, "Eatonton, GA 31024  •  observed 6:05 a.m. EDT")

    xcols = [48, 118, 240, 326]
    y = 645
    for day, cond, temps, precip in WEATHER:
        c.setStrokeColor(HexColor("#E9E1D4"))
        c.line(48, y - 4, 390, y - 4)
        c.setFont("GazetteBold", 6.5)
        c.setFillColor(NAVY)
        c.drawString(xcols[0], y, day)
        c.setFont("Gazette", 6.5)
        c.setFillColor(INK)
        c.drawString(xcols[1], y, cond)
        c.drawString(xcols[2], y, temps)
        c.drawRightString(390, y, precip)
        y -= 16
    c.setFont("Gazette", 5.4)
    c.setFillColor(MUTED)
    c.drawString(240, 651, "HIGH / LOW")
    c.drawRightString(390, 651, "PRECIP.")

    # Photo crop
    with Image.open(PHOTO) as im:
        iw, ih = im.size
    box_x, box_y, box_w, box_h = 410, 588, 80, 86
    c.saveState()
    p = c.beginPath()
    p.roundRect(box_x, box_y, box_w, box_h, 4)
    c.clipPath(p, stroke=0, fill=0)
    scale = max(box_w / iw, box_h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(PHOTO)), box_x + (box_w - dw) / 2, box_y + (box_h - dh) / 2, dw, dh, mask="auto")
    c.restoreState()
    c.setFont("GazetteBold", 6.2)
    c.setFillColor(NAVY)
    c.drawString(500, 665, "YESTERDAY'S IMAGE")
    c.setFont("Gazette", 5.8)
    c.setFillColor(INK)
    c.drawString(500, 652, "Gene Autry, 1942")
    c.drawString(500, 643, "POTD • Oct. 2")
    c.setFillColor(MUTED)
    c.drawString(500, 629, "Warnecke & Cranston")
    c.drawString(500, 620, "NPG / Smithsonian")
    link_text(c, "CC0 • COMMONS", 500, 603, "GazetteBold", 5.6, GOLD, PHOTO_URL)

    # Stoic practice
    c.setFillColor(NAVY)
    c.roundRect(34, 528, 544, 31, 5, stroke=0, fill=1)
    c.setFont("GazetteBold", 7.1)
    c.setFillColor(GOLD)
    c.drawString(47, 546, "STOIC PRACTICE")
    c.setFont("GazetteItalic", 7.4)
    c.setFillColor(PAPER)
    c.drawString(124, 546, "Name the duty you are resisting. Give it ten focused minutes before negotiating with yourself.")
    link_text(c, "DAILY STOIC", 500, 533, "GazetteBold", 5.4, HexColor("#E8DCC8"), "https://dailystoic.com/podcast/")

    # Story ledger — every summary is rendered on exactly one line.
    top = 507
    row_h = 29
    for i, (label, date, summary, url) in enumerate(STORIES):
        y0 = top - i * row_h
        if i % 2 == 0:
            c.setFillColor(Color(1, 1, 1, alpha=0.42))
            c.rect(34, y0 - 20, 544, row_h, stroke=0, fill=1)
        c.setStrokeColor(RULE)
        c.line(34, y0 - 21, 578, y0 - 21)
        c.setFont("GazetteBold", 7.2)
        c.setFillColor(NAVY)
        c.drawString(42, y0, label)
        c.setFont("Gazette", 5.2)
        c.setFillColor(GOLD)
        c.drawString(42, y0 - 9, date)
        source_x = 535
        summary_x = 122
        summary_w = source_x - summary_x - 9
        size = fit_text(c, summary, "Gazette", 6.7, 5.35, summary_w)
        link_text(c, summary, summary_x, y0 - 4, "Gazette", size, INK, url)
        if url:
            link_text(c, "SOURCE ↗", source_x, y0 - 4, "GazetteBold", 5.1, GOLD, url)
        else:
            c.setFont("GazetteBold", 5.1)
            c.setFillColor(MUTED)
            c.drawString(source_x, y0 - 4, "NO ITEM")

    # One-line close
    c.setFillColor(PAPER)
    c.roundRect(34, 146, 544, 43, 6, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(34, 146, 544, 43, 6, stroke=1, fill=0)
    c.setFont("GazetteBold", 7)
    c.setFillColor(GOLD)
    c.drawString(47, 173, "THE DAY IN ONE LINE")
    close = "Agents grow up, vehicle demand rebounds, smart spaces outpace fixtures, and lake country lines up its next Friday night."
    size = fit_text(c, close, "GazetteItalic", 7.4, 6.3, 515)
    c.setFont("GazetteItalic", size)
    c.setFillColor(NAVY)
    c.drawString(47, 158, close)

    c.setStrokeColor(NAVY)
    c.line(34, 122, 578, 122)
    c.setFont("Gazette", 5.5)
    c.setFillColor(MUTED)
    c.drawString(34, 110, "Fresh links. Plain-English takeaways. One page for a better Saturday.")
    c.drawRightString(578, 110, "GREAT WATERS GAZETTE • OCTOBER 3, 2026")
    c.setFont("Gazette", 4.8)
    c.drawString(34, 98, "Weather: The Weather Channel. Photo: Harry Warnecke & Robert F. Cranston / National Portrait Gallery, Smithsonian; CC0 via Wikimedia Commons.")

    c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    build()
