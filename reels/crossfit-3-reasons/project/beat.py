# Original 124 BPM upbeat bed (no third-party music) for the reel -> bg-audio.mp3
import numpy as np,wave,subprocess
SR=44100;DUR=18.6;rng=np.random.default_rng(3);T=lambda d:np.arange(int(d*SR))/SR
buf=np.zeros(int((DUR+1)*SR))
def add(x,at,g=1.):
    s=int(at*SR);e=min(len(buf),s+len(x))
    if 0<=s<len(buf):buf[s:e]+=x[:e-s]*g
def lp(x,fc):X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X/(1+(f/fc)**4),len(x))
def bp(x,lo,hi):X=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/SR);return np.fft.irfft(X*((f>=lo)&(f<=hi)),len(x))
saw=lambda f,d:2*((T(d)*f)%1)-1
def kick(d=.4):t=T(d);return np.sin(2*np.pi*np.cumsum(40+80*np.exp(-t*30))/SR)*np.exp(-t*8)
def hat(d=.06):return bp(rng.standard_normal(int(d*SR)),7000,16000)*np.exp(-T(d)*35)
def clap(d=.22):x=bp(rng.standard_normal(int(d*SR)),900,4000);return x*np.exp(-T(d)*16)
def pluck(f,d):x=saw(f,d)+saw(f*1.006,d)*.7;return lp(x,f*6)*np.exp(-T(d)*7)
bt=60/124;chords=[(220,261.63,329.63),(174.61,220,261.63),(261.63,329.63,392),(196,246.94,293.66)];roots=[55,43.65,65.41,49]
i=0
while i*bt<DUR-.2:
    t=i*bt;beat=i%4;bar=(i//4)%4;intro=t<1.9
    if not intro:add(kick(),t,.9)
    add(hat(),t+bt*.5,.3)
    if beat in(1,3) and not intro:add(clap(),t,.45)
    for s in range(4):add(hat(.035),t+s*bt/4,.1)
    add(lp(saw(roots[bar]*2,bt*.45),380)*np.exp(-T(bt*.45)*5),t+bt*.5,.45 if not intro else .2)
    for s in range(2):add(pluck(chords[bar][(i*2+s)%3]*2,bt*.5),t+s*bt/2,.2)
    i+=1
out=np.tanh(buf[:int(DUR*SR)]*1.1);n=len(out);out*=np.clip(np.arange(n)/SR/.3,0,1)*np.clip((DUR-np.arange(n)/SR)/.8,0,1);out=out/np.abs(out).max()*.9
st=np.stack([out,np.roll(out,int(.0005*SR))],1)
w=wave.open('/tmp/claude-0/-home-user-cload-connection/7cf9c7eb-dc35-5bb1-b714-1954d7878076/scratchpad/beat.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype('<i2').tobytes());w.close()
subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/claude-0/-home-user-cload-connection/7cf9c7eb-dc35-5bb1-b714-1954d7878076/scratchpad/beat.wav','-b:a','256k','/root/Documents/video-editor-bassam/projects/x7-reel-1/bg-audio.mp3'],check=True);print('bg-audio.mp3 ok')
