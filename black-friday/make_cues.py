# Turn each option's on-screen EVENTS into a cues.json + swaps.json for the sound-effects skill (real CC0 files, picked per hit).
import json,sys,itertools
opt=sys.argv[1];J=json.load(open(f'out/{opt}.events.json'))
BIG=itertools.cycle(['impact/fs-347561-micheal-bay-hit.ogg','impact/fs-177242-cinematic-impact.ogg'])
MID=itertools.cycle(['impact/fs-222517-dramatic-hit.ogg','impact/kenney-sci-lowfrequency-explosion-000.ogg','impact/kenney-sci-lowfrequency-explosion-001.ogg'])
HIT=itertools.cycle(['impact/kenney-impact-impactpunch-heavy-000.ogg','impact/kenney-impact-impactpunch-heavy-001.ogg'])
RIS=itertools.cycle(['riser/fs-685256-riser-sound-effect-short-wav.ogg','kit/riser.ogg','riser/fs867126.ogg','riser/fs-396161-scary-hits-risers-001.ogg'])
WHO=itertools.cycle(['whoosh/fs-683101-quick-woosh.ogg','transition/fs-786514-swoosh-v2.ogg','whoosh/fs-127197-fast-simple-chop-5-aif.ogg'])
cues=[];swaps={}
for ev in J['events']:
    t,name=ev[0],ev[1];arg=ev[2] if len(ev)>2 else None
    if name in('drop','kick808'):continue            # these stay in the music bed
    if name=='riser' or name=='roll':c={'t':t,'type':'build_up','dur':arg or .8,'desc':name};f=next(RIS)
    elif name in('bigboom','edmdrop'):c={'t':t,'type':'reveal','desc':'big hit'};f=next(BIG)
    elif name in('boom','impact'):c={'t':t,'type':'reveal','desc':'impact'};f=next(MID)
    elif name=='hit':c={'t':t,'type':'reveal','desc':'word slam'};f=next(HIT)
    elif name=='whoosh':c={'t':t,'type':'scene_cut','desc':'carried transition'};f=next(WHO)
    elif name=='tick':c={'t':t,'type':'hover_or_small_ui','desc':'counter tick'};f='kit/tick.ogg'
    else:continue
    swaps[str(len(cues))]=f;cues.append(c)
json.dump(cues,open(f'out/{opt}.cues.json','w'),indent=1);json.dump(swaps,open(f'out/{opt}.swaps.json','w'),indent=1)
print(opt,len(cues),'cues')
