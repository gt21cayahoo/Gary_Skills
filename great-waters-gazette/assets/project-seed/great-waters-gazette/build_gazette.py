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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-17.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-16-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Eurasian_coot_(Fulica_atra)_with_chicks.jpg"
WEATHER=[("Today","Sunny (3%)","92 / 66"),("Fri 18","Mostly sunny (15%)","96 / 71"),("Sat 19","PM thunderstorms (59%)","93 / 71"),("Sun 20","PM thunderstorms (38%)","90 / 70"),("Mon 21","PM thunderstorms (48%)","92 / 70")]
STORIES=[
("AI Story of the Day","OpenAI launched a systematic misalignment-disclosure framework and published six concerning-behavior reports.","https://openai.com/index/model-misalignment-reporting-framework/"),
("Microsoft 365 Copilot","Brand Kit now shares custom PowerPoint skills; tip: publish one approved deck workflow for the whole team.","https://support.microsoft.com/en-us/powerpoint/copilot/brand-skill-support-copilot-powerpoint"),
("ChatGPT","ChatGPT is testing labeled sponsored business agents; tip: keep promotion separate from independent answers.","https://www.reuters.com/business/media-telecom/openai-tests-advertiser-sponsored-agents-expands-ai-tools-chatgpt-ads-2026-09-16/"),
("Tesla Manufacturing & Expansion","Tesla is weighing a $10.1 billion Fort Bend solar factory after winning a 10-year local tax break.","https://www.axios.com/local/houston/2026/09/16/tesla-solar-plant-fort-bend-county-lamar-cisd-tax-incentive"),
("Lighting Industry — Story One","ArchLIGHT showed practical AI for Revit automation, submittal reviews and lighting visualization.","https://edisonreport.com/2026/09/16/ai-for-lighting-designers-ardra-zinkon/"),
("Lighting Industry — Story Two","NEMA's business-confidence index rose to 65.8 as orders, grid upgrades and data centers supported demand.","https://inside.lighting/news/26-09/electrical-manufacturers-see-stronger-business-conditions"),
("3D Printing News","Rainshow revived Beamit's aerospace unit as it installed EMEA's first six-laser EOS M4 ONYX.","https://www.voxelmatters.com/beamit-survives-insolvency-under-rainshow-and-installs-eoss-newest-metal-printer/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer a $3,000 branded Copilot-skill setup; validate it with three midmarket presentation managers.","https://support.microsoft.com/en-us/powerpoint/copilot/brand-skill-support-copilot-powerpoint"),
("Anna Maria Island News","Holmes Beach seeks county and FDOT help to curb rental congestion at Kingfish Boat Ramp.","https://www.islander.org/2026/09/hb-seeks-help-to-retain-boat-ramp-access/"),
("Lake Oconee News","Table at the Lake serves its featured Smash Burger from 5–9 tonight in Greensboro.","https://lakeoconeelife.com/lake-oconee-calendar-of-events/smash-burger0917"),
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
    c.setTitle("Great Waters Gazette — Thursday, September 17, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Thursday, September 17, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:07 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Eurasian coot with chicks in Trujillo, Spain.")
    c.setFillColor(LINK); c.drawString(px,549,"Charles J. Sharp / Wikimedia Commons / CC BY-SA 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Use today's uncertainty as practice: choose the next useful action, then release the rest.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
