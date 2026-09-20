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
OUT=ROOT.parent/"output"/"pdf"/"Great_Waters_Gazette_2026-09-20.pdf"
ARCHIVE=ROOT/"archive"/OUT.name
PHOTO=ROOT/"assets"/"2026-09-19-picture-of-the-day.jpg"
CREAM=HexColor("#FBF7E9"); NAVY=HexColor("#173A5E"); LINK=HexColor("#0B5EA8"); TEXT=HexColor("#151515")
pdfmetrics.registerFont(TTFont("DVSans","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVSansBold","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVSansOblique","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
WEATHER_URL="https://weather.com/us/georgia/eatonton/postcode/31024/tenday"
PHOTO_URL="https://commons.wikimedia.org/wiki/File:Zitting_Cisticola_in_Bhigwan_August_2025_by_Tisha_Mukherjee_01.jpg"
WEATHER=[("Today","Partly cloudy (15%)","90 / 69"),("Mon 21","Mostly sunny (15%)","94 / 70"),("Tue 22","PM thunderstorms (63%)","91 / 70"),("Wed 23","Scattered storms (51%)","82 / 64"),("Thu 24","AM clouds/PM sun (22%)","78 / 60")]
STORIES=[
("AI Story of the Day","The IMF says AI could lift European productivity 1% in five years while widening inequality and straining power grids.","https://www.reuters.com/business/imf-tells-eu-ministers-ai-could-boost-growth-increase-economic-strains-2026-09-19/"),
("Microsoft 365 Copilot","Microsoft says outcome-led Copilot workflows lifted close rates 20%; tip: redesign one process before scaling licenses.","https://blogs.microsoft.com/blog/2026/09/17/what-weve-learned-from-microsofts-own-ai-transformation/"),
("ChatGPT","OpenAI plans to retire custom GPTs; tip: migrate, test and review plugin access before switching.","https://help.openai.com/en/articles/8554407-gpts-in-chatgpt"),
("Tesla Manufacturing & Expansion","Barclays says Shanghai makes over half of Tesla's vehicles and exports nearly half its output.","https://www.barrons.com/articles/tesla-stock-shanghai-gigafactory-7bb4795b"),
("Lighting Industry — Story One","Casambi is restructuring North American sales around local rep agencies.","https://edisonreport.com/2026/09/18/casambi-north-america-rep-agency-strategy/"),
("Lighting Industry — Story Two","Amerlux says serviceability and long-term performance still separate quality lighting from low-cost alternatives.","https://edisonreport.com/2026/09/18/quality-lighting-bill-plageman/"),
("3D Printing News","Stratasys won $27.6 million after a jury found Bambu Lab willfully infringed four 3D-printing patents.","https://www.voxelmatters.com/stratasys-wins-27-6-million-verdict-against-bambu-lab-in-first-of-two-patent-trials/"),
("Porsche 997 & 911","No worthwhile unused standard 997 road-car item remains in the verified three-month queue.",""),
("AI-Powered Solopreneur Business","Offer a $5,000 AI workflow-redesign sprint; validate it by mapping one stalled sales process with three managers.","https://blogs.microsoft.com/blog/2026/09/17/what-weve-learned-from-microsofts-own-ai-transformation/"),
("Anna Maria Island News","Three Holmes Beach commission candidates debated taxes, rentals and tourist funding in an LWV forum.","https://www.islander.org/2026/09/lwv-hosts-hb-candidate-forum/"),
("Lake Oconee News","The Concert Truck brings an outdoor OPAS performance to Harbor Club at 7 tonight.","https://lakeoconeelife.com/lake-oconee-calendar-of-events/opas-pop-up-series-the-concert-truck-returns0920"),
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
    c.setTitle("Great Waters Gazette — Sunday, September 20, 2026"); c.setAuthor("Great Waters Gazette")
    c.setFillColor(CREAM); c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(TEXT); c.setFont("DVSansBold",28); c.drawCentredString(W/2,752,"Great Waters Gazette")
    c.setFont("DVSans",11); c.drawCentredString(W/2,731,"Sunday, September 20, 2026")
    left,right=40,572; top=704; gap=16; ww=195; px=left+ww+gap; pw=right-px
    c.setFont("DVSansBold",13); c.drawString(left,top,"ZIP 31024 — 5-Day Forecast")
    c.setStrokeColor(NAVY); c.line(left,top-6,left+ww,top-6); y=top-25
    for d,s,t in WEATHER:
        c.setFillColor(TEXT); c.setFont("DVSansBold",8.1); c.drawString(left,y,d)
        c.setFont("DVSans",6.8); c.drawString(left+47,y,s); c.drawRightString(left+ww,y,t); y-=16
    c.setFillColor(LINK); c.setFont("DVSans",7.3); lab="Weather Channel — 6:05 AM EDT"; c.drawString(left,y-1,lab)
    c.linkURL(WEATHER_URL,(left,y-3,left+stringWidth(lab,"DVSans",7.3),y+8),relative=0)
    cover(c,PHOTO,px,570,pw,134); c.linkURL(PHOTO_URL,(px,570,right,704),relative=0)
    c.setFillColor(TEXT); c.setFont("DVSans",6.8); c.drawString(px,559,"Yesterday's Picture: Zitting cisticola in Bhigwan, Maharashtra, India.")
    c.setFillColor(LINK); c.drawString(px,549,"Tisha Mukherjee / Wikimedia Commons / CC BY-SA 4.0 (cropped)")
    c.linkURL(PHOTO_URL,(px,547,right,558),relative=0)
    c.setFillColor(NAVY); c.roundRect(left,509,right-left,31,4,stroke=1,fill=0)
    c.setFont("DVSansBold",9); c.drawString(left+8,528,"Today's Stoic Practice")
    c.setFillColor(TEXT); c.setFont("DVSansOblique",7.4); c.drawString(left+8,516,"Meet delay without complaint: control your response, not the timing.")
    c.setFillColor(LINK); c.drawRightString(right-8,516,"Daily Stoic"); c.linkURL("https://dailystoic.com/podcast/",(right-66,514,right-8,524),relative=0)
    y=486
    for h,s,u in STORIES:
        c.setFillColor(TEXT); c.setFont("DVSansBold",9.5); c.drawString(left,y,h)
        c.setStrokeColor(NAVY); c.line(left,y-3,right,y-3); line(c,left+3,y-16,s,u,right-left-3); y-=40
    c.setFillColor(NAVY); c.setFont("DVSansOblique",7); c.drawCentredString(W/2,25,"A concise morning digest — sources linked in every section")
    c.showPage(); c.save(); ARCHIVE.parent.mkdir(exist_ok=True); shutil.copyfile(OUT,ARCHIVE); print(OUT)
if __name__=="__main__": build()
