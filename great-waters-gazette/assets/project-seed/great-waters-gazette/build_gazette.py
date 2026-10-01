from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
from pypdf import PdfReader
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = str(ROOT / 'archive' / 'Great_Waters_Gazette_2026-10-01.pdf')
PHOTO = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / 'assets' / 'photo-of-the-day.jpg')
Path(OUT).parent.mkdir(parents=True, exist_ok=True)
NAVY = colors.HexColor('#112A46')
INK = colors.HexColor('#17202A')
CREAM = colors.HexColor('#F6F0E3')
BLUE = colors.HexColor('#245B83')
MUTED = colors.HexColor('#5B6670')
RULE = colors.HexColor('#9AA6B2')

styles = getSampleStyleSheet()
title = ParagraphStyle('title', parent=styles['Title'], fontName='Times-Bold', fontSize=23, leading=23, alignment=TA_CENTER, textColor=NAVY, spaceAfter=1)
date_style = ParagraphStyle('date', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=9, alignment=TA_CENTER, textColor=MUTED, spaceAfter=5)
section = ParagraphStyle('section', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=8.2, leading=9, textColor=NAVY, spaceBefore=2.5, spaceAfter=0.5, borderWidth=0, uppercase=True)
weather_head = ParagraphStyle('weather_head', parent=section, textColor=colors.white)
body = ParagraphStyle('body', parent=styles['BodyText'], fontName='Helvetica', fontSize=6.65, leading=7.7, textColor=INK, spaceAfter=2)
small = ParagraphStyle('small', parent=body, fontSize=5.7, leading=6.6, textColor=MUTED)
stoic = ParagraphStyle('stoic', parent=body, fontName='Times-Italic', fontSize=7, leading=8, alignment=TA_CENTER, leftIndent=8, rightIndent=8, spaceAfter=3)

def p(text, style=body):
    return Paragraph(text, style)

def item(label, text, url):
    t = Table([[Paragraph(label.upper(), section)], [Paragraph(text + f' <link href="{url}" color="#245B83"><u>Source</u></link>', body)]], colWidths=[2.66*inch])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return t

def bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.1)
    canvas.line(28, 760, 584, 760)
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 5.5)
    canvas.drawCentredString(letter[0]/2, 15, 'GREAT WATERS GAZETTE • OCTOBER 1, 2026')
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=letter, rightMargin=26, leftMargin=26, topMargin=22, bottomMargin=21)
story = [Paragraph('GREAT WATERS GAZETTE', title), Paragraph('THURSDAY, OCTOBER 1, 2026  •  GREAT WATERS, GEORGIA', date_style)]

weather_data = [
    [p('<b>WEATHER CHANNEL • EATONTON 31024</b>', weather_head), '', '', ''],
    [p('<b>Today</b>'), p('Mostly Sunny'), p('90 / 68'), p('15%')],
    [p('<b>Fri 02</b>'), p('PM Showers'), p('88 / 71'), p('46%')],
    [p('<b>Sat 03</b>'), p('Showers'), p('86 / 71'), p('65%')],
    [p('<b>Sun 04</b>'), p('Rain'), p('76 / 67'), p('93%')],
    [p('<b>Mon 05</b>'), p('AM Showers'), p('80 / 59'), p('46%')],
    [p('<link href="https://weather.com/us/georgia/eatonton/postcode/31024/tenday" color="#245B83"><u>Weather Channel • checked 6:01 AM EDT</u></link>', small), '', '', ''],
]
wt = Table(weather_data, colWidths=[.72*inch, 1.08*inch, .62*inch, .38*inch], rowHeights=[13, 12, 12, 12, 12, 12, 12])
wt.setStyle(TableStyle([
    ('SPAN',(0,0),(3,0)),('SPAN',(0,6),(3,6)),('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
    ('GRID',(0,1),(-1,5),.25,colors.HexColor('#CBD1D7')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('ALIGN',(2,1),(-1,5),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
    ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
]))

img = Image(PHOTO, width=2.50*inch, height=1.67*inch)
caption = p('Tower of the Cathedral of Saint Domnius, Split, Croatia, seen from Diocletian’s Palace. <link href="https://commons.wikimedia.org/wiki/File:Split_Cathedral_Bell_Tower_From_The_Vestibule_-_Split.jpg" color="#245B83"><u>Sumitsurai / CC BY-SA 4.0 (cropped)</u></link>', small)
photo = Table([[img],[caption]], colWidths=[2.50*inch])
photo.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
top = Table([[wt, photo]], colWidths=[2.96*inch, 2.50*inch], hAlign='CENTER')
top.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3)]))
story += [top, Spacer(1,3), Paragraph('<b>THE DAILY STOIC</b> — Before reacting, separate the event from the story you are telling about it. Write the bare facts in one sentence, then choose the most useful next action. <link href="https://dailystoic.com/" color="#245B83"><u>Daily Stoic</u></link>', stoic)]

left = []
left += [item('Artificial Intelligence', 'The FTC opened a consumer-protection probe into OpenAI, Anthropic and other frontier AI developers.', 'https://apnews.com/article/89ac416717adbfb1d72f2d85e6ce83d1')]
left += [item('Microsoft 365 Copilot', 'Teams Copilot can analyze recorded screen-shared content alongside meeting chat and transcript; use it to trace decisions to the slide that prompted them.', 'https://www.microsoft.com/microsoft-365/roadmap?featureid=119620')]
left += [item('ChatGPT', 'Pro 500 costs $500 monthly and is the only Pro tier with Astra Ultrafast; test whether lower latency pays back before upgrading.', 'https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers')]
left += [item('Tesla', 'Tesla signed three credit facilities totaling $30 billion, led by a $20 billion delayed-draw term loan.', 'https://www.sec.gov/Archives/edgar/data/1318605/000162828026063820/tsla-20260929.htm')]
left += [item('Lighting • 1', 'Third-party-verified industry EPDs now cover linears, downlights, cylinders, troffers and post tops.', 'https://edisonreport.com/2026/09/30/industry-wide-luminaire-epds/')]
left += [item('Lighting • 2', 'Signify earned an 88/100 EcoVadis score and its seventh straight Platinum medal, including 100/100 for environment.', 'https://edisonreport.com/2026/09/30/signify-earns-highest-ever-ecovadis-score-and-seventh-consecutive-platinum-medal/')]

right = []
right += [item('3D Printing', 'ADDMAN plans 81 more HP Jet Fusion 5620 Pro printers, taking its MJF fleet above 125 systems.', 'https://www.tctmagazine.com/addman-announces-plans-to-install-81-additional-hp-jet-fusion-5620-pro-3d-printers/')]
right += [item('Porsche 997 Watch', 'No newly published, freely accessible qualifying 997.1/997.2 standard road-car video was verified in the rolling three-month window today.', 'https://www.youtube.com/results?search_query=Porsche+997+review')]
right += [item('Solopreneur Move', 'Sell a $1,500 meeting-memory setup for consultancies: configure searchable Teams recordings, pilot it with three firms, and measure time saved finding decisions.', 'https://www.microsoft.com/microsoft-365/roadmap?featureid=119620')]
right += [item('Anna Maria Island', 'A Sarasota Bay Watch youth cleanup mobilized 45 volunteers to remove fishing line, lures, nets and other debris that threatens seabirds.', 'https://amisun.com/monofilament-cleanup-inspires-youth-leadership/')]
right += [item('Lake Oconee', 'Lake Country Books & Gifts in Harmony Crossing combines an independent bookstore with book clubs, author visits, story times and special-order service.', 'https://lakeoconeelife.com/business/lakecountrybooksandgifts')]
right += [Paragraph('TODAY IN ONE LINE', section), Paragraph('Watch the rain trend, test premium AI against real latency value, and turn meeting search into a measurable client service.', body)]

left_col = Table([[x] for x in left], colWidths=[2.68*inch])
right_col = Table([[x] for x in right], colWidths=[2.68*inch])
for inner in (left_col, right_col):
    inner.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
cols = Table([[left_col, right_col]], colWidths=[2.72*inch, 2.72*inch], hAlign='CENTER')
cols.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBEFORE',(1,0),(1,0),.7,NAVY),('LEFTPADDING',(0,0),(0,0),4),('RIGHTPADDING',(0,0),(0,0),8),('LEFTPADDING',(1,0),(1,0),9),('RIGHTPADDING',(1,0),(1,0),3)]))
story.append(cols)
doc.build(story, onFirstPage=bg, onLaterPages=bg)
r = PdfReader(OUT)
if len(r.pages) != 1:
    raise SystemExit(f'ERROR: PDF has {len(r.pages)} pages')
print(OUT)
