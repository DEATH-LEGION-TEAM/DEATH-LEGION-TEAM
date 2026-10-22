import numpy as np, math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
random.seed(3); np.random.seed(3)
OUT='/mnt/user-data/outputs/readme-pack/assets'
def save(name, frames, ms=50):
    p=[f.convert('P',palette=Image.ADAPTIVE,colors=64) for f in frames]
    p[0].save(f'{OUT}/{name}',save_all=True,append_images=p[1:],duration=ms,loop=0,optimize=True,disposal=2)
    print(name, os.path.getsize(f'{OUT}/{name}')//1024,'KB')
W,H=360,200
BG=(9,9,11)

# 1 starfield warp
def warp():
    n=140; st=[[random.uniform(-1,1),random.uniform(-1,1),random.uniform(.1,1)] for _ in range(n)]
    fr=[]
    for f in range(60):
        im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
        for s in st:
            z0=s[2]; s[2]-=0.018
            if s[2]<=.02: s[0],s[1],s[2]=random.uniform(-1,1),random.uniform(-1,1),1; z0=1.02
            x0,y0=W/2+s[0]/z0*W*.5,H/2+s[1]/z0*H*.5
            x1,y1=W/2+s[0]/s[2]*W*.5,H/2+s[1]/s[2]*H*.5
            b=int(255*(1-s[2])); col=(min(255,120+b//2),60+b//3,min(255,200+b//4))
            d.line([x0,y0,x1,y1],fill=col,width=1 if s[2]>.5 else 2)
        fr.append(im)
    save('gif-warp.gif',fr,45)

# 2 matrix rain
def matrix():
    f_=ImageFont.load_default(); cols=W//10
    heads=[random.uniform(-H,0) for _ in range(cols)]; sp=[random.uniform(3,7) for _ in range(cols)]
    chars=[[random.choice('01') for _ in range(H//10+4)] for _ in range(cols)]
    fr=[]
    for f in range(60):
        im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
        for c in range(cols):
            heads[c]+=sp[c]
            if heads[c]>H+160: heads[c]=random.uniform(-80,0)
            for k in range(14):
                y=int(heads[c]-k*10)
                if 0<=y<H:
                    a=1-k/14; col=(int(255*a) if k==0 else int(120*a),int(255*a) if k==0 else int(60*a),int(255*a) if k==0 else int(240*a))
                    d.text((c*10,y),chars[c][(y//10)%len(chars[c])],fill=col,font=f_)
            if random.random()<.05: chars[c][random.randrange(len(chars[c]))]=random.choice('01')
        fr.append(im)
    save('gif-matrix.gif',fr,60)

# 3 plasma
def plasma():
    x,y=np.meshgrid(np.linspace(0,6,W//4),np.linspace(0,4,H//4)); fr=[]
    for f in range(32):
        t=f/32*2*math.pi
        v=np.sin(x*2+t)+np.sin(y*3-t)+np.sin((x+y)*2+t)+np.sin(np.hypot(x-3,y-2)*3-t*2)
        v=(v+4)/8
        r=(40+120*v**2).astype(np.uint8); g=(10+40*v).astype(np.uint8); b=(80+170*v).astype(np.uint8)
        im=Image.fromarray(np.dstack([r,g,b]),'RGB').resize((W,H),Image.BICUBIC).quantize(24).convert('RGB'); fr.append(im)
    save('gif-plasma.gif',fr,60)

# 4 radar
def radar():
    fr=[]; blips=[(random.uniform(0,2*math.pi),random.uniform(.2,.9)) for _ in range(9)]
    for f in range(60):
        a=f/60*2*math.pi
        im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); cx,cy,R=W//2,H//2,H//2-8
        for k in (1,.66,.33): d.ellipse([cx-R*k,cy-R*k,cx+R*k,cy+R*k],outline=(70,30,110))
        d.line([cx-R,cy,cx+R,cy],fill=(50,25,80)); d.line([cx,cy-R,cx,cy+R],fill=(50,25,80))
        sw=Image.new('RGB',(W,H),BG); sd=ImageDraw.Draw(sw)
        for k in range(30):
            aa=a-k*0.025; col=(int(140*(1-k/30)),int(40*(1-k/30)),int(30*(1-k/30)))
            sd.line([cx,cy,cx+R*math.cos(aa),cy+R*math.sin(aa)],fill=(int(220*(1-k/30)),int(30*(1-k/30)),int(40*(1-k/30))),width=3)
        im=Image.blend(im,sw,.0); im=Image.composite(sw,im,sw.convert('L').point(lambda v:255 if v>12 else 0))
        d=ImageDraw.Draw(im)
        d.line([cx,cy,cx+R*math.cos(a),cy+R*math.sin(a)],fill=(255,80,80),width=2)
        for ba,br in blips:
            diff=(a-ba)%(2*math.pi)
            if diff<2.2:
                al=1-diff/2.2; x=cx+R*br*math.cos(ba); y=cy+R*br*math.sin(ba); r=3+2*al
                d.ellipse([x-r,y-r,x+r,y+r],fill=(int(255*al),int(190*al),int(60*al)))
        fr.append(im)
    save('gif-radar.gif',fr,55)

# 5 oscilloscope waves
def waves():
    fr=[]
    for f in range(48):
        t=f/48*2*math.pi
        im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
        for gx in range(0,W,30): d.line([gx,0,gx,H],fill=(22,16,36))
        for gy in range(0,H,25): d.line([0,gy,W,gy],fill=(22,16,36))
        for k,(col,fq,amp,ph) in enumerate([((220,38,38),2,.35,0),((251,191,36),3,.22,1),((155,92,240),5,.15,2)]):
            pts=[(x,H/2+math.sin(x/W*2*math.pi*fq+t*(1+k)+ph)*H*amp*math.sin(x/W*math.pi+.3)) for x in range(0,W,3)]
            d.line(pts,fill=col,width=2)
        fr.append(im)
    fr=[f.filter(ImageFilter.GaussianBlur(.6)) for f in fr]
    save('gif-waves.gif',fr,55)

# 6 glitch bars
def glitch():
    base=np.zeros((H,W,3),np.uint8); base[:]=BG
    fr=[]
    for f in range(40):
        a=base.copy().astype(int)
        for _ in range(random.randint(2,6)):
            y=random.randrange(H-12); h=random.randint(3,16); x=random.randint(0,W//2); w=random.randint(40,W-x)
            col=random.choice([(220,38,38),(34,211,238),(139,43,226),(251,191,36)])
            a[y:y+h,x:x+w]=col
        shift=random.randint(-14,14)
        r=np.roll(a[...,0],shift,axis=1); b=np.roll(a[...,2],-shift,axis=1)
        a[...,0]=r; a[...,2]=b
        pass
        a[::3]=(a[::3]*.7).astype(int)
        fr.append(Image.fromarray(np.clip(a,0,255).astype(np.uint8)))
    save('gif-glitch.gif',fr,70)

# 7 neon rotating wireframe sphere + torus knot
def neon():
    S=240; fr=[]
    for f in range(60):
        th=2*math.pi*f/60
        im=Image.new('RGB',(S,S),BG); d=ImageDraw.Draw(im)
        pts=[]
        for i in range(260):
            t=2*math.pi*i/260; r=2+math.cos(3*t)
            p=(r*math.cos(2*t)/3,r*math.sin(2*t)/3,math.sin(3*t)/3)
            x,z=p[0]*math.cos(th)+p[2]*math.sin(th),-p[0]*math.sin(th)+p[2]*math.cos(th)
            y=p[1]*math.cos(.6)-z*math.sin(.6); z=p[1]*math.sin(.6)+z*math.cos(.6)
            k=5/(5+z); pts.append((S/2+x*k*80,S/2+y*k*80,z))
        gl=Image.new('RGB',(S,S),BG); gd=ImageDraw.Draw(gl)
        for i in range(len(pts)):
            a,b=pts[i],pts[(i+1)%len(pts)]; depth=(a[2]+1.3)/2.6
            col=(int(120+120*(1-depth)),int(40+60*(1-depth)),int(200+55*(1-depth)))
            gd.line([a[0],a[1],b[0],b[1]],fill=col,width=3 if depth<.5 else 2)
        blur=gl.filter(ImageFilter.GaussianBlur(4))
        im=Image.fromarray(np.clip(np.array(gl).astype(int)+np.array(blur).astype(int),0,255).astype(np.uint8))
        fr.append(im)
    save('gif-knot.gif',fr,50)

for fn in (plasma,glitch): fn()
