# Re-take chosen lines N times and keep the clearest take (highest voiced ratio) per line.
import sys,subprocess,librosa,numpy as np,shutil,json
sys.path.insert(0,'.');from vo_lines import LINES
from voicetut_tts import VoiceTutTTS
idx=[int(x) for x in sys.argv[1].split(',')];N=int(sys.argv[2])
tts=VoiceTutTTS.from_pretrained('/home/user/models/VoiceTut-TTS',device='cpu',dtype='float32',references='/home/user/mohammedaly22/VoiceTuT-TTS/reference_speakers/references.json')
def score(f):
    y,sr=librosa.load(f,sr=16000);f0,v,_=librosa.pyin(y,fmin=60,fmax=350,sr=sr,frame_length=1024);return float(np.mean(v))
for i in idx:
    best=(score(f'vo/vt{i}_raw.wav'),f'vo/vt{i}_raw.wav');print(i,'current',round(best[0],2),flush=True)
    for k in range(N):
        f=f'vo/vt{i}_take{k}.wav';tts.synthesize(LINES[i-1][0],speaker='Shaker',num_step=32,speed=1.05,output=f)
        s=score(f);print(i,'take',k,round(s,2),flush=True)
        if s>best[0]:best=(s,f)
    if best[1]!=f'vo/vt{i}_raw.wav':shutil.copy(best[1],f'vo/vt{i}_raw.wav')
    print(i,'kept',best[1],round(best[0],2),flush=True)
