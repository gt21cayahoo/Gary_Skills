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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-13.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-12-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:The_Wounded_Angel_-_Hugo_Simberg.jpg"
WEATHER=[("Today","Mostly sunny (4%)","93 / 69"),("Mon 14","Sunny (6%)","96 / 73"),("Tue 15","Partly cloudy (23%)","91 / 67"),("Wed 16","Sunny (6%)","90 / 63"),("Thu 17","Sunny (6%)","91 / 64")]
STORIES=[
("AI Story of the Day","Reuters and CuttingRoom linked verified news footage to AI-assisted browser editing.","https://www.reuters.com/media-center/reuters-cuttingroom-partner-provide-newsrooms-with-ai-assisted-video-editing-2026-09-12/"),
("Microsoft 365 Copilot","Copilot opens cited Outlook emails beside chat; tip: review the source without context switching.","https://learn.microsoft.com/en-us/microsoft-365/copilot/release-notes"),
("ChatGPT","Box, Dropbox and SharePoint are now in Library; tip: keep a source file open beside your analysis.","https://help.openai.com/en/articles/6825453-chatgpt-release-notes"),
("Tesla Manufacturing & Expansion","Tesla says Cybercab's parallel-module line is five times faster and needs half the floor space.","https://247wallst.com/cards/tsla-xpost-01m21exw0xh2ccw9q9gtfc4jfs"),
("Lighting Industry — Story One","Canada's 50% retaliatory tariffs on U.S.-origin lighting products took effect September 8.","https://inside.lighting/news/26-09/canadas-50-lighting-tariffs-take-effect"),
("Lighting Industry — Story Two","A new study found even triple the usual daylight factor did not reliably support circadian timing.","https://inside.lighting/news/26-09/when-more-daylight-doesnt-mean-better-daylight"),
("3D Printing News","AltForm brings its four-laser Print Brilliance 400 metal AM platform to IMTS in Chicago.","https://www.voxelmatters.com/altform-to-show-metal-am-systems-at-imts-2026/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer local newsletters a $2,000 monthly AI video-repackaging service; test with three editors.","https://www.reuters.com/media-center/reuters-cuttingroom-partner-provide-newsrooms-with-ai-assisted-video-editing-2026-09-12/"),
("Anna Maria Island News","St. Bernard Catholic Church marked September 11 with a special Holmes Beach sermon.","https://amisun.com/"),
("Lake Oconee News","OPAS presents An Afternoon in Paris at the Reynolds Lake Oconee Lake Club today.","https://visitlakeoconee.com/events/month/2026-09/"),
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
    c.setTitle("Great Waters Gazette — Sunday, September 13, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Sunday, September 13, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:00 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: The Wounded Angel (1903), by Hugo Simberg.")
    c.setFillColor(LINK); c.drawString(px,549,"Hugo Simberg / Wikimedia Commons / public domain (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Let the day arrive before your judgments do; meet each task as it is, not as you feared it might be.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
