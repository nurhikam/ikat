#!/usr/bin/env python3
"""OG v3 — polish: bigger sub, bigger pill, 2 phones larger"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = "/home/dev/work/ikat"
def lf(size, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()
def ts(draw, text, font):
    b=draw.textbbox((0,0),text,font=font)
    return b[2]-b[0], b[3]-b[1]
def rr(draw, xy, r, fill, outline=None, width=1):
    try: draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)
    except: draw.rectangle(xy, fill=fill, outline=outline, width=width)

W, H = 1200, 630
accent=(255,92,57)
white=(255,255,255)
img=Image.new("RGB",(W,H),accent)
draw=ImageDraw.Draw(img)
# subtle lighter circle top-right
light=tuple(int(a*0.92+255*0.08) for a in accent)
draw.ellipse((W-420,-100,W+60,380), fill=light)

# Pill — bigger
f_brand=lf(14, bold=True)
brand="IKAT  ·  101 TEMA  ·  22 KB"
bw,bh=ts(draw, brand, f_brand)
px, py=(W-(bw+28))//2, 28
rr(draw,(px,py,px+bw+28,py+bh+14),r=20,fill=white)
draw.text((px+14,py+7),brand,fill=accent,font=f_brand)

# Headline — bigger
f_h1=lf(64, bold=True)
line1="Undangan yang kebuka."
tw1,th1=ts(draw,line1,f_h1)
y1=py+bh+14+20
draw.text(((W-tw1)//2,y1),line1,fill=white,font=f_h1)

# Sub — bigger, semi-bold
f_sub=lf(20, bold=True)
sub="Bukan yang bikin tamu nunggu di parkiran."
tw2,th2=ts(draw,sub,f_sub)
draw.text(((W-tw2)//2,y1+th1+10),sub,fill=white,font=f_sub)

# 2 phones, larger
thumb_map={}
for p in glob.glob(os.path.join(ROOT,"site/thumbs","*.webp")):
    thumb_map[os.path.splitext(os.path.basename(p))[0]]=p
pick=["forest-lace","noir-editorial"]
card_w, card_h=260, 440
total_w=card_w*2+20
start_x=(W-total_w)//2
base_y=y1+th1+10+th2+24
for i,slug in enumerate(pick):
    cx=start_x+i*(card_w+20)
    cy=base_y+(6 if i==1 else 0)
    rr(draw,(cx+5,cy+5,cx+card_w+5,cy+card_h+5),r=14,fill=(0,0,0))
    rr(draw,(cx,cy,cx+card_w,cy+card_h),r=14,fill=white,outline=(230,230,230),width=1)
    tp=thumb_map.get(slug)
    if tp and os.path.exists(tp):
        thumb=Image.open(tp).convert("RGB")
        thumb=thumb.resize((card_w,card_h), Image.LANCZOS)
        mask=Image.new("L",(card_w,card_h),0)
        ImageDraw.Draw(mask).rounded_rectangle((0,0,card_w,card_h),radius=14,fill=255)
        img.paste(thumb,(cx,cy),mask)
        rr(draw,(cx,cy,cx+card_w,cy+card_h),r=14,fill=None,outline=(220,220,220),width=1)

# Bottom — ikat.id bigger
f_url=lf(13,bold=True)
url="ikat.id"
uw,uh=ts(draw,url,f_url)
draw.text(((W-uw)//2,H-26-uh),url,fill=white,font=f_url)

out=os.path.join(ROOT,"site/og.png")
img.save(out,"PNG")
print(f"{out}  ({W}x{H}, {os.path.getsize(out)/1024:.0f} KB)")
