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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-15.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-14-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Oregon_National_Historic_Trail_in_Wyoming.jpg"
WEATHER=[("Today","Partly cloudy (20%)","92 / 69"),("Wed 16","Mostly sunny (8%)","90 / 63"),("Thu 17","Sunny (7%)","92 / 66"),("Fri 18","Mostly sunny (9%)","97 / 69"),("Sat 19","Isolated storms (33%)","94 / 70")]
STORIES=[
("AI Story of the Day","Microsoft drafted rules requiring its AI systems to accept correction, shutdown and human control.","https://www.reuters.com/legal/litigation/microsoft-drafts-code-conduct-keep-its-ai-under-human-control-2026-09-14/"),
("Microsoft 365 Copilot","Connector content and identity crawls now run together; tip: recheck newly indexed material sooner.","https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
("ChatGPT","Group Managers can administer scoped users; tip: delegate membership work without broad admin access.","https://help.openai.com/en/articles/10128477-chatgpt-enterprise-edu-release-notes"),
("Tesla Manufacturing & Expansion","Tesla scheduled an October 1 unveiling for its long-delayed second-generation Roadster.","https://www.investors.com/news/tesla-roadster-elon-musk-cybercab-robotaxi/"),
("Lighting Industry — Story One","IKEA launched a low-cost Matter-compatible driver for integrated cabinet and shelf lighting.","https://www.t3.com/home-living/smart-home/ikeas-matter-compatible-driver-has-finally-launched-after-leaking-6-months-ago-and-its-cheap-as-chips"),
("Lighting Industry — Story Two","Philips Hue added screen-sync devices, wall panels, rope lights and a gradient floor pole.","https://www.techradar.com/home/smart-lights/philips-hue-just-launched-over-a-dozen-new-smart-lights-and-accessories-heres-every-syncing-device-light-strip-and-wall-panel-worth-your-money"),
("3D Printing News","SHINING 3D's wireless FreeScan Trak Nova+ captures up to 7.6 million points per second.","https://www.voxelmatters.com/shining-3d-upgrades-the-freescan-trak-nova-scanning-system/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer a $2,000 AI client-meeting prep workflow to independent advisers; validate with three RIAs.","https://www.reuters.com/business/anthropic-targets-financial-advisers-with-new-claude-tool-2026-09-14/"),
("Anna Maria Island News","Anna Maria approved $436,000 to build the city pier's long-awaited T-end.","https://www.islander.org/"),
("Lake Oconee News","Tuesday Detroit-style pizza night brings a fresh local dining option to the Lake Oconee calendar.","https://lakeoconeelife.com/"),
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
    c.setTitle("Great Waters Gazette — Tuesday, September 15, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Tuesday, September 15, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 7:00 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Oregon National Historic Trail crossing Wyoming.")
    c.setFillColor(LINK); c.drawString(px,549,"Bureau of Land Management / Wikimedia Commons / Public domain (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Do the next right thing without needing applause; character becomes visible through quiet repetition.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
