# usage: python3 audio.py opt1|opt2|opt3  -> out/<opt>.wav ; sounds are synthesized and timed to out/<opt>.events.json
import sys,json,wave,numpy as np
SR=44100
rng=np.random.default_rng(7)
def t_(d):return np.arange(int(d*SR))/SR
def bp(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);m=((f>=lo)&(f<=hi)).astype(float)
    k=max(1,int(4*len(x)/SR));m=np.convolve(m,np.ones(k)/k,'same');return np.fft.irfft(X*m,len(x))
def noise(d):return rng.standard_normal(int(d*SR))
def sweep(f0,f1,d,curve=1):
    t=t_(d);fr=f0+(f1-f0)*(t/d)**curve;return np.sin(2*np.pi*np.cumsum(fr)/SR)
def kick(d=.45,f0=140,f1=42):
    t=t_(d);fr=f1+(f0-f1)*np.exp(-t*28);return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*7)+.25*np.exp(-t*400)*noise(d)
def k808(d=1.2,f=48):
    t=t_(d);fr=f*(1+1.6*np.exp(-t*30));return np.tanh(2.2*np.sin(2*np.pi*np.cumsum(fr)/SR))*np.exp(-t*2.6)
def boom(d=1.6):
    t=t_(d);x=np.sin(2*np.pi*np.cumsum(70*np.exp(-t*1.5)+30)/SR)*np.exp(-t*2.2)+.5*bp(noise(d),40,400)*np.exp(-t*4);return np.tanh(2*x)
def bigboom(d=2.4):
    t=t_(d);x=np.sin(2*np.pi*np.cumsum(90*np.exp(-t*1.8)+28)/SR)*np.exp(-t*1.4)+.6*bp(noise(d),30,900)*np.exp(-t*2.2)+.25*bp(noise(d),2000,9000)*np.exp(-t*3);return np.tanh(2.4*x)
def impact(d=1.2):
    t=t_(d);x=np.sin(2*np.pi*np.cumsum(120*np.exp(-t*6)+45)/SR)*np.exp(-t*4)+.5*bp(noise(d),200,6000)*np.exp(-t*9);return np.tanh(2*x)
def hit(d=.35):
    t=t_(d);return np.tanh(2*(np.sin(2*np.pi*np.cumsum(180*np.exp(-t*30)+60)/SR)*np.exp(-t*12)+.5*bp(noise(d),500,5000)*np.exp(-t*20)))
def tick(d=.06):return bp(noise(d),3000,9000)*np.exp(-t_(d)*60)
def whoosh(d=.7):
    n=noise(d);t=t_(d);o=np.zeros_like(n)
    for i in range(6):
        c=500+i*i*400;o+=bp(n,c*.6,c*1.6)*np.sin(np.pi*np.clip((t/d)+(5-i)*.02,0,1))**2/(i+1)
    return o*1.5
def riser(d=1.0):
    t=t_(d);n=bp(noise(d),500,9000)*(t/d)**2;s=sweep(200,2400,d,2)*(t/d)**2*.4
    e=np.ones(len(t));e[-int(.03*SR):]*=np.linspace(1,0,int(.03*SR));return (n*.9+s)*e
def roll(d=.4):
    n=max(2,int(d/.05));o=np.zeros(int(d*SR)+int(.1*SR))
    for i in range(n):
        h=hit(.1)*(.4+.6*i/n);s=int(i*.05*SR);o[s:s+len(h)]+=h
    return o
def hat(d=.08,o=False):return bp(noise(d),6000,16000)*np.exp(-t_(d)*(25 if not o else 8))
def clap(d=.3):
    x=bp(noise(d),900,4500);e=np.zeros(len(x))
    for k in (0,.012,.024):
        n0=int(k*SR);e[n0:]+=np.exp(-np.arange(len(e)-n0)/SR*(40 if k<.024 else 14))
    return x*e
def snare(d=.3):
    t=t_(d);return np.tanh(1.5*(bp(noise(d),1500,9000)*np.exp(-t*18)+np.sin(2*np.pi*190*t)*np.exp(-t*25)*.7))
def saw(f,d):
    t=t_(d);return 2*((t*f)%1)-1
def pluck(f,d=.25):
    x=saw(f,d)+saw(f*1.005,d)*.8;return bp(x,max(60,f*.8),f*8+2000)*np.exp(-t_(d)*9)
def add(buf,x,at,g=1.0):
    s=int(at*SR)
    if s<0 or s>=len(buf):return
    e=min(len(buf),s+len(x));buf[s:e]+=x[:e-s]*g
def mix(*xs):
    n=max(len(x) for x in xs);o=np.zeros(n)
    for x in xs:o[:len(x)]+=x
    return o
EV={'riser':lambda a:riser(a or 1.0),'boom':lambda a:boom(),'bigboom':lambda a:bigboom(),'impact':lambda a:impact(),'whoosh':lambda a:whoosh(),
 'tick':lambda a:tick(),'hit':lambda a:hit(),'drop':lambda a:k808(1.6,46),'kick808':lambda a:mix(k808(1.0,50),kick(.3)*.8),
 'roll':lambda a:roll(a or .4),'edmdrop':lambda a:mix(kick(.45),boom(1.2)*.6)}
GAIN={'riser':.55,'boom':.9,'bigboom':1.0,'impact':.9,'whoosh':.5,'tick':.5,'hit':.8,'drop':1.0,'kick808':.9,'roll':.5,'edmdrop':1.0}
opt=sys.argv[1];BED=len(sys.argv)>2 and sys.argv[2]=='--bed';J=json.load(open(f'out/{opt}.events.json'));dur=J['dur']
buf=np.zeros(int((dur+1)*SR))
for ev in J['events']:
    name=ev[1];arg=ev[2] if len(ev)>2 else None
    if BED and name not in('drop','kick808'):continue
    add(buf,EV[name](arg),ev[0],GAIN[name])
def bed(bpm,start,end,style):
    bt=60/bpm;i=0;t=start
    root=[55.0,55.0,43.65,49.0]
    arp=[[220,261.63,329.63],[220,261.63,329.63],[174.61,220,261.63],[196,246.94,293.66]]
    while t<end-1e-6:
        beat=i%4;bar=(i//4)%4
        if style=='trap':
            if beat==0:add(buf,kick(),t,.8)
            if beat==2:add(buf,snare(),t,.7)
            if beat in(1,3):add(buf,k808(bt*1.6,root[bar]),t+bt*.5,.55)
            for s in range(4):add(buf,hat(),t+s*bt/4,.22 if s%2 else .32)
            if i%8==7:
                for s in range(8):add(buf,hat(),t+s*bt/8,.2)
            for s in range(2):add(buf,pluck(arp[bar][(i*2+s)%3]*2,bt*.5),t+s*bt/2,.18)
        elif style=='house':
            add(buf,kick(),t,.95)
            add(buf,hat(.2,True),t+bt*.5,.25)
            if beat in(1,3):add(buf,clap(),t,.55)
            for s in range(4):add(buf,hat(),t+s*bt/4,.12)
            add(buf,pluck(root[bar]*2,bt*.45),t+bt*.5,.55);add(buf,pluck(root[bar]*4,bt*.2),t+bt*.75,.3)
            for s in range(2):add(buf,pluck(arp[bar][(i+s)%3]*2,bt*.5),t+s*bt/2,.25)
        else:
            if beat==0:add(buf,boom(bt*1.5),t,.55)
            if beat%2==0:add(buf,kick(),t,.7)
            if beat in(1,3):add(buf,snare(),t,.35)
            for s in range(2):add(buf,hat(),t+s*bt/2,.2)
            add(buf,pluck(root[bar]*2,bt*.9),t,.45)
        i+=1;t+=bt
if opt=='opt1':
    d=t_(dur);dr=np.sin(2*np.pi*55*d)*(.1+.15*np.clip(d/6,0,1))+np.sin(2*np.pi*82.4*d)*.05;buf[:len(dr)]+=dr
    bed(120,5.4,9.4,'cine');bed(120,11.4,15.6,'house')
elif opt=='opt2':
    bt=60/140;bed(140,4*bt,dur-.4,'trap')
else:
    bt=60/128;bed(128,7*bt,24*bt,'house');bed(128,25*bt,dur-.3,'house')
L=int(dur*SR)+(int(.003*SR) if BED else 0);buf=buf[:L];buf=np.tanh(buf*1.1);buf*=np.clip((dur-np.arange(len(buf))/SR)/.35,0,1)
buf=buf/np.max(np.abs(buf))*.92
st=np.stack([buf,np.roll(buf,int(.0004*SR))],1)
w=wave.open(f'out/{opt}{"-bed" if BED else ""}.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes());w.close()
print(opt,'audio',round(len(buf)/SR,1),'s')
