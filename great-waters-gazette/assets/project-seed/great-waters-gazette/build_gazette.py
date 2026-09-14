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

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-14.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-13-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Breil-Brigels._(actm)_02.jpg"
WEATHER=[("Today","Partly cloudy (15%)","97 / 72"),("Tue 15","Partly cloudy (11%)","92 / 68"),("Wed 16","Mostly sunny (6%)","90 / 63"),("Thu 17","Sunny (5%)","92 / 63"),("Fri 18","Sunny (5%)","95 / 67")]
STORIES=[
("AI Story of the Day","Trump dismissed AI-safety warnings as exaggerated while urging the U.S. to keep its technology lead.","https://www.reuters.com/world/europe/trump-says-very-negative-forces-raising-exaggerated-concerns-over-ai-2026-09-13/"),
("Microsoft 365 Copilot","Copilot's redesigned chat home and navigation simplify switching; tip: pin the tools you use most.","https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
("ChatGPT","Business admins can test a member's model access; tip: diagnose policy settings before changing them.","https://help.openai.com/en/articles/11391654-chatgpt-business-release-notes"),
("Tesla Manufacturing & Expansion","Tesla registered a Vietnam subsidiary for sales, parts, machinery, imports and distribution.","https://www.reuters.com/world/asia-pacific/tesla-sets-up-vietnam-unit-registration-filing-shows-2026-09-14/"),
("Lighting Industry — Story One","London Design Festival spotlights seven new lamps, including Bocci's orb and Raw Edges' low-waste design.","https://www.wallpaper.com/design-interiors/lighting-designs-at-london-design-festival-2026"),
("Lighting Industry — Story Two","Synapse Wireless named former Acuity Brands president Trevor Palmer as chief executive.","https://www.synapsewireless.com/"),
("3D Printing News","Single-piece automation points to just-in-time 3D-printed implants with linked inspection and traceability.","https://www.fabbaloo.com/news/how-single-piece-automation-could-transform-3d-printed-orthopedic-implant-manufacturing"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Sell a $1,500 monthly AI-policy signal brief to regulated small firms; validate with three owners.","https://www.reuters.com/world/europe/trump-says-very-negative-forces-raising-exaggerated-concerns-over-ai-2026-09-13/"),
("Anna Maria Island News","Bradenton Beach advanced a $7.33 million budget while keeping its current millage rate.","https://amisun.com/bradenton-beach-commission-adopts-2026-27-budget/"),
("Lake Oconee News","Songs & Drives for Lives tees off at Cuscowilla today to support mental-health awareness.","https://lakeoconeelife.com/lake-oconee-calendar-of-events"),
]
def cover(c,path,x,y,w,h):
    with Image.open(path) as im: iw,ih=im.size
    s=max(w/iw,h/ih); sw,sh=iw*s,ih*s
    c.saveState(); p=c.beginPath(); p.rect(x,y,w,h); c.clipPath(p,stroke=0,fill=0)
    c.drawImage(ImageReader(str(path)),x-(sw-w)/2,y-(sh-h)/2,sw,sh); c.restoreState()
def line(c,x,y,text,url,maxw):
    if not url:
        c.setFont("DVSans",7.3); c.setFillColor(TEXT); c.drawString(x,y,text); return
    label="  Read source"; size=7.3
    while size>6.3 and stringWidth(text+label,"DVSans",size)>maxw: size-=.1
    c.setFont("DVSans",size); c.setFillColor(TEXT); c.drawString(x,y,text)
    lx=x+stringWidth(text,"DVSans",size); c.setFillColor(LINK); c.drawString(lx,y,label)
    c.linkURL(url,(lx,y-2,lx+stringWidth(label,"DVSans",size),y+size),relative=0)
def build():
    c=canvas.Canvas(str(OUT),pagesize=letter); W,H=letter
    c.setTitle("Great Waters Gazette — Monday, September 14, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Monday, September 14, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:00 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Lag da Breil reservoir at Breil-Brigels, Switzerland.")
    c.setFillColor(LINK); c.drawString(px,549,"Agnes Monkelbaan / Wikimedia Commons / CC BY-SA 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Begin with what is yours to govern: the next judgment, the next action, and the tone you bring to both.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
