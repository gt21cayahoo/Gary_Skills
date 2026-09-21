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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-21.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-20-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Bloeiwijze_van_een_Rostrinucula_dependens._11-10-2025._(d.j.b).jpg"
WEATHER=[("Today","Partly cloudy (15%)","93 / 70"),("Tue 22","Partly cloudy (20%)","91 / 71"),("Wed 23","AM showers (37%)","82 / 64"),("Thu 24","Mostly cloudy (24%)","75 / 59"),("Fri 25","Partly cloudy (7%)","81 / 57")]
STORIES=[
("AI Story of the Day","U.S. officials proposed an AI-incident alert system with China to flag national-security threats.","https://apnews.com/article/2c7f54f07e755f506d9db9b91df282bd"),
("Microsoft 365 Copilot","Copilot adds Claude Opus 5; tip: reserve it for high-stakes, multi-step work.","https://www.microsoft.com/en-us/microsoft-365/roadmap?filters=&searchterms=555888"),
("ChatGPT","OpenAI's Microsoft add-in brings ChatGPT into Word, Excel and PowerPoint; verify every changed cell and citation.","https://marketplace.microsoft.com/en-us/product/office/WA200010215"),
("Tesla Manufacturing & Expansion","NHTSA ordered Tesla to explain how it self-certified Cybercab with temporary driver controls.","https://www.reuters.com/business/autos-transportation/us-agency-orders-tesla-answer-questions-cybercab-certification-2026-09-15/"),
("Lighting Industry — Story One","DALI Alliance will convene its first global summit and expo in Utrecht in February 2027.","https://edisonreport.com/2026/09/16/dali-alliance-announces-dali-27-inaugural-global-summit-expo/"),
("Lighting Industry — Story Two","Selectable fixtures reduce SKUs, but designers warn that flexibility can compromise design intent.","https://edisonreport.com/2026/09/16/selectable-lighting-when-one-size-does-not-fit-all/"),
("3D Printing News","IperionX validated continuous titanium-powder production across four campaigns: 500 kg in 41 hours.","https://www.voxelmatters.com/iperionx-validates-genx-continuous-titanium-powder-production/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer a $3,500 AI incident-readiness drill; validate it with one exporter and its counsel.","https://apnews.com/article/2c7f54f07e755f506d9db9b91df282bd"),
("Anna Maria Island News","Bridge Street's Sundown Getdown mixed local vendors, live art, music and food in Bradenton Beach.","https://www.islander.org/2026/09/sundown-party-heats-up-bridge-street/"),
("Lake Oconee News","Table at the Lake serves $12 martinis and chef-selected oysters from 5–9 tonight.","https://lakeoconeelife.com/lake-oconee-calendar-of-events/mondaymartinis0921"),
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
    c.setTitle("Great Waters Gazette — Monday, September 21, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Monday, September 21, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:07 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Rostrinucula dependens inflorescence.")
    c.setFillColor(LINK); c.drawString(px,549,"Dominicus Johannes Bergsma / Wikimedia Commons / CC BY-SA 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Before reacting, separate the event from the judgment you add.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
