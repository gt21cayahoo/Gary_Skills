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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-16.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-15-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Iglesia_del_colegio_de_los_Jesuitas,_Ponta_Delgada,_isla_de_San_Miguel,_Azores,_Portugal,_2020-07-30,_DD_09-11_HDR.jpg"
WEATHER=[("Today","Partly cloudy (4%)","89 / 64"),("Thu 17","Sunny (7%)","92 / 67"),("Fri 18","Partly cloudy (24%)","97 / 71"),("Sat 19","PM thunderstorms (48%)","93 / 70"),("Sun 20","Partly cloudy (24%)","91 / 70")]
STORIES=[
("AI Story of the Day","Anthropic signed its first Australian data-center lease for a 2.16-GW inference campus near Brisbane.","https://www.reuters.com/world/asia-pacific/anthropic-signs-first-australia-data-centre-agreement-2026-09-16/"),
("Microsoft 365 Copilot","Microsoft is testing Grok in Word, Excel and PowerPoint; tip: compare the same workbook task across models.","https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/grok-is-now-in-microsoft-copilot-but-dont-expect-snark-in-your-spreadsheets"),
("ChatGPT","Healthcare Public Data searches approved public sources; tip: review workspace permissions before connecting apps.","https://help.openai.com/en/articles/20001489-using-healthcare-public-data-in-chatgpt-and-codex"),
("Tesla Manufacturing & Expansion","Tesla plans 100-plus European Semi Megachargers as its Nevada factory targets 1,000 trucks weekly.","https://driveteslacanada.ca/news/tesla-semi-megacharger-network-europe-100-stalls/"),
("Lighting Industry — Story One","ArchLIGHT opened with smooth setup, zero drayage charges and its strongest education program yet.","https://edisonreport.com/2026/09/15/archlight-summit-day-0/"),
("Lighting Industry — Story Two","Sourcery linked its specification workspace with OASIS to connect designer schedules and agency sales workflows.","https://edisonreport.com/2026/09/14/sourcery-partners-with-oasis-sales-software/"),
("3D Printing News","VulcanForms and Specter will combine metal 3D printing and missile engineering for hypersonic production.","https://www.voxelmatters.com/vulcanforms-and-specter-aerospace-partner-on-us-hypersonic-manufacturing-capacity/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer a $2,500 AI data-residency readiness audit to Australian SaaS firms; validate with five CTOs.","https://www.reuters.com/world/asia-pacific/anthropic-signs-first-australia-data-centre-agreement-2026-09-16/"),
("Anna Maria Island News","Fire & Stone's owners regained property access and began planning repairs toward a possible reopening.","https://www.islander.org/2026/09/fire-stone-owners-move-toward-reopening/"),
("Lake Oconee News","Beginners Mahjong with Jan White meets from 6–8 tonight in the Lake Oconee area.","https://lakeoconeelife.com/calendar"),
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
    c.setTitle("Great Waters Gazette — Wednesday, September 16, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Wednesday, September 16, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 7:00 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Church of the Jesuit College, Ponta Delgada, Azores.")
    c.setFillColor(LINK); c.drawString(px,549,"Diego Delso / Wikimedia Commons / CC BY-SA 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Measure the day by the quality of your choices, not by how much attention they attract.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
