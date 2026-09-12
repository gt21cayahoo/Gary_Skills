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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-12.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-11-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Baikal,_Cape_Burhan,_Olkhon_Island,_Lake_Baikal,_Russia.jpg"
WEATHER=[("Today","Scattered thunderstorms (56%)","84 / 71"),("Sun 13","Mostly sunny (22%)","93 / 69"),("Mon 14","Mostly sunny (8%)","96 / 72"),("Tue 15","Partly cloudy (12%)","92 / 67"),("Wed 16","Mostly sunny (15%)","90 / 63")]
STORIES=[
("AI Story of the Day","Senate negotiators weigh a frontier-AI duty of care and power to block unsafe releases.","https://www.reuters.com/legal/litigation/us-senate-negotiators-consider-requiring-ai-firms-mitigate-known-major-risks-2026-09-11/"),
("Microsoft 365 Copilot","Copilot can steer and create Pages on mobile; tip: draft in chat, then refine by audience.","https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
("ChatGPT","ChatGPT Work adds the Data plugin; tip: ask one metric question, then build a dashboard.","https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
("Tesla Manufacturing & Expansion","Tesla is taking Semi to Europe as its Nevada high-volume line begins feeding expansion.","https://www.reuters.com/business/autos-transportation/tesla-eyes-european-freight-market-with-long-delayed-semi-truck-2026-09-11/"),
("Lighting Industry — Story One","SESCO will acquire Thomas Harris & Co., extending its agency footprint into Virginia.","https://inside.lighting/news/26-09/sesco-lighting-acquires-thomas-harris-co-virginia"),
("Lighting Industry — Story Two","GigaTera reportedly ended North American sales; a Dallas team remains for warranty claims.","https://inside.lighting/news/26-09/gigatera-usa-lighting-operations-go-dark"),
("3D Printing News","NIST's RM 8047 resin gives photopolymer printers a common cure and exposure baseline.","https://www.voxelmatters.com/nist-reference-material-aims-to-standardize-photopolymer-3d-printing/"),
("Porsche 997 & 911","A fresh road test asks whether the standard 911 997 still delivers the analog dream.","https://www.youtube.com/watch?v=RAc-_ePJH4o"),
("AI-Powered Solopreneur Business","Sell a $1,500 AI-growth sprint to tiny firms; validate with three owners hiring next.","https://www.axios.com/2026/09/10/ai-hiring-small-business"),
("Anna Maria Island News","Holmes Beach expects the Marina Drive/56th Street closure through at least Sept. 25.","https://www.islander.org/2026/09/marina-drive-closure-extended-into-late-september/"),
("Lake Oconee News","Eatonton's Downtown Getdown brings live music and food vendors downtown tonight.","https://lakeoconeelife.com/lake-oconee-calendar-of-events/downtown-getdown-concert-series0912"),
]
def cover(c,path,x,y,w,h):
    with Image.open(path) as im: iw,ih=im.size
    s=max(w/iw,h/ih); sw,sh=iw*s,ih*s
    c.saveState(); p=c.beginPath(); p.rect(x,y,w,h); c.clipPath(p,stroke=0,fill=0)
    c.drawImage(ImageReader(str(path)),x-(sw-w)/2,y-(sh-h)/2,sw,sh); c.restoreState()
def line(c,x,y,text,url,maxw):
    label="  Read source"; size=7.3
    while size>6.3 and stringWidth(text+label,"DVSans",size)>maxw: size-=.1
    c.setFont("DVSans",size); c.setFillColor(TEXT); c.drawString(x,y,text)
    lx=x+stringWidth(text,"DVSans",size); c.setFillColor(LINK); c.drawString(lx,y,label)
    c.linkURL(url,(lx,y-2,lx+stringWidth(label,"DVSans",size),y+size),relative=0)
def build():
    c=canvas.Canvas(str(OUT),pagesize=letter); W,H=letter
    c.setTitle("Great Waters Gazette — Saturday, September 12, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Saturday, September 12, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:06 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Cape Burhan and Shamanka Rock, Lake Baikal.")
    c.setFillColor(LINK); c.drawString(px,549,"Vyacheslav Argenberg / Wikimedia Commons / CC BY 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Meet the first interruption without resentment; your response is the part of the morning you control.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
