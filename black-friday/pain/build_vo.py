# Re-time scenes to the voice lines (tight gaps), rebuild voice.wav, and update the page's scene map.
import json,subprocess,re
LEAD,TAIL,END_HOLD=0.10,0.15,1.6
d=json.load(open('vo/durs.json'))
orig=[[0,4.7],[4.7,8.3],[8.3,11.3],[11.3,14.3],[14.3,17.9],[17.9,20.5],[20.5,28.0]]
lens=[LEAD+x+TAIL for x in d];lens[0]=max(lens[0],2.6);lens[-1]=LEAD+d[-1]+END_HOLD
new=[];t=0
for L in lens:new.append([round(t,3),round(t+L,3)]);t+=L
json.dump({'orig':orig,'new':new,'lead':LEAD,'dur':round(t,3)},open('vo/timing.json','w'))
ins=[];fl=[]
for i,(a,b) in enumerate(new):
    ins+=['-i',f'vo/line{i+1}.wav'];ms=int((a+LEAD)*1000);fl.append(f'[{i}:a]adelay={ms}|{ms}[v{i}]')
fc=';'.join(fl)+';'+''.join(f'[v{i}]' for i in range(len(new)))+f'amix=inputs={len(new)}:normalize=0,apad,atrim=0:{round(t,3)}[o]'
subprocess.run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',fc,'-map','[o]','-ar','48000','vo/voice.wav'],check=True)
s=open('pain.html').read()
s=re.sub(r"const SC_ORIG=.*?,SC_NEW=\[.*?\]\];",f"const SC_ORIG={json.dumps(orig)},SC_NEW={json.dumps(new)};",s,count=1,flags=re.S)
s=re.sub(r"window\.DURATION=[0-9.]+;window\.EVENTS=window\.EVENTS\.map",f"window.DURATION={new[-1][1]};window.EVENTS=window.EVENTS.map",s,count=1)
open('pain.html','w').write(s)
print('scenes',new,'total',round(t,2))
