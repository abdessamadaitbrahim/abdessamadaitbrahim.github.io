from PIL import Image, ImageDraw, ImageFont
import glob
W,H=1200,630
im=Image.new("RGB",(W,H),"#f4f6fa");d=ImageDraw.Draw(im)
d.rectangle([0,0,18,H],fill="#2447f5")
cands=glob.glob("/usr/share/fonts/**/*Serif*Bold*.ttf",recursive=True)+glob.glob("/usr/share/fonts/**/*.ttf",recursive=True)
fp=cands[0] if cands else None
f1=ImageFont.truetype(fp,84) if fp else ImageFont.load_default()
f2=ImageFont.truetype(fp,34) if fp else ImageFont.load_default()
d.text((90,190),"Abdessamad",font=f1,fill="#0b1020")
d.text((90,290),"Ait Brahim",font=f1,fill="#2447f5")
d.text((90,430),"Big Data & AI engineering student  |  NLP, Vision, Deep Learning",font=f2,fill="#44506a")
p=Image.open("assets/img/site/portrait.webp").convert("RGB").resize((330,351))
im.paste(p,(800,140))
im.save("assets/img/site/og.png",optimize=True)
