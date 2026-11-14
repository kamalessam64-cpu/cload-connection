# Egyptian voice-over with VoiceTut-TTS (fine-tuned on Egyptian Arabic). usage: python3 gen_vt.py [speaker=Shaker] [num_step=32]
import sys,json,subprocess,time
sys.path.insert(0,'.');from vo_lines import LINES
from voicetut_tts import VoiceTutTTS
spk=sys.argv[1] if len(sys.argv)>1 else 'Shaker';steps=int(sys.argv[2]) if len(sys.argv)>2 else 32
tts=VoiceTutTTS.from_pretrained('/home/user/models/VoiceTut-TTS',device='cpu',dtype='float32',
    references='/home/user/mohammedaly22/VoiceTuT-TTS/reference_speakers/references.json')
durs=[]
for i,(text,_,__) in enumerate(LINES):
    t0=time.time();raw=f'vo/vt{i+1}_raw.wav';out=f'vo/line{i+1}.wav'
    tts.synthesize(text,speaker=spk,num_step=steps,speed=1.05,output=raw)
    # trim edges, then shorten any pause longer than 0.25 s down to 0.15 s, so the delivery has no lag
    subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af',
      'silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse,'
      'silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-42dB:stop_silence=0.15',
      '-ar','48000','-ac','1',out],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    durs.append(round(d,3));print(i+1,f'{d:.2f}s',f'(took {time.time()-t0:.0f}s)',text,flush=True)
json.dump(durs,open('vo/durs.json','w'));print('total',round(sum(durs),2))
