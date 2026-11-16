# Virtual camera: crop follows the speaker's face (smoothed per source shot), zoom curve keyed to her words,
# zoom-punch transitions on the source cuts / sentence starts. Output cam/camera.mp4 (1080x1920, 30 fps, silent).
import cv2,json,numpy as np,subprocess
W='/root/Documents/video-editor-bassam/projects/x7-reel-1'
T=json.load(open(W+'/cam/track.json'));caps=json.load(open(W+'/caps.json'))['cards']
fps=T['fps'];N=T['frames'];FW,FH=1080,1920
CUTS=[3.533,11.267,13.367]                     # source shot changes (ffmpeg scene detect)
tr=np.array(T['track']);t_all=np.arange(N)/fps
# per-shot outlier rejection: keep detections whose size and position match the speaker in that shot
edges=[0]+CUTS+[1e9];keep=[]
for s0,s1 in zip(edges,edges[1:]):
    seg=tr[(tr[:,0]>=s0)&(tr[:,0]<s1)]
    if not len(seg):continue
    mh=np.median(seg[:,3]);seg=seg[(seg[:,3]>0.65*mh)&(seg[:,3]<1.5*mh)]
    mx=np.median(seg[:,1]);seg=seg[np.abs(seg[:,1]-mx)<320]
    keep.append(seg)
tr=np.vstack(keep);print('kept',len(tr),'detections')
def interp(col):return np.interp(t_all,tr[:,0],tr[:,col])
cx,cy,fh=interp(1),interp(2),interp(3)
# smooth inside each shot only, so the camera cuts with the source instead of sliding across a cut
bounds=[0]+[int(round(c*fps)) for c in CUTS]+[N]
def smooth(a,sig):
    o=a.copy()
    for s,e in zip(bounds,bounds[1:]):
        seg=a[s:e];k=int(sig*3)*2+1
        if len(seg)>k:
            pad=np.pad(seg,(k//2,k//2),mode='edge');g=np.exp(-0.5*((np.arange(k)-k//2)/sig)**2);g/=g.sum()
            o[s:e]=np.convolve(pad,g,'valid')
    return o
cx,cy,fh=smooth(cx,9),smooth(cy,9),smooth(fh,12)
# zoom curve (1 = full frame). Keyframes per sentence: settle, then punch on the key word.
def wt(word):
    for c in caps:
        for w in c['w']:
            if w['t']==word:return w['s']
    return None
K=[(0.00,1.22),(3.30,1.55),                                   # hook: slow push-in on the question
   (3.53,1.35),(wt('٣') or 3.73,1.62),(5.99,1.50),            # "٣ أسباب" punch
   (6.01,1.30),(wt('تمرينة') or 9.3,1.42),(11.25,1.50),       # list: gentle drift in
   (11.267,1.68),(13.19,1.72),                                # "مش كفاية": tight
   (13.367,1.18),(wt('تبعتلنا') or 15.6,1.30),(wt('«جوب»') or 16.3,1.55),(18.59,1.45)]  # CTA: wide then push on the keyword
kt=np.array([k[0] for k in K]);kz=np.array([k[1] for k in K])
def ease(x):return x*x*(3-2*x)
Z=np.empty(N)
for i,t in enumerate(t_all):
    j=np.searchsorted(kt,t,side='right')-1;j=max(0,min(j,len(kt)-2))
    a,b=kt[j],kt[j+1];x=0 if b<=a else min(1,max(0,(t-a)/(b-a)));Z[i]=kz[j]+(kz[j+1]-kz[j])*ease(x)
# transition punch: short overshoot + blur around each cut / sentence start
TR=sorted(set(CUTS+[6.01]))
def bump(t):
    v=0
    for c in TR:
        d=(t-c)*fps
        if -3<=d<=5: v=max(v,np.exp(-0.5*(d/2.0)**2))
    return v
# ── B-roll inserts from X7's Instagram (CrossFit only), matched to her words.
# (reel start, reel end, file, source start, crop x,y,w,h, mode)  mode: full = fill the frame, card = sharp card on blurred fill
IG='/root/Documents/video-editor-bassam/projects/x7-reel-1/ig/'
INS=[(1.19,1.70,'cg01.mp4',6.0,(90,0,540,960),'full'),          # "الكروسفيت": Combat Games barbell floor
     (3.00,3.50,'DfxKXJXgWAL.mp4',14.0,None,'full'),             # "صعبة؟": handstand on parallettes
     (7.93,8.65,'DWrN2QOtFSL.mp4',25.0,(112,230,496,425),'card'),# "الكونديشنينج": HYROX sled push
     (8.65,9.40,'DfxKXJXgWAL.mp4',5.0,None,'full'),              # "والجيمناستيكس": handstand push-up
     (9.85,10.55,'cg02.mp4',1.9,(270,0,810,1440),'full'),        # "والسترينث": barbell clean
     (17.27,18.05,'DfxKXJXgWAL.mp4',18.7,None,'full')]           # "كل التفاصيل": dips on the X7 PLUS rig
caps_={}
def grab(fn,t):
    c=caps_.get(fn)
    if c is None:c=caps_[fn]=cv2.VideoCapture(IG+fn)
    c.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=c.read();return f
def fit(img,w,h,z=1.0,y_anchor=0.4):
    ih,iw=img.shape[:2];ch=ih/z;cw=ch*w/h
    if cw>iw:cw=iw/z;ch=cw*h/w
    x0=(iw-cw)/2;y0=(ih-ch)*y_anchor
    M=np.float32([[w/cw,0,-x0*w/cw],[0,h/ch,-y0*h/ch]])
    return cv2.warpAffine(img,M,(w,h),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
def sharpen(o):bl=cv2.GaussianBlur(o,(0,0),1.6);return cv2.addWeighted(o,1.5,bl,-0.5,0)
def insert_frame(t):
    for s0,s1,fn,src0,crop,mode in INS:
        if s0<=t<s1:
            f=grab(fn,src0+(t-s0))
            if f is None:return None
            if crop:x,y,w,h=crop;f=f[y:y+h,x:x+w]
            k=(t-s0)/(s1-s0);z=1.0+0.08*k
            if mode=='full':return sharpen(fit(f,FW,FH,z))
            bg=cv2.GaussianBlur(fit(f,FW//4,FH//4,1.3),(0,0),6);bg=cv2.resize(bg,(FW,FH));bg=(bg*0.45).astype(np.uint8)
            cw=980;ch=int(cw*f.shape[0]/f.shape[1]);card=sharpen(fit(f,cw,ch,z))
            x0=(FW-cw)//2;y0=int(FH*0.40-ch/2);bg[y0:y0+ch,x0:x0+cw]=card
            cv2.rectangle(bg,(x0-6,y0-6),(x0+cw+6,y0+ch+6),(42,230,166),6)   # lime frame (BGR)
            return bg
    return None
TR=sorted(set(TR+[x for ins in INS for x in (ins[0],ins[1])]))
src=cv2.VideoCapture(W+'/cutz_orig.mp4')
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{FW}x{FH}','-r',str(fps),'-i','-',
    '-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',W+'/cam/camera.mp4'],stdin=subprocess.PIPE)
for i in range(N):
    ok,f=src.read()
    if not ok:break
    ins=insert_frame(t_all[i])
    b=bump(t_all[i]);z=Z[i]*(1+0.10*b)
    ch=FH/z;cw=ch*FW/FH
    x0=cx[i]-cw/2; y0=cy[i]-0.30*ch            # face centred, sitting at 30% from the top
    x0=min(max(0,x0),FW-cw);y0=min(max(0,y0),FH-ch)
    M=np.float32([[FW/cw,0,-x0*FW/cw],[0,FH/ch,-y0*FH/ch]])
    o=cv2.warpAffine(f,M,(FW,FH),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_REPLICATE)
    if ins is not None:o=ins
    if b>0.05:                                 # zoom-blur on the punch frames
        acc=o.astype(np.float32);n=5
        for k in range(1,n):
            s=1+0.025*b*k;Ms=cv2.getRotationMatrix2D((FW/2,FH*0.30),0,s)
            acc+=cv2.warpAffine(o,Ms,(FW,FH),borderMode=cv2.BORDER_REPLICATE)
        o=(acc/n).astype(np.uint8)
    enc.stdin.write(o.tobytes())
enc.stdin.close();enc.wait()
json.dump({'zoom':[round(z,3) for z in Z[::15]]},open(W+'/cam/zoom_preview.json','w'))
print('camera.mp4 done',N,'frames')
