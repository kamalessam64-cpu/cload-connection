# Music bed for the pain promo: dark drone + heartbeat (0-11.3s), near-silence for the turn, uplifting 124 BPM house from the drop (14.3s).
import wave,numpy as np
import json;TM=json.load(open('vo/timing.json'));SR=44100;DUR=TM['dur'];TURN=TM['new'][3][0];DROP=TM['new'][4][0];rng=np.random.default_rng(11)
T=lambda d:np.arange(int(d*SR))/SR
buf=np.zeros(int((DUR+1)*SR))
def add(x,at,g=1.):
    s=int(at*SR);e=min(len(buf),s+len(x))
    if 0<=s<len(buf):buf[s:e]+=x[:e-s]*g
def lp(x,fc):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X/(1+(f/fc)**4),len(x))
def bp(x,lo,hi):
    X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
saw=lambda f,d:2*((T(d)*f)%1)-1
def kick(d=.4,f0=120,f1=40):t=T(d);return np.sin(2*np.pi*np.cumsum(f1+(f0-f1)*np.exp(-t*30))/SR)*np.exp(-t*8)
def hat(d=.07):return bp(rng.standard_normal(int(d*SR)),7000,16000)*np.exp(-T(d)*30)
def clap(d=.25):x=bp(rng.standard_normal(int(d*SR)),900,4000);return x*np.exp(-T(d)*16)
def pluck(f,d):x=saw(f,d)+saw(f*1.006,d)*.7;return lp(x,f*6)*np.exp(-T(d)*7)
# 1) dark drone 0..14.3 (A minor), swelling, gone at the turn
d=DROP+.1;t=T(d);dr=sum(lp(saw(f,d)+saw(f*1.004,d),300) for f in (55,65.41,82.41))*.18
env=np.clip(t/2,0,1)*np.where(t<TURN,1,np.clip(1-(t-TURN)/1.2,0,1));add(dr*env,0)
# heartbeat (lub-dub) every 1.05 s until the turn
x=0.0
while x<TURN-.3:add(kick(.3,90,38),x,.9);add(kick(.25,80,36),x+.22,.55);x+=1.05
# 2) drop at 14.3: 124 BPM house, Am - F - C - G
bt=60/124;chords=[(220,261.63,329.63),(174.61,220,261.63),(261.63,329.63,392),(196,246.94,293.66)];roots=[55,43.65,65.41,49]
t0=DROP;i=0
while t0+i*bt<DUR-.3:
    tt=t0+i*bt;beat=i%4;bar=(i//4)%4
    add(kick(),tt,.95);add(hat(),tt+bt*.5,.35)
    if beat in(1,3):add(clap(),tt,.5)
    for s in range(4):add(hat(.04),tt+s*bt/4,.12)
    add(lp(saw(roots[bar]*2,bt*.45),400)*np.exp(-T(bt*.45)*5),tt+bt*.5,.5)
    for s in range(2):add(pluck(chords[bar][(i*2+s)%3]*2,bt*.5),tt+s*bt/2,.22)
    i+=1
# pad under the drop
d2=DUR-DROP;pad=sum(lp(saw(f,d2)+saw(f*1.005,d2),900) for f in (220,261.63,329.63))*.05;add(pad*np.clip(T(d2)/1.5,0,1),DROP)
out=np.tanh(buf[:int(DUR*SR)+int(.003*SR)]*1.1);out*=np.clip((DUR-np.arange(len(out))/SR)/.6,0,1);out=out/np.abs(out).max()*.9
st=np.stack([out,np.roll(out,int(.0005*SR))],1)
w=wave.open('out/pain-bed.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes());w.close();print('bed ok')
